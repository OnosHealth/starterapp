from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse

from django_tenants.admin import TenantAdminMixin
from .models import Client, Domain, SubTenant

class DomainInline(admin.TabularInline):
    model = Domain
    extra = 1

@admin.register(Client)
class ClientAdmin(TenantAdminMixin, admin.ModelAdmin):
    list_display = ('name', 'schema_name', 'created_on', 'get_subtenants')
    search_fields = ('name', 'schema_name')

    inlines = [DomainInline]

    def get_subtenants(self, obj):
        return obj.subtenants.count()
    
    get_subtenants.short_description = 'Number of SubTenants'

@admin.register(Domain)
class DomainAdmin(admin.ModelAdmin):
    list_display = ('domain', 'tenant', 'is_primary')
    list_filter = ('is_primary',)
    search_fields = ('domain',)
    list_select_related = ('tenant',)

@admin.register(SubTenant)
class SubTenantAdmin(admin.ModelAdmin):
    list_display = ('name', 'client', 'created_on')
    list_filter = ('client',)
    search_fields = ('name', 'client__name')
