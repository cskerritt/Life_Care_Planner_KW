from django.urls import path
from apps.dashboard import views

app_name = "dashboard"

urlpatterns = [
    path("", views.dashboard, name="dashboard"),
    # Evaluees
    path("evaluees/", views.patient_list, name="evaluee_list"),
    path("evaluees/create/", views.patient_create, name="evaluee_create"),
    path("evaluees/<int:patient_id>/", views.patient_detail, name="evaluee_detail"),
    path("evaluees/<int:patient_id>/edit/", views.patient_edit, name="evaluee_edit"),
    # Life Care Plans
    path("life-care-plans/", views.care_plan_list, name="care_plan_list"),
    path("life-care-plans/create/", views.create_care_plan, name="care_plan_create"),
    path("life-care-plans/<int:plan_id>/", views.care_plan_detail, name="care_plan_detail"),
    path("life-care-plans/<int:plan_id>/edit/", views.care_plan_edit, name="care_plan_edit"),
    path("life-care-plans/<int:plan_id>/export/", views.export_care_plan, name="export_care_plan"),
    # Medical Costs
    path("medical-costs/", views.medical_costs, name="medical_costs"),
    path("life-care-plans/<int:plan_id>/medical-costs/", views.medical_costs, name="care_plan_medical_costs"),
    # Life Expectancy
    path("life-expectancy/", views.life_expectancy, name="life_expectancy"),
    path("life-care-plans/<int:plan_id>/life-expectancy/", views.life_expectancy, name="care_plan_life_expectancy"),
]
