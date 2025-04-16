from django.db import models

class Member(models.Model):
    name = models.CharField(max_length=100)
    email = models.TextField(blank=True)
    phone = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    subtenant_id = models.IntegerField(null=True, blank=True)
    
    def __str__(self):
        return self.name