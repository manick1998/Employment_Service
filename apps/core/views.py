from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Count
from django.shortcuts import redirect, render
from django.views.generic import RedirectView, TemplateView

from apps.applications.models import JobApplication
from apps.jobs.models import Job


class HomeView(TemplateView):
    template_name = 'core/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['stats'] = {
            'jobs': Job.objects.filter(status=Job.Status.PUBLISHED, is_active=True).count(),
            'companies': Job.objects.values('company').distinct().count(),
            'applications': JobApplication.objects.count(),
        }
        context['featured_jobs'] = (
            Job.objects.filter(status=Job.Status.PUBLISHED, is_active=True)
            .select_related('company')
            .prefetch_related('skills')[:6]
        )
        context['top_skills'] = Job.objects.values('skills__name').exclude(skills__name='').annotate(total=Count('skills')).order_by('-total')[:5]
        return context


class DashboardRedirectView(LoginRequiredMixin, RedirectView):
    permanent = False

    def get_redirect_url(self, *args, **kwargs):
        user = self.request.user
        if user.is_superuser or user.role == user.Role.ADMIN:
            return '/admin/'
        if user.role == user.Role.RECRUITER:
            return '/accounts/dashboard/recruiter/'
        return '/accounts/dashboard/job-seeker/'


def permission_denied_view(request, exception):
    return render(request, 'errors/403.html', status=403)


def page_not_found_view(request, exception):
    return render(request, 'errors/404.html', status=404)


def server_error_view(request):
    return render(request, 'errors/500.html', status=500)
