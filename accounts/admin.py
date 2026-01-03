from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, MemberProfile

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        ("Role", {"fields": ("role",)}),
    )
    list_display = ("username", "email", "role", "is_staff", "is_active")

@admin.register(MemberProfile)
class MemberProfileAdmin(admin.ModelAdmin):
    list_display = ("member_id", "user", "monthly_fee_amount", "is_active")
    search_fields = ("member_id", "user__username", "user__email")
