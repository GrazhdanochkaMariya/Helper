from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from apps.api.models import LeadContact


class ContactAPIView(APIView):
    def get(self, request):
        query_params = getattr(request, 'query_params', {})
        try:
            linkedin_profile = str(query_params["linkedin_profile"])
        except (TypeError, KeyError):
            return Response(status=status.HTTP_400_BAD_REQUEST)

        contact = LeadContact.objects.filter(linkedin_profile=linkedin_profile).first()
        if contact:
            data = {"lead_name": contact.lead_name}
            return Response(data=data, status=status.HTTP_200_OK)

        return Response(status=status.HTTP_404_NOT_FOUND)


class GoogleSheetsProcessorViews(APIView):
    def post(self, request, **kwargs):
        data = request.data
        # TODO validation

        if data["status"] == LeadContact.TypeEnum.CONTACT:
            contact = await LeadContactDAO().select_one_or_none_filter_by(
                linkedin_profile=data.linkedin_profile
            )
            if not contact:
                await LeadContactDAO().add_rows(data=data)

        elif data["status"] == LeadContact.TypeEnum.DECLINED:
            await LeadContactDAO().delete_rows_filer_by(
                linkedin_profile=data.linkedin_profile
            )

        elif data["status"] == LeadContact.TypeEnum.DNM:
            await LeadContactDAO().update_status_by_linkedin_profile(
                linkedin_profile=data.linkedin_profile, status=data.status
            )
