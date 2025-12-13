from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import CustomUser


class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser

    list_display = ("phone_number", "full_name", "user_type", "is_staff", "is_active", "date_joined")
    list_filter = ("is_student", "is_staff", "is_active", "date_joined")
    search_fields = ("phone_number", "first_name", "last_name")
    date_hierarchy = "date_joined"
    ordering = ("-date_joined",)
    
    fieldsets = (
        (None, {"fields": ("phone_number", "password")}),
        ("Personal Info", {"fields": ("first_name", "last_name", "is_student")}),
        ("Permissions", {
            "fields": ("is_staff", "is_active", "is_superuser", "groups", "user_permissions"),
            "classes": ("collapse",)
        }),
        ("Important dates", {
            "fields": ("last_login", "date_joined"),
            "classes": ("collapse",)
        }),
    )

    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": (
                "phone_number", "password1", "password2", "first_name", "last_name", 
                "is_student", "is_staff", "is_active", "groups", "user_permissions"
            )}
        ),
    )
    
    readonly_fields = ("last_login", "date_joined")
    
    def full_name(self, obj):
        return obj.get_full_name() or "-"
    full_name.short_description = "Name"
    full_name.admin_order_field = "first_name"
    
    def user_type(self, obj):
        if obj.is_superuser:
            return "Superuser"
        elif obj.is_staff:
            return "Admin/Teacher"
        elif obj.is_student:
            return "Student"
        return "Unknown"
    user_type.short_description = "User Type"



admin.site.register(CustomUser, CustomUserAdmin)
