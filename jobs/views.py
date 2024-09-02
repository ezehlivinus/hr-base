from django.shortcuts import render
from rest_framework import generics, permissions
from rest_framework.exceptions import PermissionDenied

from jobs.models import Job, Application
from jobs.serializers import JobSerializer, ApplicationSerializer
from organizations.models import OrganizationStaff


class CreateJobView(generics.CreateAPIView):
    serializer_class = JobSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        if self.request.user.role != 'ORG_HR':
            raise PermissionDenied('Only HRs can create job postings.')
        serializer.save(created_by=self.request.user)

class UpdateJobView(generics.UpdateAPIView):
    queryset = Job.objects.all()
    serializer_class = JobSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_update(self, serializer):
        if self.request.user.role != 'ORG_HR':
            raise PermissionDenied('Only HRs can update job postings.')
        serializer.save()

class ListJobsView(generics.ListAPIView):
    serializer_class = JobSerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = Job.objects.all()

class ApplyForJobView(generics.CreateAPIView):
    serializer_class = ApplicationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        job = Job.objects.get(pk=self.kwargs['job_id'])
        if OrganizationStaff.objects.filter(user=self.request.user, organization=job.organization).exists():
            raise PermissionDenied('You cannot apply for jobs in your own organization.')
        serializer.save(applicant=self.request.user, job=job)

class ListApplicationsView(generics.ListAPIView):
    serializer_class = ApplicationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        job = Job.objects.get(pk=self.kwargs['job_id'])
        user = self.request.user
        if user.role in ['ORG_HR', 'ORG_ADMIN'] and job.organization.admin == user:
            return Application.objects.filter(job=job)
        return Application.objects.none()

