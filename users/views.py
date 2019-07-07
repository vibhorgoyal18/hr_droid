from users import serializers, models
from django.http import JsonResponse
from django.contrib.auth.hashers import make_password
from rest_framework import views, generics
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions
from mydesq_hr.permissions.admin_permissions import AdminPermissions
from rest_framework_jwt.settings import api_settings
from rest_framework.schemas import ManualSchema
from coreapi import Field
from django.utils.datastructures import MultiValueDictKeyError
from django.db.models import Max


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
                'user': {
                    'first_name': serializer.validated_data['user'].first_name,
                    'last_name': serializer.validated_data['user'].last_name,
                    'role': serializer.validated_data['user'].role.role
                }
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

            return Response({
                'success': True,
                'data': None
            },
                status=status.HTTP_201_CREATED)
        except Exception:
            return JsonResponse({
                'success': False,
                'message': 'Error occurred in registering user!'
            },
                status=500)


class GetUserInfoView(generics.RetrieveAPIView):
    permission_classes = [permissions.IsAuthenticated]
    schema = ManualSchema(fields=[
        Field("employee_id",
              required=True,
              location='query',
              type='integer',
              description='Employee ID id of user')
    ])

    def get(self, request, *args, **kwargs):
        try:
            if request.query_params['employee_id'] == 'me':
                employee_id = self.request.user.employee_id
            else:
                employee_id = int(self.request.query_params['employee_id'])
            serializer = serializers.GetUserInfoSerializer(
                models.User.objects.get(employee_id=employee_id))
            return Response({
                'success': True,
                'data': serializer.data

            },
                status=status.HTTP_200_OK)
        except models.User.DoesNotExist:
            return JsonResponse({
                'success': False,
                'message': 'User with this employee id does not exist'
            }, status=400)
        except MultiValueDictKeyError:
            return JsonResponse({
                'success': False,
                'message': 'Parameter value "employee_id" is required'
            }, status=400)
        except ValueError:
            return JsonResponse({
                'success': False,
                'message': 'Parameter value "employee_id" is invalid'
            }, status=400)
        # except Exception:
        #     return JsonResponse({
        #         'success': False,
        #         'error': 'Error occurred in getting user data!'
        #     },
        #         status=500)


class GetUserDetailsView(generics.RetrieveAPIView):
    permission_classes = [permissions.IsAuthenticated]
    schema = ManualSchema(fields=[
        Field("employee_id",
              required=True,
              location='query',
              type='integer',
              description='Employee ID id of user')
    ])

    def get(self, request, *args, **kwargs):

        try:
            if request.query_params['employee_id'] == 'me':
                employee_id = self.request.user.employee_id
            else:
                employee_id = int(self.request.query_params['employee_id'])
            user = models.User.objects.get(employee_id=employee_id)
        except ValueError:
            return JsonResponse({
                'success': False,
                'message': 'Invalid user id'
            },
                status=400)
        except models.User.DoesNotExist:
            return JsonResponse({
                'success': False,
                'error': 'User with this id does not exist'
            }, status=400)
        except MultiValueDictKeyError:
            return JsonResponse({
                'success': False,
                'message': 'Parameter value "employee_id" is required'
            }, status=400)
        try:
            serializer = serializers.GetUserDetailInfoSerializer(user)
            return Response({
                'success': True,
                'data': serializer.data
            },
                status=status.HTTP_200_OK)

        except Exception:
            return JsonResponse({
                'success': False,
                'message': 'Error occurred in getting user data!'
            },
                status=500)


class GetUserAccountDetails(generics.RetrieveAPIView):
    permission_classes = [permissions.IsAuthenticated]
    schema = ManualSchema(fields=[
        Field("employee_id",
              required=True,
              location='query',
              type='integer',
              description='Employee ID id of user')
    ])

    def get(self, request, *args, **kwargs):
        try:
            if request.query_params['employee_id'] == 'me':
                employee_id = self.request.user.employee_id
            else:
                employee_id = int(self.request.query_params['employee_id'])
            user = models.User.objects.get(employee_id=employee_id)
            account_details = models.AccountDetails.objects.get(user=user)
            serializer = serializers.GetAccountDetailsSerializer(account_details)
            return Response({
                'success': True,
                'data': serializer.data
            },
                status=status.HTTP_200_OK)
        except ValueError:
            return JsonResponse({
                'success': False,
                'message': 'Invalid user id'
            },
                status=400)
        except models.User.DoesNotExist:
            return JsonResponse({
                'success': False,
                'message': 'User with this id does not exist'
            }, status=400)

        except MultiValueDictKeyError:
            return JsonResponse({
                'success': False,
                'message': 'Parameter value "employee_id" is required'
            }, status=400)


class GetAllUsersView(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated, AdminPermissions]
    serializer_class = serializers.GetUserInfoSerializer
    queryset = models.User.objects.all()

    def list(self, request, *args, **kwargs):
        try:
            queryset = self.get_queryset()
            serializer = serializers.GetUserInfoSerializer(queryset, many=True)
            return JsonResponse({
                'success': True,
                'data': serializer.data
            }, status=200)
        except Exception:
            return JsonResponse({
                'success': False,
                'message': 'Error occurred in getting user data!'
            },
                status=500)


class GetNewEmployeeIdView(generics.RetrieveAPIView):
    serializer_class = serializers.GetNewEmployeeId
    permission_classes = (AdminPermissions,)
    queryset = models.User.objects.aggregate(Max('employee_id'))

    def get(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=self.get_queryset())
        serializer.is_valid(raise_exception=True)

        return JsonResponse({
            'success': True,
            'data': {
                'employee_id': serializer.validated_data['employee_id__max'] + 1
            }
        },
            status=200)
