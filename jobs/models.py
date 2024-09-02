from django.conf import settings
from django.db import models

class Job(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(max_length=500)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='created_jobs')
    organization = models.ForeignKey('organizations.Organization', on_delete=models.CASCADE, related_name='jobs')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class Application(models.Model):
    job = models.ForeignKey(Job, on_delete=models.CASCADE, related_name='applicants')
    applicant = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='applications')
    skill_description = models.TextField(max_length=500)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('job', 'applicant')

    def __str__(self):
        return f'{self.applicant.name} - {self.job.title}'