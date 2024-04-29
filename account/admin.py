from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import *
# Register your models here.

class User_Admin(UserAdmin):
    list_display = ('id', 'first_name' , 'last_name', 'username', 'email' , 'is_staff')
    
    list_display_links = ('id' , 'first_name' , 'last_name', 'username')
    
    fieldsets = UserAdmin.fieldsets + (  # Include 'gender' in the 'Personal Information' section
        ('Other Information', {
            'fields': ('registration_no',
                       'is_email_verified',),
        }),
    )
admin.site.register(User , User_Admin)

class User_Profile_Admin(admin.ModelAdmin):
    list_display = ('id', 'user','first_name' , 'last_name' ,'registration_no', 'email')
admin.site.register(User_Profile , User_Profile_Admin)