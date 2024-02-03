from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User , Profile
# Register your models here.

class CustomUserAdmin(UserAdmin):
    model = User
    list_display = ('phone_number','is_superuser','is_verified')
    list_filter = ('phone_number','is_verified')
    searching_fields = ('phone_number',)
    ordering = ('phone_number',)
    fieldsets = (
        ('Authentication',{
            'fields':(
                'phone_number','token'
            ),
        }),
        ('Permissions',{
            'fields':(
                'is_staff','is_superuser','is_verified'
            ),
        }),
        ('Group Permissions',{
            'fields':(
                'groups','user_permissions',
            ),
        }),
        ('Important Date',{
            'fields':(
                'last_login',
            ),
        }),
    )
    add_fieldsets = (
        (None,{
            'classes':('wide',),
            'fields':('phone_number','is_staff','is_superuser','is_verified','token')
        }),
    )

admin.site.register(User,CustomUserAdmin)
admin.site.register(Profile)
