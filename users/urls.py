from django.urls import path
from users import views

app_name = 'users'

urlpatterns = [
    path('new', views.CreateUserView.as_view(), name='new-user'),
    path('info', views.GetUserInfoView.as_view(), name='view-all'),
    path('details', views.GetUserDetailsView.as_view(), name='user-details'),
    path('account-details', views.GetUserAccountDetails.as_view(), name='account-details'),
    path('all', views.GetAllUsersView.as_view(), name='view-all'),
    path('new-employee-id', views.GetNewEmployeeIdView.as_view(), name='new-employee-id'),
]
