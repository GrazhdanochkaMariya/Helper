from django.db import models


class LeadContact(models.Model):
    class TypeEnum(models.TextChoices):
        CONTACT = "CONTACT"
        DNM = "DNM"
        REQUEST = "REQUEST"
        DECLINED = "DECLINED"

    lead_name = models.CharField(max_length=50)
    linkedin_profile = models.CharField(max_length=255, unique=True)
    status = models.CharField(max_length=50, choices=TypeEnum.choices, default=TypeEnum.CONTACT)
    next_contact = models.CharField(max_length=50, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.status}: {self.linkedin_profile}"
