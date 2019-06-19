from django.urls import path
from users import views

app_name = 'users'

urlpatterns = [
    path('new', views.CreateUserView.as_view(), name='new-user'),
    path('login', views.LoginView.as_view(), name='login'),
]
