from django.contrib import admin
from users import models

admin.site.register(models.User)
admin.site.register(models.UserDetails)
admin.site.register(models.UserRoles)
admin.site.register(models.UserAddress)
admin.site.register(models.AccountDetails)
