from rest_framework import serializers

from .models import Job, Application


class JobSerializer(serializers.ModelSerializer):
    class Meta:
        model = Job
        fields = ['id', 'title', 'description', 'created_by', 'organization', 'created_at', 'updated_at']
        read_only_fields = ['created_by', 'updated_at', 'created_at']

class ApplicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Application
        fields = ['id', 'job', 'applicant', 'skill_description', 'created_at']
        read_only_fields = ['created_at']

