from django.contrib import admin
from import_export import resources
from import_export.admin import ImportExportModelAdmin

from apps.api.models import LeadContact


admin.site.site_title = 'Andersen Marketing Lead Helper'
admin.site.site_header = 'Andersen Marketing Lead Helper'
admin.site.index_title = 'Andersen Marketing Lead Helper'


class ReportResource(resources.ModelResource):
    class Meta:
        model = LeadContact


@admin.register(LeadContact)
class LeadContactAdmin(ImportExportModelAdmin):
    resource_class = ReportResource

    list_display = ("id", "lead_name", "linkedin_profile", "next_contact", "status", "created_at")
    search_fields = (
        "lead_name",
        "linkedin_profile",
    )
