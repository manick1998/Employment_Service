from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, PasswordChangeView, PasswordResetConfirmView, PasswordResetView
from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic import CreateView, TemplateView, UpdateView

from apps.applications.models import JobApplication
from apps.jobs.models import Job

from .forms import (
    JobSeekerProfileForm,
    JobSeekerSignUpForm,
    RecruiterProfileForm,
    RecruiterSignUpForm,
    StyledAuthenticationForm,
    StyledPasswordChangeForm,
    StyledPasswordResetForm,
    StyledSetPasswordForm,
    UserUpdateForm,
)
from .mixins import JobSeekerRequiredMixin, RecruiterRequiredMixin
from .models import User


class RegisterChoiceView(TemplateView):
    template_name = 'accounts/register_choice.html'


class JobSeekerSignUpView(CreateView):
    model = User
    form_class = JobSeekerSignUpForm
    template_name = 'accounts/signup.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['role_title'] = 'Job Seeker'
        return context

    def get_success_url(self):
        return reverse_lazy('job_seeker_dashboard')

    def form_valid(self, form):
        response = super().form_valid(form)
        login(self.request, self.object)
        messages.success(self.request, 'Your job seeker account has been created.')
        return response


class RecruiterSignUpView(CreateView):
    model = User
    form_class = RecruiterSignUpForm
    template_name = 'accounts/signup.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['role_title'] = 'Recruiter'
        return context

    def get_success_url(self):
        return reverse_lazy('recruiter_dashboard')

    def form_valid(self, form):
        response = super().form_valid(form)
        login(self.request, self.object)
        messages.success(self.request, 'Your recruiter account has been created.')
        return response


class CustomLoginView(LoginView):
    template_name = 'registration/login.html'
    authentication_form = StyledAuthenticationForm
    redirect_authenticated_user = True


class CustomPasswordChangeView(PasswordChangeView):
    template_name = 'registration/password_change_form.html'
    form_class = StyledPasswordChangeForm
    success_url = reverse_lazy('password_change_done')


class CustomPasswordResetView(PasswordResetView):
    template_name = 'registration/password_reset_form.html'
    email_template_name = 'registration/password_reset_email.txt'
    subject_template_name = 'registration/password_reset_subject.txt'
    success_url = reverse_lazy('password_reset_done')
    form_class = StyledPasswordResetForm


class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    template_name = 'registration/password_reset_confirm.html'
    form_class = StyledSetPasswordForm
    success_url = reverse_lazy('password_reset_complete')


class JobSeekerDashboardView(JobSeekerRequiredMixin, TemplateView):
    template_name = 'accounts/job_seeker_dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        profile = self.request.user.job_seeker_profile
        context['profile'] = profile
        context['application_count'] = JobApplication.objects.filter(job_seeker=self.request.user).count()
        context['recent_applications'] = (
            JobApplication.objects.filter(job_seeker=self.request.user)
            .select_related('job', 'job__company')[:5]
        )
        return context


class RecruiterDashboardView(RecruiterRequiredMixin, TemplateView):
    template_name = 'accounts/recruiter_dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['posted_jobs_count'] = Job.objects.filter(recruiter=self.request.user).count()
        context['open_jobs_count'] = Job.objects.filter(recruiter=self.request.user, status=Job.Status.PUBLISHED, is_active=True).count()
        context['recent_jobs'] = Job.objects.filter(recruiter=self.request.user).select_related('company')[:5]
        context['company'] = getattr(self.request.user, 'company', None)
        context['profile'] = self.request.user.recruiter_profile
        return context


class AccountSettingsView(LoginRequiredMixin, UpdateView):
    form_class = UserUpdateForm
    template_name = 'accounts/account_settings.html'
    success_url = reverse_lazy('account_settings')

    def get_object(self, queryset=None):
        return self.request.user

    def form_valid(self, form):
        messages.success(self.request, 'Account details updated successfully.')
        return super().form_valid(form)


class JobSeekerProfileUpdateView(JobSeekerRequiredMixin, UpdateView):
    form_class = JobSeekerProfileForm
    template_name = 'accounts/profile_form.html'
    success_url = reverse_lazy('job_seeker_dashboard')

    def get_object(self, queryset=None):
        return self.request.user.job_seeker_profile

    def form_valid(self, form):
        messages.success(self.request, 'Job seeker profile updated successfully.')
        return super().form_valid(form)


class RecruiterProfileUpdateView(RecruiterRequiredMixin, UpdateView):
    form_class = RecruiterProfileForm
    template_name = 'accounts/profile_form.html'
    success_url = reverse_lazy('recruiter_dashboard')

    def get_object(self, queryset=None):
        return self.request.user.recruiter_profile

    def form_valid(self, form):
        messages.success(self.request, 'Recruiter profile updated successfully.')
        return super().form_valid(form)
