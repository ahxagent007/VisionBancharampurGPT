from django.contrib import admin
from .models import InvestmentProject, Asset

@admin.register(InvestmentProject)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ("name", "project_type", "status", "start_date", "created_at")
    list_filter = ("project_type", "status")
    search_fields = ("name",)

@admin.register(Asset)
class AssetAdmin(admin.ModelAdmin):
    list_display = ("title", "project", "purchase_cost", "purchase_date")
    list_filter = ("purchase_date", "project__project_type")
    search_fields = ("title", "project__name")
