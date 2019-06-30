from users import serializers, models
from django.http import JsonResponse
from django.contrib.auth.hashers import make_password
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions
from mydesq_hr.permissions.admin_permissions import AdminPermissions
from rest_framework_jwt.settings import api_settings


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
                'token': token
            }
        },
            status=200)


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
                last_name=serializer.validated_data['last_name'],
                employee_id=serializer.validated_data['employee_id'])

        except Exception:
            return JsonResponse({
                'success': False,
                'error': 'Error occurred in registering user!'
            },
                status=500)

        return Response({
            'success': True,
            'data': None
        },
            status=status.HTTP_201_CREATED)


class GetSelfUserInfoView(generics.RetrieveAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        try:
            serializer = serializers.UserInfoSerializer(models.User.objects.filter(id=self.request.user.id), many=True)
            return Response({
                'success': True,
                'data': serializer.data[0]

            },
                status=status.HTTP_200_OK)
        except Exception:
            return JsonResponse({
                'success': False,
                'error': 'Error occurred in getting user data!'
            },
                status=500)
