from django.contrib import admin

from .models import Job, Skill


@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    search_fields = ('name',)
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    list_display = ('title', 'company', 'recruiter', 'status', 'is_active', 'created_at')
    list_filter = ('status', 'employment_type', 'experience_level', 'is_active')
    search_fields = ('title', 'description', 'location', 'company__name', 'recruiter__username')
    list_select_related = ('company', 'recruiter')
    filter_horizontal = ('skills',)
