from decimal import Decimal
from django.db import transaction
from django.utils import timezone

from accounts.models import MemberProfile
from ledger.services import add_ledger_entry
from .models import MemberContribution, Payment, ContributionCycle

@transaction.atomic
def generate_contributions_for_cycle(*, cycle: ContributionCycle) -> int:
    """
    Create MemberContribution rows for all active members for this cycle.
    Safe to run multiple times (won't duplicate due to unique_together).
    Returns number of created rows.
    """
    created_count = 0
    members = MemberProfile.objects.filter(is_active=True).select_related("user")

    for m in members:
        obj, created = MemberContribution.objects.get_or_create(
            member=m,
            cycle=cycle,
            defaults={
                "expected_amount": m.monthly_fee_amount,
                "paid_amount": Decimal("0"),
                "status": "PENDING",
            }
        )
        if created:
            created_count += 1
    return created_count

@transaction.atomic
def record_payment(*, contribution: MemberContribution, amount, method: str, recorded_by, reference: str = "") -> Payment:
    amount = Decimal(str(amount))
    if amount <= 0:
        raise ValueError("Amount must be greater than 0")

    if contribution.cycle.is_closed:
        raise ValueError("This cycle is closed. You cannot record payments.")

    payment = Payment.objects.create(
        contribution=contribution,
        amount=amount,
        method=method,
        reference=reference,
        recorded_by=recorded_by,
    )

    contribution.paid_amount = (contribution.paid_amount or Decimal("0")) + amount

    if contribution.paid_amount >= contribution.expected_amount:
        contribution.status = "PAID"
    elif contribution.paid_amount > 0:
        contribution.status = "PARTIAL"
    else:
        contribution.status = "PENDING"

    contribution.save(update_fields=["paid_amount", "status"])

    add_ledger_entry(
        date=timezone.now().date(),
        entry_type="DEPOSIT",
        direction="IN",
        amount=amount,
        created_by=recorded_by,
        member=contribution.member,
        description=f"Monthly deposit for {contribution.cycle}",
    )

    return payment
