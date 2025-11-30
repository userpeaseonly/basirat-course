from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import CustomUser


class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser

    list_display = ("phone_number", "is_student", "is_staff", "is_active",)
    list_filter = ("is_student", "is_staff", "is_active",)
    
    fieldsets = (
        (None, {"fields": ("phone_number", "password")}),
        ("Personal Info", {"fields": ("first_name", "last_name", "is_student")}),
        ("Permissions", {"fields": ("is_staff", "is_active", "is_superuser", "groups", "user_permissions")}),
        ("Important dates", {"fields": ("last_login", "date_joined")}),
    )

    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": (
                "phone_number", "password1", "password2", "is_student", "is_staff",
                "is_active", "groups", "user_permissions"
            )}
        ),
    )

    search_fields = ("phone_number", "first_name", "last_name")
    ordering = ("phone_number",)



admin.site.register(CustomUser, CustomUserAdmin)
