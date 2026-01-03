from django.db import models
from django.conf import settings

class Expense(models.Model):
    class Status(models.TextChoices):
        SUBMITTED = "SUBMITTED", "Submitted"
        APPROVED = "APPROVED", "Approved"
        REJECTED = "REJECTED", "Rejected"

    category = models.CharField(max_length=80)
    amount = models.DecimalField(max_digits=14, decimal_places=2)
    expense_date = models.DateField()
    notes = models.TextField(blank=True)

    status = models.CharField(max_length=10, choices=Status.choices, default=Status.SUBMITTED)

    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name="expenses_created")
    approved_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, null=True, blank=True,
        on_delete=models.PROTECT, related_name="expenses_approved"
    )

    def __str__(self):
        return f"{self.category} - {self.amount} ({self.status})"
