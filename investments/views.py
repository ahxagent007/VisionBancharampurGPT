from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from accounts.decorators import staff_required
from .models import InvestmentProject, Asset
from .forms import ProjectForm, AssetForm
from .services import create_asset_with_ledger

@staff_required
def project_list(request):
    projects = InvestmentProject.objects.order_by("-created_at")
    return render(request, "investments/project_list.html", {"projects": projects})

@staff_required
def project_create(request):
    form = ProjectForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        project = form.save(commit=False)
        project.created_by = request.user
        project.save()
        messages.success(request, "Project created.")
        return redirect("investments:project_list")
    return render(request, "investments/project_form.html", {"form": form, "mode": "create"})

@staff_required
def project_detail(request, project_id):
    project = get_object_or_404(InvestmentProject, id=project_id)
    assets = project.assets.order_by("-purchase_date")
    return render(request, "investments/project_detail.html", {"project": project, "assets": assets})

@staff_required
def asset_create(request):
    form = AssetForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        asset = form.save(commit=False)
        asset.created_by = request.user
        asset.save()
        create_asset_with_ledger(asset_obj=asset, created_by=request.user)
        messages.success(request, "Asset added and ledger updated.")
        return redirect("investments:project_detail", project_id=asset.project_id)
    return render(request, "investments/asset_form.html", {"form": form})
