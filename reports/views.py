from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from accounts.decorators import staff_required
from .queries import monthly_summary

@staff_required
def monthly_report(request):
    # Simple: choose year/month via query params ?year=2026&month=1
    year = int(request.GET.get("year", 2026))
    month = int(request.GET.get("month", 1))
    summary = monthly_summary(year, month)
    return render(request, "reports/monthly_report.html", {"year": year, "month": month, "summary": summary})
