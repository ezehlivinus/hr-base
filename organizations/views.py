from django.shortcuts import render
from rest_framework import generics, permissions, status, serializers
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema, inline_serializer
from .models import Organization, OrganizationStaff
from .serializers import OrganizationSerializer, CreateOrganizationSerializer, JoinOrganizationSerializer, OrganizationStaffDetailSerializer


class CreateOrganizationView(generics.CreateAPIView):
    serializer_class = CreateOrganizationSerializer
    permission_classes = [permissions.IsAuthenticated]

    @extend_schema(
        request=CreateOrganizationSerializer,
        responses={
            201: inline_serializer(
                name='CreateOrganizationResponse',
                fields={
                    'status': serializers.BooleanField(),
                    'data': OrganizationSerializer(),
                }
            )
        },
        description="Create a new organization and set the current user as the admin."
    )
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        organization = self.perform_create(serializer)

        # Use the `OrganizationSerializer` to serialize the created object
        organization_serializer = OrganizationSerializer(organization)

        #
        return Response({
            'status': True,
            'data': organization_serializer.data
        }, status=status.HTTP_201_CREATED)

    def perform_create(self, serializer):
        print('Auth user', self.request.user, self.request.data)
        organization = serializer.save(admin=self.request.user)
        self.request.user.role = 'ORG_ADMIN'
        self.request.user.save()

        return organization

class JoinOrganizationView(generics.CreateAPIView):
    serializer_class = JoinOrganizationSerializer
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
    serializer_class = OrganizationStaffDetailSerializer
    permission_classes = [permissions.IsAuthenticated]

    # def get_queryset(self):
    #     user = self.request.user
    #     if user.role == 'ORG_ADMIN':
    #         return OrganizationStaff.objects.filter(organization__admin=user)
    #     return OrganizationStaff.objects.none()

    def get_queryset(self):
        user = self.request.user
        if user.role == 'ORG_ADMIN':
            return OrganizationStaff.objects.filter(organization__admin=user).select_related('user', 'organization')
        return OrganizationStaff.objects.none()

