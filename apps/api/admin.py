from django.contrib import admin
from django.contrib.auth import get_user_model

from apps.api.models import LeadContact

User = get_user_model()


@admin.register(LeadContact)
class LeadContactAdmin(admin.ModelAdmin):
    list_display = ("id", "lead_name", "linkedin_profile", "next_contact", "status", "created_at")
    search_fields = (
        "lead_name",
        "linkedin_profile",
    )
