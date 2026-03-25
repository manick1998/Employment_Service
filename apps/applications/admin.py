from django.contrib import admin

from .models import JobApplication


@admin.register(JobApplication)
class JobApplicationAdmin(admin.ModelAdmin):
    list_display = ('job', 'job_seeker', 'status', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('job__title', 'job_seeker__username', 'job_seeker__email')
    list_select_related = ('job', 'job_seeker')
