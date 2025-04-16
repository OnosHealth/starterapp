from ninja import NinjaAPI, Schema
from typing import List, Optional
from .models import Member
from datetime import datetime
from django.shortcuts import get_object_or_404
from django.core.exceptions import ObjectDoesNotExist
from django.db import connection

api = NinjaAPI(title="Tenant API", urls_namespace="tenant_api")
    
class MemberUpdateSchema(Schema):
    name: str
    phone: Optional[str] = None
    email: Optional[str] = None

class MemberResponseSchema(Schema):
    id: int
    name: str
    phone: Optional[str] = None
    email: Optional[str] = None
    created_at: datetime

class ErrorSchema(Schema):
    detail: str

@api.exception_handler(ObjectDoesNotExist)
def object_does_not_exist_handler(request, exc):
    return api.create_response(
        request,
        {"detail": "Object not found."},
        status=404
    )

# Internal function for other endpoints to use
def get_member(request, member_id: int):
    member = Member.objects.get(id=member_id)
    return member

# Subtenant API endpoints
@api.get("/members/{subtenant_name}", response=List[MemberResponseSchema])
def list_members_by_subtenant(request, subtenant_name: str):
    if subtenant_name.isdigit():
        # This is a direct member ID access, redirect to the get_member endpoint
        return get_member(request, int(subtenant_name))
    
    if hasattr(request, 'subtenant') and request.subtenant:
        return Member.objects.filter(subtenant_id=request.subtenant.id)
    
    return Member.objects.none()

@api.post("/members/{subtenant_name}", response=MemberResponseSchema)
def create_member_for_subtenant(request, subtenant_name: str, payload: MemberUpdateSchema):
    if not hasattr(request, 'subtenant') or not request.subtenant:
        return api.create_response(
            request,
            {"detail": f"Subtenant '{subtenant_name}' not found."},
            status=404
        )
    
    member = Member.objects.create(
        name=payload.name,
        phone=payload.phone,
        email=payload.email,
        subtenant_id=request.subtenant.id
    )
    return member

@api.get("/members/{subtenant_name}/{member_id}", response=MemberResponseSchema)
def get_member_from_subtenant(request, subtenant_name: str, member_id: int):
    if not hasattr(request, 'subtenant') or not request.subtenant:
        return api.create_response(
            request,
            {"detail": f"Subtenant '{subtenant_name}' not found."},
            status=404
        )
    
    member = Member.objects.get(id=member_id, subtenant_id=request.subtenant.id)
    return member

@api.put("/members/{subtenant_name}/{member_id}", response=MemberResponseSchema)
def update_member_for_subtenant(request, subtenant_name: str, member_id: int, payload: MemberUpdateSchema):
    if not hasattr(request, 'subtenant') or not request.subtenant:
        return api.create_response(
            request,
            {"detail": f"Subtenant '{subtenant_name}' not found."},
            status=404
        )
    
    member = Member.objects.get(id=member_id, subtenant_id=request.subtenant.id)
    member.name = payload.name
    if payload.phone is not None:
        member.phone = payload.phone
    if payload.email is not None:
        member.email = payload.email
    member.save()
    return member

@api.delete("/members/{subtenant_name}/{member_id}", response={200: None})
def delete_member_from_subtenant(request, subtenant_name: str, member_id: int):
    if not hasattr(request, 'subtenant') or not request.subtenant:
        return api.create_response(
            request,
            {"detail": f"Subtenant '{subtenant_name}' not found."},
            status=404
        )
    
    member = Member.objects.get(id=member_id, subtenant_id=request.subtenant.id)
    member.delete()
    return 200