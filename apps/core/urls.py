from django.urls import path

from .views import DashboardRedirectView, HomeView

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('dashboard/', DashboardRedirectView.as_view(), name='dashboard_redirect'),
]
