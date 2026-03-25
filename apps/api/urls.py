from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import MyApplicationViewSet, PublicJobViewSet

router = DefaultRouter()
router.register('jobs', PublicJobViewSet, basename='api-jobs')
router.register('my-applications', MyApplicationViewSet, basename='api-my-applications')

urlpatterns = [
    path('', include(router.urls)),
]
