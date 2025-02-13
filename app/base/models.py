from django.db import models
from django.utils import timezone

# Create logic models here.
# Configure the database

class JobStorage(models.Model):
    """Model for storing job data."""
    
    job_id = models.BigAutoField(primary_key = True)
    job_position = models.CharField(max_length = 100)
    job_description = models.TextField() 
    job_education = models.CharField(max_length = 300)
    
    EXPERIENCE_LEVELS = [
        ('NR', 'Not requirement'),
        ('LT1', 'Less than 1 year'),
        ('1Y', '1 year'),
        ('2Y', '2 years'),
        ('3Y', '3 years'),
        ('4Y', '4 years'),
        ('5Y', '5 years'),
        ('GT5', 'Greater than 5 years'),
    ]

    job_experience = models.CharField(max_length = 15, choices = EXPERIENCE_LEVELS, default = 'NR')
    
    job_responsibilities = models.TextField()
    job_tech_skills = models.CharField(max_length = 500)
    job_soft_skills = models.CharField(max_length = 500)
    job_certificates = models.CharField(max_length = 255, blank = True, null = True)
    
    STATES = [
        ('Open', 'Open'),
        ('Closed', 'Closed'),
    ]
    
    job_status = models.CharField(max_length = 10, choices = STATES, default = 'Open')
    job_start = models.DateTimeField()
    job_end = models.DateTimeField()

    def __str__(self):
        return f"{self.job_position}, ({self.job_experience}), ({self.job_start}), ({self.job_end})"
    
    
class ResumeStorage(models.Model):
    """Model for storing resume data."""
    
    resume_id = models.BigAutoField(primary_key = True)
    resume_name = models.CharField(max_length = 100, blank = False, null = True)
    resume_email = models.EmailField(blank = False, null = True)
    resume_phone = models.CharField(max_length = 15, blank = True, null = True)
    resume_path = models.CharField(max_length = 255, blank = False, null = False)
    resume_text = models.TextField()
    resume_date_added = models.DateTimeField(default=timezone.now, blank=False, null=False)
    resume_education = models.CharField(max_length = 100, blank = True, null = True)
    resume_experience = models.FloatField(default = 0.0)
    resume_tech_skills = models.CharField(max_length = 255, blank = True, null = True)
    resume_soft_skills = models.CharField(max_length = 255, blank = True, null = True)
    resume_certificates = models.CharField(max_length = 255, blank = True, null = True)
    
    STATES = [
        ('Passed', 'Passed'),
        ('Pending', 'Pending'),
        ('Rejected', 'Rejected'),
    ]
    
    resume_status = models.CharField(max_length = 10, choices = STATES, default = 'Pending')
    resume_summary = models.TextField()
    resume_score = models.FloatField(default = 0.0)
    resume_AI_explanation = models.TextField(blank = True, null = True)
    resume_job_id = models.ForeignKey(JobStorage, on_delete = models.CASCADE, blank = True, null = True)

    def __str__(self):
        return f"{self.resume_path}, ({self.resume_date_added}), ({self.resume_score})"