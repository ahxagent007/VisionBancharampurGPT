from django.db import models
from django.conf import settings

class LedgerEntry(models.Model):
    class Type(models.TextChoices):
        DEPOSIT = "DEPOSIT", "Deposit"
        EXPENSE = "EXPENSE", "Expense"
        ASSET_PURCHASE = "ASSET_PURCHASE", "Asset Purchase"
        INVESTMENT = "INVESTMENT", "Investment"
        RETURN = "RETURN", "Return/Income"
        DISTRIBUTION = "DISTRIBUTION", "Distribution"
        REFUND = "REFUND", "Refund"
        ADJUSTMENT = "ADJUSTMENT", "Adjustment"

    class Direction(models.TextChoices):
        IN = "IN", "Inflow"
        OUT = "OUT", "Outflow"

    created_at = models.DateTimeField(auto_now_add=True)
    date = models.DateField()

    entry_type = models.CharField(max_length=20, choices=Type.choices)
    direction = models.CharField(max_length=3, choices=Direction.choices)
    amount = models.DecimalField(max_digits=14, decimal_places=2)

    description = models.CharField(max_length=255, blank=True)

    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name="ledger_created")

    member = models.ForeignKey(
        "accounts.MemberProfile",
        null=True, blank=True,
        on_delete=models.PROTECT,
        related_name="ledger_entries"
    )

    def __str__(self):
        return f"{self.date} {self.entry_type} {self.direction} {self.amount}"
