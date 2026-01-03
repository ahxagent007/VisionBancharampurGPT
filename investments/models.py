from django.db import models
from django.conf import settings

class InvestmentProject(models.Model):
    class Type(models.TextChoices):
        LAND = "LAND", "Land"
        PROPERTY = "PROPERTY", "Property"
        BUSINESS = "BUSINESS", "Business"

    class Status(models.TextChoices):
        PLANNED = "PLANNED", "Planned"
        ACTIVE = "ACTIVE", "Active"
        CLOSED = "CLOSED", "Closed"

    name = models.CharField(max_length=120)
    project_type = models.CharField(max_length=20, choices=Type.choices)
    status = models.CharField(max_length=10, choices=Status.choices, default=Status.PLANNED)

    description = models.TextField(blank=True)
    start_date = models.DateField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name="projects_created")

    def __str__(self):
        return f"{self.name} ({self.project_type})"

class Asset(models.Model):
    project = models.ForeignKey(InvestmentProject, on_delete=models.PROTECT, related_name="assets")
    title = models.CharField(max_length=140)

    purchase_date = models.DateField()
    purchase_cost = models.DecimalField(max_digits=14, decimal_places=2)
    current_value = models.DecimalField(max_digits=14, decimal_places=2, null=True, blank=True)

    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name="assets_created")

    def __str__(self):
        return f"{self.title} - {self.purchase_cost}"
