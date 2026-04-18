from django.contrib import admin
from .models import CustomUser
from django.contrib.auth.admin import UserAdmin

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'role','rollno', 'is_active', 'is_staff')
    readonly_fields = ('rollno',)

    def get_fieldsets(self, request, obj=None):
        # Start with the default fieldsets
        fieldsets = super().get_fieldsets(request, obj)

        # Remove any previous Additional Info if exists (prevents duplicates)
        fieldsets = tuple(f for f in fieldsets if f[0] != 'Additional Info')

        if obj and obj.role == 'student':
            fieldsets += (('Additional Info', {'fields': ('role', 'rollno','stream')}),)
        else:
            fieldsets += (('Additional Info', {'fields': ('role',)}),)
        return fieldsets

    def get_add_fieldsets(self, request):
        fieldsets = super().get_add_fieldsets(request)

        # Remove any previous Additional Info if exists (prevents duplicates)
        fieldsets = tuple(f for f in fieldsets if f[0] != 'Additional Info')

        # Show role + stream by default on add form; rollno will be assigned automatically
        fieldsets += (('Additional Info', {'fields': ('role','stream')}),)
        return fieldsets
