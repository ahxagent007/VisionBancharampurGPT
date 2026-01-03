from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),

    path("", include("accounts.urls")),
    path("contributions/", include("contributions.urls")),
    path("reports/", include("reports.urls")),
    path("investments/", include("investments.urls")),
    path("expenses/", include("expenses.urls")),

]
