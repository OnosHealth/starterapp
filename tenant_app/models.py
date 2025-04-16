from django.db import models
from shared_app.models import SubTenant

class Member(models.Model):
    name = models.CharField(max_length=100)
    email = models.TextField(blank=True)
    phone = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    subtenant_id = models.IntegerField(null=True, blank=True)
    
    def __str__(self):
        return self.name
        
    @property
    def subtenant_name(self):
        if self.subtenant_id:
            try:
                subtenant = SubTenant.objects.get(id=self.subtenant_id)
                return subtenant.name
            except SubTenant.DoesNotExist:
                return None
        return None
    
    @subtenant_name.setter
    def subtenant_name(self, name):
        if name:
            try:
                subtenant = SubTenant.objects.get(name=name)
                self.subtenant_id = subtenant.id
            except SubTenant.DoesNotExist:
                pass