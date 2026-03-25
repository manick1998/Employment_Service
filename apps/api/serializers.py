from rest_framework import serializers

from apps.applications.models import JobApplication
from apps.companies.models import Company
from apps.jobs.models import Job, Skill


class SkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = Skill
        fields = ('id', 'name', 'slug')


class CompanySummarySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = ('id', 'name', 'location', 'website')


class JobSerializer(serializers.ModelSerializer):
    company = CompanySummarySerializer(read_only=True)
    skills = SkillSerializer(many=True, read_only=True)

    class Meta:
        model = Job
        fields = (
            'id',
            'title',
            'slug',
            'description',
            'location',
            'salary_min',
            'salary_max',
            'employment_type',
            'experience_level',
            'company',
            'skills',
            'created_at',
        )


class JobApplicationSerializer(serializers.ModelSerializer):
    job = JobSerializer(read_only=True)

    class Meta:
        model = JobApplication
        fields = ('id', 'job', 'status', 'cover_letter', 'resume_snapshot_name', 'created_at', 'updated_at')
