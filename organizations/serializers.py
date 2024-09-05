from django.template.defaultfilters import default
from rest_framework import serializers

from accounts.serializers import UserSerializer
from .models import Organization, OrganizationStaff


class OrganizationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Organization
        fields = ['id', 'name', 'valuation', 'location', 'admin', 'staff_access_code']
        read_only_fields = ['staff_access_code']

class CreateOrganizationSerializer(serializers.Serializer):
    name = serializers.CharField(required=True)
    valuation = serializers.DecimalField(max_digits=10, decimal_places=2)
    location = serializers.CharField()

    def create(self, validated_data):
        # Create and return a new Organization instance
        return Organization.objects.create(**validated_data)


class OrganizationStaffSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrganizationStaff
        fields = ['id', 'user', 'organization']


class OrganizationStaffCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrganizationStaff
        fields = ['id', 'user', 'organization']

class JoinOrganizationSerializer(serializers.Serializer):
    access_code = serializers.CharField(required=True)

    @staticmethod
    def validate_access_code(value):
        try:
            organization = Organization.objects.get(staff_access_code=value)
        except Organization.DoesNotExist:
            raise serializers.ValidationError("Invalid access code.")
        return value

    def create(self, validated_data):
        access_code = validated_data['access_code']

        return OrganizationStaff.objects.create(
            user=self.context['request'].user,
            organization=Organization.objects.get(staff_access_code=access_code)
        )

class OrganizationStaffDetailSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    organization = OrganizationSerializer()

    class Meta:
        model = OrganizationStaff
        fields = ['id', 'user', 'organization']