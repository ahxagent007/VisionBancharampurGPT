from django.urls import path
from . import views

app_name = "investments"

urlpatterns = [
    path("", views.project_list, name="project_list"),
    path("new/", views.project_create, name="project_create"),
    path("<int:project_id>/", views.project_detail, name="project_detail"),
    path("assets/new/", views.asset_create, name="asset_create"),
]
