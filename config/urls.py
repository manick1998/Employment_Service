from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

admin.site.site_header = 'Job Portal Administration'
admin.site.site_title = 'Job Portal Admin'
admin.site.index_title = 'Portal management'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('apps.core.urls')),
    path('accounts/', include('apps.accounts.urls')),
    path('companies/', include('apps.companies.urls')),
    path('jobs/', include('apps.jobs.urls')),
    path('applications/', include('apps.applications.urls')),
    path('api/', include('apps.api.urls')),
]

handler403 = 'apps.core.views.permission_denied_view'
handler404 = 'apps.core.views.page_not_found_view'
handler500 = 'apps.core.views.server_error_view'

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
