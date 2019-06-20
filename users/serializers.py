from rest_framework import serializers
from users import models
from django.contrib.auth import authenticate


class CreateUserSerializer(serializers.HyperlinkedModelSerializer):
    password = serializers.CharField(
        max_length=128,
        style={'input_type': 'password'},
        write_only=True)

    class Meta:
        model = models.User
        fields = ('email', 'password', 'first_name', 'last_name')


class UserInfoSerializer(serializers.ModelSerializer):
    role = serializers.SerializerMethodField();

    class Meta:
        model = models.User
        fields = ('id', 'email', 'first_name', 'last_name', 'role')

    @staticmethod
    def get_role(obj):
        obj = models.UserDetails.objects.get(user=obj)
        return obj.role.role


class LoginSerializer(serializers.Serializer):
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
