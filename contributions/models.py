from django.db import models
from django.conf import settings

class ContributionCycle(models.Model):
    year = models.PositiveIntegerField()
    month = models.PositiveSmallIntegerField()  # 1..12
    due_date = models.DateField()
    is_closed = models.BooleanField(default=False)

    class Meta:
        unique_together = ("year", "month")

    def __str__(self):
        return f"{self.year}-{self.month:02d}"

class MemberContribution(models.Model):
    class Status(models.TextChoices):
        PENDING = "PENDING", "Pending"
        PARTIAL = "PARTIAL", "Partial"
        PAID = "PAID", "Paid"
        OVERDUE = "OVERDUE", "Overdue"

    member = models.ForeignKey("accounts.MemberProfile", on_delete=models.PROTECT, related_name="contributions")
    cycle = models.ForeignKey(ContributionCycle, on_delete=models.PROTECT, related_name="member_contributions")

    expected_amount = models.DecimalField(max_digits=12, decimal_places=2)
    paid_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    status = models.CharField(max_length=10, choices=Status.choices, default=Status.PENDING)

    class Meta:
        unique_together = ("member", "cycle")

class Payment(models.Model):
    class Method(models.TextChoices):
        CASH = "CASH", "Cash"
        BANK = "BANK", "Bank"
        ONLINE = "ONLINE", "Online"

    contribution = models.ForeignKey(MemberContribution, on_delete=models.PROTECT, related_name="payments")
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    method = models.CharField(max_length=10, choices=Method.choices)
    reference = models.CharField(max_length=80, blank=True)
    paid_at = models.DateTimeField(auto_now_add=True)
    recorded_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name="payments_recorded")

    def __str__(self):
        return f"{self.contribution.member.member_id} {self.amount} {self.method}"
