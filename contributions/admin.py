from django.contrib import admin
from .models import ContributionCycle, MemberContribution, Payment

@admin.register(ContributionCycle)
class ContributionCycleAdmin(admin.ModelAdmin):
    list_display = ("year", "month", "due_date", "is_closed")
    list_filter = ("year", "is_closed")

@admin.register(MemberContribution)
class MemberContributionAdmin(admin.ModelAdmin):
    list_display = ("member", "cycle", "expected_amount", "paid_amount", "status")
    list_filter = ("status", "cycle__year")
    search_fields = ("member__member_id", "member__user__username")

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ("contribution", "amount", "method", "reference", "paid_at", "recorded_by")
    list_filter = ("method", "paid_at")
