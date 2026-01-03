from decimal import Decimal
from django.db.models import Sum
from ledger.models import LedgerEntry

def monthly_summary(year: int, month: int):
    qs = LedgerEntry.objects.filter(date__year=year, date__month=month)
    inflow = qs.filter(direction="IN").aggregate(s=Sum("amount"))["s"] or Decimal("0")
    outflow = qs.filter(direction="OUT").aggregate(s=Sum("amount"))["s"] or Decimal("0")
    return {"inflow": inflow, "outflow": outflow, "net": inflow - outflow}
