from django import forms
from .models import InvestmentProject, Asset

class ProjectForm(forms.ModelForm):
    class Meta:
        model = InvestmentProject
        fields = ["name", "project_type", "status", "description", "start_date"]

class AssetForm(forms.ModelForm):
    class Meta:
        model = Asset
        fields = ["project", "title", "purchase_date", "purchase_cost", "current_value", "notes"]
