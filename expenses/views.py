from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404

from accounts.decorators import staff_required, admin_required
from .models import Expense
from .forms import ExpenseForm
from .services import approve_expense, reject_expense

@staff_required
def expense_list(request):
    # staff sees all; you can restrict later if needed
    expenses = Expense.objects.order_by("-expense_date", "-created_at")
    return render(request, "expenses/expense_list.html", {"expenses": expenses})

@staff_required
def expense_create(request):
    form = ExpenseForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        exp = form.save(commit=False)
        exp.created_by = request.user
        exp.status = "SUBMITTED"
        exp.save()
        messages.success(request, "Expense submitted for approval.")
        return redirect("expenses:expense_list")
    return render(request, "expenses/expense_form.html", {"form": form})

@admin_required
def expense_approve(request, expense_id):
    exp = get_object_or_404(Expense, id=expense_id)

    if request.method == "POST":
        action = request.POST.get("action")
        if action == "approve":
            approve_expense(expense=exp, approved_by=request.user)
            messages.success(request, "Expense approved and ledger updated.")
        elif action == "reject":
            reject_expense(expense=exp, approved_by=request.user)
            messages.success(request, "Expense rejected.")
        return redirect("expenses:expense_list")

    return render(request, "expenses/expense_approve.html", {"expense": exp})
