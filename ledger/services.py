from decimal import Decimal
from django.db.models import Sum
from .models import LedgerEntry

def fund_balance() -> Decimal:
    inflow = LedgerEntry.objects.filter(direction="IN").aggregate(s=Sum("amount"))["s"] or Decimal("0")
    outflow = LedgerEntry.objects.filter(direction="OUT").aggregate(s=Sum("amount"))["s"] or Decimal("0")
    return inflow - outflow

def add_ledger_entry(*, date, entry_type, direction, amount, created_by, member=None, description=""):
    return LedgerEntry.objects.create(
        date=date,
        entry_type=entry_type,
        direction=direction,
        amount=amount,
        created_by=created_by,
        member=member,
        description=description,
    )
