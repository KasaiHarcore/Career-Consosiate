from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse

from .models import *
from .forms import *

from utils.reader import ResumeReader
from utils.parse import parse_resumes

import log, globals

# Create your views here.
# This is where the logic of the application is handled
# Contain Class, Function, things that are called by the URL

# Dashboard Pages
def dashbroad(request):
    return render(request, 'dashbroad.html')

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


# Candidate Pages
def candidate(request):
    query = request.GET.get('search', '')
    resumes = ResumeStorage.objects.all()
    
    if query:
        resumes = resumes.filter(resume_text__icontains=query)
        
    if request.method == "POST":
        action = request.POST.get("action")

        if action == "edit":
            resume_id = request.POST.get("resume_id")
            job_instance = get_object_or_404(ResumeStorage, resume_id=resume_id)
            form = JobForm(request.POST, instance=job_instance)
            if form.is_valid():
                form.save()
                return JsonResponse({"success": True, "resume_id": resume_id})
            return JsonResponse({"success": False})

        elif action == "delete":
            resume_id = request.POST.get("resume_id")
            job_instance = get_object_or_404(ResumeStorage, resume_id=resume_id)
            job_instance.delete()
            return JsonResponse({"success": True, "resume_id": resume_id})
        
    context = {
        'resumes': resumes,
        'search_query': query,
    }
    return render(request, 'candidates.html', context)

# CV Screening Pages
def matching(request):
    return render(request, 'matching.html')