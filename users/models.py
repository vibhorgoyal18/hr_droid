from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.base_user import AbstractBaseUser
from django.utils.translation import ugettext_lazy as _
from django.contrib.postgres.fields import JSONField

from .managers import UserManager


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(_('email address'), unique=True)
    user_id = models.IntegerField(null=True)
    date_joined = models.DateTimeField(_('date joined'), auto_now_add=True)
    is_active = models.BooleanField(_('active'), default=True)
    is_staff = models.BooleanField(_('staff'), default=True)
    first_name = models.CharField(max_length=50, blank=False)
    last_name = models.CharField(max_length=50, blank=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')


class UserRoles(models.Model):
    role = models.CharField(max_length=50, blank=False)
    level = models.IntegerField(blank=False)

    class Meta:
        verbose_name = _('user_roles')
        verbose_name_plural = _('users_roles')


class BankDetails(models.Model):
    user = models.OneToOneField(
        User,
        related_name='bank_user',
        on_delete=models.CASCADE,
        primary_key=True,
    )
    account_number = models.CharField(max_length=20, blank=False)
    ifsc = models.CharField(max_length=20, blank=False)
    bank_name = models.CharField(max_length=40, blank=False)
    branch_name = models.CharField(max_length=200, blank=False)

    class Meta:
        verbose_name = _('account_detail')
        verbose_name_plural = _('account_details')


class UserAddress(models.Model):

    user = models.ForeignKey(User, related_name='address_user', on_delete=models.CASCADE)
    address_type = models.CharField(max_length=11,
                                    choices=(
                                        ('PERMANENT', 'Permanent'),
                                        ('RESIDENTIAL', 'Residential')))
    house_number = models.CharField(max_length=20)
    street_name = models.CharField(max_length=20)
    locality = models.CharField(max_length=20)
    city = models.CharField(max_length=20)
    pincode = models.CharField(max_length=10)
    state = models.CharField(max_length=20)
    nearby = models.CharField(max_length=100)
    country = models.CharField(max_length=20)

    class Meta:
        verbose_name = _('address')
        verbose_name_plural = _('address')


class UserDetails(models.Model):
    user = models.OneToOneField(
        User,
        related_name='user',
        on_delete=models.CASCADE,
        primary_key=True,
    )

    designation = models.CharField(max_length=100, blank=False)
    role = models.ForeignKey(UserRoles, related_name='user_role', on_delete=False, blank=True)
    reporting_manager = models.ForeignKey(User, related_name='reporting_manager', on_delete=False)
    contact = models.CharField(max_length=20, blank=True)
    emergency_contact = models.CharField(max_length=20, blank=True)
    date_of_birth = models.DateField(blank=True)
    aadhaar_number = models.CharField(max_length=20, blank=True)
    pan_number = models.CharField(max_length=20, blank=True)
    personal_mail_id = models.EmailField(blank=True)

    class Meta:
        verbose_name = _('user_detail')
        verbose_name_plural = _('users_details')


