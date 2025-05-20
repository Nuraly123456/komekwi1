from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser
from .models import Rating
from .models import Schedule


class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ['username', 'email', 'role', 'rating', 'is_staff', 'is_active']
    list_filter = ['role', 'is_staff', 'is_active']
    fieldsets = UserAdmin.fieldsets + (
        ('Custom Fields', {'fields': ('role', 'rating')}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Custom Fields', {'fields': ('role', 'rating')}),
    )
    search_fields = ['username', 'email']
    ordering = ['username']

    def changelist_view(self, request, extra_context=None):
        print("Using CustomUserAdmin")  # Debug: check if printed in console
        return super().changelist_view(request, extra_context)

admin.site.register(CustomUser, CustomUserAdmin)

admin.site.register(Rating)

admin.site.register(Schedule)
