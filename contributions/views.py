from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404

from accounts.decorators import staff_required, member_required
from .models import ContributionCycle, MemberContribution
from .forms import CycleForm, PaymentForm
from .services import generate_contributions_for_cycle, record_payment

@staff_required
def cycle_list(request):
    cycles = ContributionCycle.objects.order_by("-year", "-month")
    return render(request, "contributions/cycle_list.html", {"cycles": cycles})

@staff_required
def cycle_create(request):
    form = CycleForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        cycle = form.save()
        messages.success(request, f"Cycle created: {cycle}")
        return redirect("contributions:cycle_list")
    return render(request, "contributions/cycle_create.html", {"form": form})

@staff_required
def cycle_generate(request, cycle_id):
    cycle = get_object_or_404(ContributionCycle, id=cycle_id)
    created_count = generate_contributions_for_cycle(cycle=cycle)
    messages.success(request, f"Generated {created_count} member contribution rows for {cycle}.")
    return redirect("contributions:member_contributions", cycle_id=cycle.id)

@staff_required
def member_contributions(request, cycle_id):
    cycle = get_object_or_404(ContributionCycle, id=cycle_id)
    rows = (
        MemberContribution.objects
        .select_related("member__user", "cycle")
        .filter(cycle=cycle)
        .order_by("member__member_id")
    )
    return render(request, "contributions/member_contribution_list.html", {"cycle": cycle, "rows": rows})

@staff_required
def payment_create(request, contribution_id):
    contribution = get_object_or_404(MemberContribution, id=contribution_id)
    form = PaymentForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        try:
            record_payment(
                contribution=contribution,
                amount=form.cleaned_data["amount"],
                method=form.cleaned_data["method"],
                recorded_by=request.user,
                reference=form.cleaned_data.get("reference", ""),
            )
            messages.success(request, "Payment recorded.")
            return redirect("contributions:member_contributions", cycle_id=contribution.cycle_id)
        except ValueError as e:
            messages.error(request, str(e))

    return render(request, "contributions/payment_create.html", {"form": form, "contribution": contribution})

@member_required
def member_statement(request):
    mp = request.user.member_profile
    contributions = (
        MemberContribution.objects
        .select_related("cycle")
        .filter(member=mp)
        .order_by("-cycle__year", "-cycle__month")
    )
    ledger_entries = mp.ledger_entries.order_by("-date", "-created_at")

    return render(request, "contributions/member_statement.html", {
        "member": mp,
        "contributions": contributions,
        "ledger_entries": ledger_entries,
    })
