from django.contrib import admin
from .models import JobStorage, ResumeStorage
# Register your models here.


admin.site.register(JobStorage)
admin.site.register(ResumeStorage)