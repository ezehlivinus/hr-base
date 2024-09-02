from rest_framework import serializers

from models import Organization, OrganizationStaff


class OrganizationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Organization
        fields = ['id', 'name', 'valuation', 'location', 'admin', 'staff_access_code']
        read_only_fields = ['staff_access_code']

class OrganizationStaffSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrganizationStaff
        fields = ['id', 'user', 'organization']


class OrganizationStaffCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrganizationStaff
        fields = ['id', 'user', 'organization']