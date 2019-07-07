from rest_framework import serializers
from users import models
from django.contrib.auth import authenticate
from django.db.models import Max


class CreateUserSerializer(serializers.HyperlinkedModelSerializer):
    password = serializers.CharField(
        max_length=128,
        style={'input_type': 'password'},
        write_only=True)

    class Meta:
        model = models.User
        fields = ('email', 'password', 'first_name', 'last_name', 'employee_id')


class GetReportingManagerSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.User
        fields = ('first_name', 'last_name', 'employee_id')


class GetUserInfoSerializer(serializers.ModelSerializer):
    role = serializers.SerializerMethodField()
    reporting_manager = serializers.SerializerMethodField()

    class Meta:
        model = models.User
        fields = ('email', 'first_name', 'last_name', 'employee_id', 'role', 'designation', 'reporting_manager')

    @staticmethod
    def get_role(obj):
        return obj.role.role

    @staticmethod
    def get_reporting_manager(obj):
        obj = models.UserDetails.objects.get(user=obj)
        serializer = GetReportingManagerSerializer(obj.reporting_manager)
        return serializer.data


class GetUserAllDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.UserDetails
        exclude = ('user', 'reporting_manager',)


class GetUserAddressDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.UserAddress
        exclude = ('id', 'user',)


class GetAccountDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.AccountDetails
        exclude = ('user',)


class GetUserDetailInfoSerializer(serializers.ModelSerializer):
    basic_details = serializers.SerializerMethodField()
    address_details = serializers.SerializerMethodField()

    class Meta:
        model = models.User
        fields = ('basic_details', 'address_details',)

    @staticmethod
    def get_basic_details(obj):
        obj = models.UserDetails.objects.get(user=obj)
        serializer = GetUserAllDetailsSerializer(obj)
        return serializer.data

    @staticmethod
    def get_address_details(obj):
        obj = models.UserAddress.objects.filter(user=obj)
        serializer = GetUserAddressDetailsSerializer(obj, many=True)
        return serializer.data


class LoginSerializer(serializers.Serializer):
    def update(self, instance, validated_data):
        pass

    def create(self, validated_data):
        pass

    email = serializers.EmailField()
    password = serializers.CharField(
        max_length=128,
        style={'input_type': 'password'},
        write_only=True)

    class Meta:
        fields = ('email', 'password')

    def validate(self, attrs):
        user = authenticate(
            self.context['request'],
            username=attrs.get('email'),
            password=attrs.get('password')
        )
        attrs['user'] = user
        return attrs


class GetNewEmployeeId(serializers.Serializer):
    def create(self, validated_data):
        pass

    def update(self, instance, validated_data):
        pass

    employee_id__max = serializers.IntegerField()

    class Meta:
        fields = ('employee_id__max',)
