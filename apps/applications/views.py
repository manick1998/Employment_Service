from django.contrib import messages
from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import FormView, ListView, UpdateView

from apps.accounts.mixins import JobSeekerRequiredMixin, RecruiterRequiredMixin
from apps.jobs.models import Job

from .forms import ApplicationStatusUpdateForm, JobApplicationForm
from .models import JobApplication
from .selectors import applicants_for_job, applied_jobs_for_user
from .services import submit_application


class ApplyToJobView(JobSeekerRequiredMixin, FormView):
    form_class = JobApplicationForm
    template_name = 'applications/apply.html'

    def dispatch(self, request, *args, **kwargs):
        self.job = get_object_or_404(Job.objects.published().select_related('company'), slug=kwargs['slug'])
        if self.job.applications.filter(job_seeker=request.user).exists():
            messages.info(request, 'You have already applied for this job.')
            return redirect('applied_jobs')
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['job'] = self.job
        return context

    def form_valid(self, form):
        try:
            submit_application(
                job_seeker=self.request.user,
                job=self.job,
                cover_letter=form.cleaned_data.get('cover_letter', ''),
            )
        except ValueError as exc:
            form.add_error(None, str(exc))
            return self.form_invalid(form)
        messages.success(self.request, 'Your application was submitted successfully.')
        return redirect('applied_jobs')


class AppliedJobListView(JobSeekerRequiredMixin, ListView):
    template_name = 'applications/applied_jobs.html'
    context_object_name = 'applications'
    paginate_by = 10

    def get_queryset(self):
        return applied_jobs_for_user(self.request.user)


class RecruiterApplicantListView(RecruiterRequiredMixin, ListView):
    template_name = 'applications/recruiter_applicants.html'
    context_object_name = 'applications'
    paginate_by = 10

    def dispatch(self, request, *args, **kwargs):
        self.job = get_object_or_404(Job.objects.select_related('company'), slug=kwargs['slug'])
        if self.job.recruiter_id != request.user.id:
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        return applicants_for_job(self.job, self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['job'] = self.job
        return context


class ApplicationStatusUpdateView(RecruiterRequiredMixin, UpdateView):
    model = JobApplication
    form_class = ApplicationStatusUpdateForm
    template_name = 'applications/application_status_form.html'

    def get_queryset(self):
        return JobApplication.objects.filter(job__recruiter=self.request.user).select_related('job', 'job_seeker')

    def get_success_url(self):
        messages.success(self.request, 'Application status updated successfully.')
        return reverse_lazy('job_applicants', kwargs={'slug': self.object.job.slug})
