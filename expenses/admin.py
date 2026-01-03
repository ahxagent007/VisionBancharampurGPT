from django.contrib import admin
from .models import Expense

@admin.register(Expense)
class ExpenseAdmin(admin.ModelAdmin):
    list_display = ("category", "amount", "expense_date", "status", "created_by")
    list_filter = ("status", "expense_date")
    search_fields = ("category", "notes")
