import random
import string

from django.conf import settings
from django.db import models

def generate_access_code():
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))

class Organization(models.Model):
    name = models.CharField(max_length=255)
    valuation = models.DecimalField(max_digits=10, decimal_places=2)
    location = models.CharField(max_length=255)
    admin = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='administered_organizations')
    staff_access_code = models.CharField(max_length=6, default=generate_access_code, unique=True)

    def __str__(self):
        return self.name

class OrganizationStaff(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, related_name='staff')

    class Meta:
        unique_together = ('user', 'organization')

    def __str__(self):
        return f'{self.user.name} - {self.organization.name}'
