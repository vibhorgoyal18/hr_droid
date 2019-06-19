from django.contrib import admin
from django.urls import path, include
from rest_framework_swagger.views import get_swagger_view
from rest_framework_jwt.views import obtain_jwt_token, refresh_jwt_token, verify_jwt_token

schema_view = get_swagger_view(title='My API')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('user/', include('users.urls', namespace='user')),
    path('api-auth/refresh-token', refresh_jwt_token, name='refresh-token'),
    path('api-auth/token-verify', verify_jwt_token, name='verify-token'),
    path('', schema_view, name='api-root'),
]