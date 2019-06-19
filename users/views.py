from users import serializers
from django.http import JsonResponse
from django.contrib.auth.hashers import make_password
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions
from mydesq_hr.permissions.admin_permissions import AdminPermissions
from rest_framework_jwt.settings import api_settings


class CreateUserView(generics.CreateAPIView):
    """
    create a new user
    """
    serializer_class = serializers.CreateUserSerializer
    permission_classes = [permissions.IsAuthenticated, AdminPermissions]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            serializer.save(
                email=serializer.validated_data['email'],
                password=make_password(serializer.validated_data['password']),
                first_name=serializer.validated_data['first_name'],
                last_name=serializer.validated_data['last_name'], )

        except Exception as exception:
            return JsonResponse({
                'success': False,
                'error': 'Error occurred in registering user!'
            },
                status=500)

        return Response({'success': True, 'data': {'message': 'User created successfully'}},
                        status=status.HTTP_201_CREATED)


class LoginView(generics.CreateAPIView):
    serializer_class = serializers.LoginSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
        jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
        payload = jwt_payload_handler(serializer.validated_data['user'])
        token = jwt_encode_handler(payload)
        return JsonResponse({
            'message': 'success',
            'data': {
                'token': token,
                'user': serializers.UserInfoSerializer(serializer.validated_data['user']).data
            }
        },
            status=200)
