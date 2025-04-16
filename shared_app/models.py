from django.db import models
from django_tenants.models import TenantMixin, DomainMixin

class Client(TenantMixin):
    name = models.CharField(max_length=100)
    created_on = models.DateField(auto_now_add=True)

    # Default true, schema will be automatically created and synced when it is saved
    auto_create_schema = True

    def __str__(self):
        return self.name

class Domain(DomainMixin):
    pass

class SubTenant(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='subtenants')
    name = models.CharField(max_length=100)  # e.g., 'ny', 'al'
    created_on = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.client.name}-{self.name}"