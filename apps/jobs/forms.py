from django import forms

from apps.accounts.forms import BootstrapFormMixin

from .models import Job, Skill
from .selectors import skill_choices_queryset


class JobForm(BootstrapFormMixin, forms.ModelForm):
    class Meta:
        model = Job
        fields = (
            'title',
            'description',
            'location',
            'salary_min',
            'salary_max',
            'employment_type',
            'experience_level',
            'status',
            'is_active',
            'skills',
        )
        widgets = {
            'skills': forms.SelectMultiple(),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['skills'].queryset = skill_choices_queryset()
        self.fields['status'].help_text = 'Published jobs appear for job seekers. Draft jobs stay visible only to the recruiter.'
        if not self.instance.pk:
            self.fields['status'].initial = Job.Status.PUBLISHED
            self.fields['is_active'].initial = True


class JobSearchForm(BootstrapFormMixin, forms.Form):
    title = forms.CharField(required=False)
    location = forms.CharField(required=False)
    skill = forms.ModelChoiceField(queryset=Skill.objects.none(), required=False)
    salary_min = forms.IntegerField(required=False, min_value=0)
    salary_max = forms.IntegerField(required=False, min_value=0)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['skill'].queryset = skill_choices_queryset()


class RecruiterJobSearchForm(JobSearchForm):
    status = forms.ChoiceField(
        choices=[('', 'All statuses'), *Job.Status.choices],
        required=False,
    )
