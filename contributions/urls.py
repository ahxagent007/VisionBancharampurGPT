from django.urls import path
from . import views

app_name = "contributions"

urlpatterns = [
    path("cycles/", views.cycle_list, name="cycle_list"),
    path("cycles/new/", views.cycle_create, name="cycle_create"),
    path("cycles/<int:cycle_id>/generate/", views.cycle_generate, name="cycle_generate"),
    path("cycles/<int:cycle_id>/members/", views.member_contributions, name="member_contributions"),

    path("payment/<int:contribution_id>/new/", views.payment_create, name="payment_create"),

    path("my/statement/", views.member_statement, name="member_statement"),
]
