from django.urls import include, path
from .views import CreateJobView, UpdateJobView, ListJobsView, ApplyForJobView, ListApplicationsView

urlpatterns = [
    path('create/', CreateJobView.as_view(), name='create_job'),
    path('update/<int:job_id>/', UpdateJobView.as_view(), name='update_job'),
    path('list/', ListJobsView.as_view(), name='list_jobs'),
    path('apply/<int:job_id>/', ApplyForJobView.as_view(), name='apply_for_job'),
    path('applications/<int:job_id>/', ListApplicationsView.as_view(), name='list_applications')
]