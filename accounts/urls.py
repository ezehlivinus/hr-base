from django.urls import path

from accounts.views import CreateUserView, LoginView

urlpatterns = [
    path('create/', CreateUserView.as_view(), name='create_user'),
    path('login/', LoginView.as_view(), name='login'),
]