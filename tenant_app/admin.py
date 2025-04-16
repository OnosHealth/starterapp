from django.contrib import admin
from .models import Member
from shared_app.models import SubTenant
from django import forms

class MemberAdminForm(forms.ModelForm):
    subtenant_name = forms.ModelChoiceField(
        queryset=SubTenant.objects.all(),
        label="Subtenant",
        required=False,
        to_field_name="name"
    )
    
    class Meta:
        model = Member
        fields = ['name', 'email', 'phone', 'subtenant_name']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        instance = kwargs.get('instance')
        if instance and instance.subtenant_id:
            try:
                subtenant = SubTenant.objects.get(id=instance.subtenant_id)
                self.initial['subtenant_name'] = subtenant.name
            except SubTenant.DoesNotExist:
                pass

    def save(self, commit=True):
        instance = super().save(commit=False)
        subtenant_name = self.cleaned_data.get('subtenant_name')
        if subtenant_name:
            try:
                subtenant = SubTenant.objects.get(name=subtenant_name.name)
                instance.subtenant_id = subtenant.id
            except SubTenant.DoesNotExist:
                instance.subtenant_id = None
        else:
            instance.subtenant_id = None
        
        if commit:
            instance.save()
        return instance

@admin.register(Member)
class MemberAdmin(admin.ModelAdmin):
    form = MemberAdminForm
    list_display = ('name', 'email', 'phone', 'created_at', 'subtenant_name')
    search_fields = ('name', 'email', 'phone')
