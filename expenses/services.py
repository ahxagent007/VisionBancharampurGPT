from django.db import transaction
from ledger.services import add_ledger_entry

@transaction.atomic
def approve_expense(*, expense, approved_by):
    expense.status = "APPROVED"
    expense.approved_by = approved_by
    expense.save(update_fields=["status", "approved_by"])

    add_ledger_entry(
        date=expense.expense_date,
        entry_type="EXPENSE",
        direction="OUT",
        amount=expense.amount,
        created_by=approved_by,
        member=None,
        description=f"Expense: {expense.category}",
    )
    return expense

@transaction.atomic
def reject_expense(*, expense, approved_by):
    expense.status = "REJECTED"
    expense.approved_by = approved_by
    expense.save(update_fields=["status", "approved_by"])
    return expense
