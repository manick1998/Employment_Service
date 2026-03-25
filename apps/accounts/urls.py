from django.contrib.auth.views import LogoutView, PasswordChangeDoneView, PasswordResetCompleteView, PasswordResetDoneView
from django.urls import path

from .views import (
    AccountSettingsView,
    CustomLoginView,
    CustomPasswordChangeView,
    CustomPasswordResetConfirmView,
    CustomPasswordResetView,
    JobSeekerDashboardView,
    JobSeekerProfileUpdateView,
    JobSeekerSignUpView,
    RecruiterDashboardView,
    RecruiterProfileUpdateView,
    RecruiterSignUpView,
    RegisterChoiceView,
)

urlpatterns = [
    path('register/', RegisterChoiceView.as_view(), name='register_choice'),
    path('register/job-seeker/', JobSeekerSignUpView.as_view(), name='job_seeker_signup'),
    path('register/recruiter/', RecruiterSignUpView.as_view(), name='recruiter_signup'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('dashboard/job-seeker/', JobSeekerDashboardView.as_view(), name='job_seeker_dashboard'),
    path('dashboard/recruiter/', RecruiterDashboardView.as_view(), name='recruiter_dashboard'),
    path('settings/account/', AccountSettingsView.as_view(), name='account_settings'),
    path('settings/job-seeker-profile/', JobSeekerProfileUpdateView.as_view(), name='job_seeker_profile_edit'),
    path('settings/recruiter-profile/', RecruiterProfileUpdateView.as_view(), name='recruiter_profile_edit'),
    path('password-change/', CustomPasswordChangeView.as_view(), name='password_change'),
    path('password-change/done/', PasswordChangeDoneView.as_view(template_name='registration/password_change_done.html'), name='password_change_done'),
    path('password-reset/', CustomPasswordResetView.as_view(), name='password_reset'),
    path('password-reset/done/', PasswordResetDoneView.as_view(template_name='registration/password_reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', CustomPasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', PasswordResetCompleteView.as_view(template_name='registration/password_reset_complete.html'), name='password_reset_complete'),
]
