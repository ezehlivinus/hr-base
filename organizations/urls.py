from django.urls import path

from organizations.views import ListOrganizationStaffView, JoinOrganizationView, CreateOrganizationView

urlpatterns = [
    path('create/', CreateOrganizationView.as_view(), name='create_organization'),
    path('staff/join/', JoinOrganizationView.as_view(), name='join_organization'),
    path('staff/', ListOrganizationStaffView.as_view(), name='organization_staff'),
]