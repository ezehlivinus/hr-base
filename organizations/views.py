from django.shortcuts import render
from rest_framework import generics, permissions, status
from rest_framework.response import Response

from .models import Organization, OrganizationStaff
from .serializers import OrganizationSerializer, OrganizationStaffCreateSerializer


class CreateOrganizationView(generics.CreateAPIView):
    serializer_class = OrganizationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(admin=self.request.user)
        self.request.user.role = 'ORG_ADMIN'
        self.request.user.save()

class JoinOrganizationView(generics.CreateAPIView):
    serializer_class = OrganizationStaffCreateSerializer
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request, *args, **kwargs):
        access_code = request.data.get('access_code')
        try:
            organization = Organization.objects.get(staff_access_code=access_code)
        except Organization.DoesNotExist:
            return Response({
                'status': False,
                'message': 'Invalid access code'
            }, status=status.HTTP_404_NOT_FOUND)

        staff, created = organization.staff.get_or_create(user=request.user, organization=organization)
        if not created:
            return Response({
                'status': False,
                'message': 'You are already a staff of this organization'
            }, status=status.HTTP_400_BAD_REQUEST)

        request.user.role = 'ORG_STAFF'
        request.user.save()
        return Response({
            'status': True,
            'message': 'You have successfully joined the organization'
        })

class ListOrganizationStaffView(generics.ListAPIView):
    serializer_class = OrganizationStaffCreateSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.role == 'ORG_ADMIN':
            return OrganizationStaff.objects.filter(organization__admin=user)
        return OrganizationStaff.objects.none()

