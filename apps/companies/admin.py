from django.contrib import admin

from .models import Company


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ('name', 'owner', 'location', 'is_active')
    list_filter = ('is_active', 'location')
    search_fields = ('name', 'owner__username', 'owner__email', 'location')
    prepopulated_fields = {'slug': ('name',)}
