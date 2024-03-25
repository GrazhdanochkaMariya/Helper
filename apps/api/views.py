from django.conf import settings
from django.http import JsonResponse
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import extend_schema, OpenApiParameter, inline_serializer
from rest_framework import status, serializers, permissions
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from apps.api.models import LeadContact


class AllowDebugAuthMixin:
    permission_classes = [permissions.IsAuthenticated] if settings.AUTH_ENABLED else []


@extend_schema(
    parameters=[
        OpenApiParameter(
            "linkedin_profile",
            OpenApiTypes.STR,
            OpenApiParameter.QUERY,
            required=True,
            description="Linkedin profile name",
        ),
    ],
    responses={
        (status.HTTP_200_OK, 'application/json'): inline_serializer(
           name='ContactAPIResponse',
           fields={
               'lead_name': serializers.CharField(),
           }
        ),
    }
)
class ContactAPIView(AllowDebugAuthMixin, APIView):
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


@extend_schema()
class GoogleSheetsProcessorViews(AllowDebugAuthMixin, APIView):
    def post(self, request, **kwargs):
        data = request.data
        # TODO validation

        if data["status"] == LeadContact.TypeEnum.CONTACT:
            # contact = await LeadContactDAO().select_one_or_none_filter_by(
            #     linkedin_profile=data.linkedin_profile
            # )
            # if not contact:
            #     await LeadContactDAO().add_rows(data=data)
            pass

        elif data["status"] == LeadContact.TypeEnum.DECLINED:
            # await LeadContactDAO().delete_rows_filer_by(
            #     linkedin_profile=data.linkedin_profile
            # )
            pass

        elif data["status"] == LeadContact.TypeEnum.DNM:
            # await LeadContactDAO().update_status_by_linkedin_profile(
            #     linkedin_profile=data.linkedin_profile, status=data.status
            # )
            pass


class ObtainTokenView(APIView):
    authentication_classes = [SessionAuthentication]
    permission_classes = [IsAuthenticated]

    @extend_schema(
        request=inline_serializer(
            name='ObtainTokenRequest',
            fields={}
        ),
        responses={
            (status.HTTP_200_OK, 'application/json'): inline_serializer(
               name='ObtainTokenResponse',
               fields={
                   'access_token': serializers.CharField(),
                   'refresh_token': serializers.CharField(),
               }
            ),
        }
    )
    def post(self, request, **kwargs):
        user = request.user
        token = RefreshToken.for_user(user)  # generate token without username & password
        response = {
            "access_token": str(token.access_token),
            "refresh_token": str(token),
        }
        return JsonResponse(response, status=status.HTTP_200_OK)
