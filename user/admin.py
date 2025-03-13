from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import User
# Register your models here.
class CustomUserAdmin(UserAdmin):
    model = User
    list_display = ('id', 'first_name', 'email', 'date_joined', 'last_login')
    readonly_fields = ('date_joined','last_login')
    list_display_links = ('id', 'first_name', 'email')
    ordering = ['-date_joined',]
    search_fields = ('email', 'username')


    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal Info', {'fields': ('first_name', 'last_name', 'username', 'phone_number')}),
        ('Permissions', {'fields': ('is_staff', 'is_superuser', 'is_active', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )


admin.site.register(User, CustomUserAdmin)