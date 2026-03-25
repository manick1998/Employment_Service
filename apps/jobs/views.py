from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import CreateView, DetailView, ListView, UpdateView

from apps.accounts.mixins import RecruiterRequiredMixin

from .forms import JobForm, JobSearchForm, RecruiterJobSearchForm
from .models import Job
from .selectors import public_jobs_queryset, recruiter_filtered_jobs_queryset
from .services import close_job


class PublicJobListView(ListView):
    template_name = 'jobs/job_list.html'
    context_object_name = 'jobs'
    paginate_by = 10

    def get_queryset(self):
        self.search_form = JobSearchForm(self.request.GET or None)
        if self.search_form.is_valid():
            return public_jobs_queryset(self.search_form.cleaned_data)
        return public_jobs_queryset()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_form'] = self.search_form
        return context


class PublicJobDetailView(DetailView):
    template_name = 'jobs/job_detail.html'
    context_object_name = 'job'

    def get_queryset(self):
        return Job.objects.published().select_related('company', 'recruiter').prefetch_related('skills')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        job = self.object
        has_applied = False
        if self.request.user.is_authenticated and self.request.user.role == self.request.user.Role.JOB_SEEKER:
            has_applied = job.applications.filter(job_seeker=self.request.user).exists()
        context['has_applied'] = has_applied
        return context


class RecruiterJobListView(RecruiterRequiredMixin, ListView):
    template_name = 'jobs/recruiter_job_list.html'
    context_object_name = 'jobs'
    paginate_by = 10

    def get_queryset(self):
        self.search_form = RecruiterJobSearchForm(self.request.GET or None)
        if self.search_form.is_valid():
            return recruiter_filtered_jobs_queryset(self.request.user, self.search_form.cleaned_data)
        return recruiter_filtered_jobs_queryset(self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_form'] = self.search_form
        return context


class RecruiterJobCreateView(RecruiterRequiredMixin, CreateView):
    form_class = JobForm
    template_name = 'jobs/job_form.html'
    success_url = reverse_lazy('recruiter_job_list')

    def dispatch(self, request, *args, **kwargs):
        if not hasattr(request.user, 'company'):
            messages.warning(request, 'Create your company profile before posting jobs.')
            return redirect('company_edit')
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        job = form.save(commit=False)
        job.recruiter = self.request.user
        job.company = self.request.user.company
        job.save()
        form.save_m2m()
        messages.success(self.request, 'Job posted successfully.')
        return redirect(self.success_url)


class RecruiterJobUpdateView(RecruiterRequiredMixin, UpdateView):
    form_class = JobForm
    template_name = 'jobs/job_form.html'
    success_url = reverse_lazy('recruiter_job_list')

    def get_queryset(self):
        return Job.objects.filter(recruiter=self.request.user).select_related('company').prefetch_related('skills')

    def form_valid(self, form):
        messages.success(self.request, 'Job updated successfully.')
        return super().form_valid(form)


class RecruiterJobCloseView(RecruiterRequiredMixin, View):
    def post(self, request, slug, *args, **kwargs):
        job = get_object_or_404(Job, slug=slug, recruiter=request.user)
        close_job(job)
        messages.success(request, 'Job has been closed and hidden from active listings.')
        return redirect('recruiter_job_list')
