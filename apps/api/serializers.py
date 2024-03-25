from rest_framework import serializers

from apps.api.models import LeadContact


class LeadContactSerializer(serializers.Serializer):
    """Serializer for profile"""
    lead_name = serializers.CharField(max_length=255)
    linkedin_profile = serializers.CharField(max_length=255)
    next_contact = serializers.CharField(max_length=255, required=False)
    status = serializers.CharField(max_length=255)

    def validate_status(self, value):
        """Validator for status"""
        if value not in [choice[0] for choice in LeadContact.TypeEnum.choices]:
            raise serializers.ValidationError("Invalid status")
        return value.upper()

    def create(self, validated_data):
        return LeadContact.objects.create(**validated_data)