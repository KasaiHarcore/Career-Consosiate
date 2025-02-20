from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from .models import *
from .forms import *
import os

from utils.reader import ResumeReader

import globals

# Create your views here.
# This is where the logic of the application is handled
# Contain Class, Function, things that are called by the URL

# Dashboard Pages
def dashboard(request):
    active_work_count = JobStorage.objects.filter(job_status='Open').count()
    pending_candidates_count = ResumeStorage.objects.filter(resume_status='Pending').count()
    completed_count = ResumeStorage.objects.filter(resume_status__in=['Passed','Rejected']).count()
    total_candidates_count = ResumeStorage.objects.count()
    job_openings_count = JobStorage.objects.filter(job_status__in=['Open', 'Closed']).count()

    if total_candidates_count > 0:
        passing_rate = (ResumeStorage.objects.filter(resume_status='Passed').count() / total_candidates_count) * 100
    else:
        passing_rate = 0

    recent_resumes = ResumeStorage.objects.order_by('-resume_date_added')[:5]

    context = {
        'active_work': active_work_count,
        'pending_candidates': pending_candidates_count,
        'completed': completed_count,
        'total_candidates': total_candidates_count,
        'job_counts': job_openings_count,
        'passing_rate': passing_rate,
        'recent_resumes': recent_resumes,
    }

    return render(request, 'dashboard.html', context)

# Job Pages
def job(request):
    query = request.GET.get('search', '')
    jobs = JobStorage.objects.all()
    form = JobForm(request.POST or None)

    if query:
        jobs = jobs.filter(job_position__icontains=query)

    total_jobs = jobs.count()
    open_positions = jobs.filter(job_status='Open').count()
    closed_positions = jobs.filter(job_status='Closed').count()
    
    if request.method == "POST":
        action = request.POST.get("action")

        if action == "create":
            form = JobForm(request.POST)
            if form.is_valid():
                form.save()
                return JsonResponse({"success": True})

        elif action == "edit":
            job_id = request.POST.get("job_id")
            job_instance = get_object_or_404(JobStorage, job_id=job_id)
            form = JobForm(request.POST, instance=job_instance)
            if form.is_valid():
                form.save()
                return JsonResponse({"success": True, "job_id": job_id})
            return JsonResponse({"success": False})

        elif action == "delete":
            job_id = request.POST.get("job_id")
            job_instance = get_object_or_404(JobStorage, job_id=job_id)
            job_instance.delete()
            return JsonResponse({"success": True, "job_id": job_id})
        
    context = {
        'jobs': jobs,
        'total_jobs': total_jobs,
        'open_positions': open_positions,
        'closed_positions': closed_positions,
        'search_query': query,
        'form': form,
    }

    return render(request, 'job.html', context)

def candidate(request):
    query = request.GET.get('search', '')
    resumes = ResumeStorage.objects.all()
    jobs = JobStorage.objects.all()
    if query:
        resumes = resumes.filter(resume_text__icontains=query)

    if request.method == "POST":
        if 'resume_files' in request.FILES:
            upload_files = request.FILES.getlist('resume_files')
            
            uploaded_paths = []

            for f in upload_files:
                destination_path = os.path.join(globals.default_working_folder, f.name)
                with open(destination_path, 'wb+') as dest:
                    for chunk in f.chunks():
                        dest.write(chunk)

                uploaded_paths.append(destination_path)
            ResumeReader(uploaded_paths)

            return render(request, 'candidates.html', {
                'resumes': resumes,
                'search_query': query,
                'message': 'Files uploaded and processed successfully!'
            })

        action = request.POST.get("action")
        if action == "edit":
            resume_id = request.POST.get("resume_id")
            resume_instance = get_object_or_404(ResumeStorage, resume_id=resume_id)
            form = ResumeForm(request.POST, instance=resume_instance)
            
            if form.is_valid():
                form.save()
                return JsonResponse({"success": True, "resume_id": resume_id})
            else:
                # Include form errors for better debugging
                return JsonResponse({"success": False, "errors": form.errors})

        elif action == "delete":
            resume_id = request.POST.get("resume_id")
            resume_instance = get_object_or_404(ResumeStorage, resume_id=resume_id)
            resume_instance.delete()
            return JsonResponse({"success": True, "resume_id": resume_id})

    context = {
        'jobs': jobs,
        'resumes': resumes,
        'search_query': query,
    }
    return render(request, 'candidates.html', context)

# CV Screening Pages
def matching(request):
    return render(request, 'matching.html')