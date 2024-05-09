from django.contrib import admin
from .models import User
class UserAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,               {'fields': ['id']}),
        (None,               {'fields': ['firstName']}),
        (None,               {'fields': ['lastName']}),
        (None,               {'fields': ['username']}),
        (None,               {'fields': ['email']}),
        (None,               {'fields': ['password']}),
        (None,               {'fields': ['additional_user_info']}),
        (None,               {'fields': ['is_active']}),
        (None,               {'fields': ['is_staff']}),
        (None,               {'fields': ['is_superuser']}),
        (None,               {'fields': ['date_joined']}),
        (None,               {'fields': ['updated_at']}),
    ]
    list_display = ('id','firstName','lastName','username', 'email','password','additional_user_info',
                    'is_active','is_staff','is_superuser','date_joined','updated_at')
admin.site.register(User, UserAdmin)

