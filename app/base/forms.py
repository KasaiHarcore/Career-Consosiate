from django import forms
from .models import *

class JobForm(forms.ModelForm):
    class Meta:
        model = JobStorage
        fields = '__all__'
        widgets = {
            'job_position': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter job title'}),
            'job_description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Enter job description'}),
            'job_education': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter required education'}),
            'job_experience': forms.Select(attrs={'class': 'form-select'}),
            'job_responsibilities': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Enter responsibilities'}),
            'job_tech_skills': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter required technical skills'}),
            'job_soft_skills': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter required soft skills'}),
            'job_certificates': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter required certificates'}),
            'job_status': forms.Select(attrs={'class': 'form-select'}),
            'job_start': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'job_end': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }
        
class ResumeForm(forms.ModelForm):
    class Meta:
        model = ResumeStorage
        fields = '__all__'
        widgets = {
            'resume_path': forms.FileInput(attrs={'class': 'form-control'}),
            'resume_text': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Enter resume text'}),
            'resume_date_added': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'resume_education': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter education'}),
            'resume_experience': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter experience'}),
            'resume_tech_skills': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter technical skills'}),
            'resume_soft_skills': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter soft skills'}),
            'resume_certificates': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter certificates'}),
            'resume_summary': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Enter summary'}),
            'resume_status': forms.Select(attrs={'class': 'form-select'}),
            'resume_job_id': forms.Select(attrs={'class': 'form-select'}),
        }