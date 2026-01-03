from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    class Role(models.TextChoices):
        ADMIN = "ADMIN", "Admin"
        STAFF = "STAFF", "Staff"
        MEMBER = "MEMBER", "Member"

    role = models.CharField(max_length=10, choices=Role.choices, default=Role.MEMBER)

class MemberProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="member_profile")
    member_id = models.CharField(max_length=30, unique=True)
    phone = models.CharField(max_length=30, blank=True)
    address = models.TextField(blank=True)
    join_date = models.DateField(auto_now_add=True)
    monthly_fee_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        name = self.user.get_full_name() or self.user.username
        return f"{self.member_id} - {name}"
