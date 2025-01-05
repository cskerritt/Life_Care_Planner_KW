from django.urls import path, include
from rest_framework import routers
from apps.dashboard import views
from apps.dashboard.api import CalendarEventViewSet
from apps.dashboard.views import CalendarView

app_name = "dashboard"

router = routers.DefaultRouter()
router.register(r'calendar/events', CalendarEventViewSet, basename='calendar-event')

urlpatterns = [
    path("", views.dashboard, name="dashboard"),
    # Evaluees
    path("evaluees/", views.evaluee_list, name="evaluee_list"),
    path("evaluees/create/", views.evaluee_create, name="evaluee_create"),
    path("evaluees/<int:evaluee_id>/", views.evaluee_detail, name="evaluee_detail"),
    path("evaluees/<int:evaluee_id>/edit/", views.evaluee_edit, name="evaluee_edit"),
    # Life Care Plans
    path("life-care-plans/", views.care_plan_list, name="care_plan_list"),
    path("life-care-plans/create/", views.create_care_plan, name="care_plan_create"),
    path("life-care-plans/<int:plan_id>/", views.care_plan_detail, name="care_plan_detail"),
    path("life-care-plans/<int:plan_id>/edit/", views.care_plan_edit, name="care_plan_edit"),
    # Export URLs
    path('care-plan/<int:plan_id>/export/', views.export_care_plan, name='export_care_plan'),
    # Equipment URLs
    path('equipment/', views.equipment_list, name='equipment_list'),
    path('equipment/add/', views.equipment_create, name='equipment_create'),
    path('equipment/<int:equipment_id>/edit/', views.equipment_edit, name='equipment_edit'),
    path('equipment/<int:equipment_id>/delete/', views.equipment_delete, name='equipment_delete'),
    path('care-plan/<int:plan_id>/equipment/add/', views.equipment_create, name='equipment_create'),
    path('care-plan/<int:plan_id>/equipment/<int:equipment_id>/edit/', views.equipment_edit, name='equipment_edit'),
    path('care-plan/<int:plan_id>/equipment/<int:equipment_id>/delete/', views.equipment_delete, name='equipment_delete'),
    # Home Care URLs
    path('home-care/', views.home_care_list, name='home_care_list'),
    path('home-care/add/', views.home_care_create, name='home_care_create'),
    path('home-care/<int:home_care_id>/edit/', views.home_care_edit, name='home_care_edit'),
    path('home-care/<int:home_care_id>/delete/', views.home_care_delete, name='home_care_delete'),
    path('care-plan/<int:plan_id>/home-care/add/', views.home_care_create, name='home_care_create'),
    path('care-plan/<int:plan_id>/home-care/<int:home_care_id>/edit/', views.home_care_edit, name='home_care_edit'),
    path('care-plan/<int:plan_id>/home-care/<int:home_care_id>/delete/', views.home_care_delete, name='home_care_delete'),
    # Medical Costs
    path("medical-costs/", views.medical_costs, name="medical_costs"),
    path("life-care-plans/<int:plan_id>/medical-costs/", views.medical_costs, name="care_plan_medical_costs"),
    # Medical Care URLs
    path('care-plan/<int:plan_id>/medical-care/', views.medical_care_list, name='medical_care_list'),
    path('care-plan/<int:plan_id>/medical-care/add/', views.medical_care_create, name='medical_care_create'),
    path('care-plan/<int:plan_id>/medical-care/<int:medical_care_id>/edit/', views.medical_care_edit, name='medical_care_edit'),
    path('care-plan/<int:plan_id>/medical-care/<int:medical_care_id>/delete/', views.medical_care_delete, name='medical_care_delete'),
    # Medication URLs
    path('care-plan/<int:plan_id>/medications/', views.medication_list, name='medication_list'),
    path('care-plan/<int:plan_id>/medications/add/', views.medication_create, name='medication_create'),
    path('care-plan/<int:plan_id>/medications/<int:medication_id>/edit/', views.medication_edit, name='medication_edit'),
    path('care-plan/<int:plan_id>/medications/<int:medication_id>/delete/', views.medication_delete, name='medication_delete'),
    # Life Expectancy
    path("life-expectancy/", views.life_expectancy, name="life_expectancy"),
    path("life-care-plans/<int:plan_id>/life-expectancy/", views.life_expectancy, name="care_plan_life_expectancy"),
    # Case Management
    path('case-management/', views.case_management_list, name='case_management_list'),
    path('case-management/create/', views.case_management_create, name='case_management_create'),
    path('case-management/<int:case_id>/', views.case_management_detail, name='case_management_detail'),
    path('case-management/<int:case_id>/edit/', views.case_management_edit, name='case_management_edit'),
    # Patient Management
    path('patients/', views.PatientListView.as_view(), name='patient_list'),
    path('patients/create/', views.PatientCreateView.as_view(), name='patient_create'),
    path('patients/<int:pk>/', views.PatientDetailView.as_view(), name='patient_detail'),
    path('patients/<int:pk>/edit/', views.PatientUpdateView.as_view(), name='patient_update'),
    path('patients/<int:pk>/delete/', views.PatientDeleteView.as_view(), name='patient_delete'),
    path('calendar/', CalendarView.as_view(), name='calendar'),
    path('api/', include(router.urls)),
]
