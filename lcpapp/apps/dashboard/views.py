from datetime import datetime, timedelta
import os
from docx import Document
from docx.shared import Inches

from django.contrib.auth.decorators import login_required
from django.template.response import TemplateResponse
from django.utils import timezone
from django.shortcuts import get_object_or_404, redirect, render
from django.http import Http404, HttpResponse, JsonResponse
from django.urls import reverse
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.utils.text import slugify
from datetime import datetime


from apps.api.models import (
    Patient, Task, CarePlan, MedicalRecord,
    MedicalRequirement, Treatment
)


@login_required
def create_care_plan(request):
    """
    Create a new life care plan
    """
    # Check for patient_id in GET parameters (from evaluee list)
    initial_patient_id = request.GET.get('patient_id')
    initial_patient = None
    if initial_patient_id:
        initial_patient = get_object_or_404(Patient, id=initial_patient_id, user=request.user)

    if request.method == "POST":
        patient_id = request.POST.get('patient_id')
        title = request.POST.get('title', 'New Life Care Plan')
        
        patient = get_object_or_404(Patient, id=patient_id, user=request.user)
        care_plan = CarePlan.objects.create(
            patient=patient,
            title=title,
            description="",
            start_date=timezone.now().date(),
            status='draft'
        )
        return redirect('dashboard:care_plan_edit', plan_id=care_plan.id)
    
    # Get list of evaluees for selection
    patients = Patient.objects.filter(user=request.user)
    return TemplateResponse(
        request,
        "dashboard/care_plan_create.html",
        context={
            "active_tab": "life-care-plans",
            "patients": patients,
            "initial_patient": initial_patient,
        },
    )

@login_required
def patient_list(request):
    """
    Display list of all evaluees
    """
    patients = Patient.objects.filter(user=request.user).order_by('-created_at')
    return TemplateResponse(
        request,
        "dashboard/evaluee_list.html",
        context={
            "active_tab": "patients",
            "patients": patients,
        },
    )

@login_required
def patient_create(request):
    """
    Create a new evaluee
    """
    if request.method == "POST":
        patient = Patient.objects.create(
            user=request.user,
            first_name=request.POST.get('first_name'),
            last_name=request.POST.get('last_name'),
            date_of_birth=request.POST.get('date_of_birth'),
            medical_record_number=request.POST.get('medical_record_number'),
            primary_diagnosis=request.POST.get('primary_diagnosis'),
            notes=request.POST.get('notes', '')
        )
        return redirect('dashboard:evaluee_list')
    
    return TemplateResponse(
        request,
        "dashboard/evaluee_create.html",
        context={
            "active_tab": "patients",
        },
    )

@login_required
def patient_detail(request, patient_id):
    """
    Display detailed view of a specific evaluee
    """
    patient = get_object_or_404(Patient, id=patient_id, user=request.user)
    care_plans = CarePlan.objects.filter(patient=patient).order_by('-created_at')
    
    return TemplateResponse(
        request,
        "dashboard/evaluee_detail.html",
        context={
            "active_tab": "patients",
            "patient": patient,
            "care_plans": care_plans,
        },
    )

@login_required
def patient_edit(request, patient_id):
    """
    Edit a specific evaluee
    """
    patient = get_object_or_404(Patient, id=patient_id, user=request.user)
    
    if request.method == "POST":
        patient.first_name = request.POST.get('first_name')
        patient.last_name = request.POST.get('last_name')
        patient.date_of_birth = request.POST.get('date_of_birth')
        patient.medical_record_number = request.POST.get('medical_record_number')
        patient.primary_diagnosis = request.POST.get('primary_diagnosis')
        patient.notes = request.POST.get('notes', '')
        patient.save()
        return redirect('dashboard:evaluee_detail', patient_id=patient_id)
    
    return TemplateResponse(
        request,
        "dashboard/evaluee_edit.html",
        context={
            "active_tab": "patients",
            "patient": patient,
        },
    )

@login_required
def dashboard(request):
    """
    Main dashboard view showing overview of evaluees and life care plans
    """
    # Get current user's evaluees
    patients = Patient.objects.filter(user=request.user)
    
    # Get upcoming tasks across all life care plans
    upcoming_tasks = Task.objects.filter(
        care_plan__patient__user=request.user,
        status__in=['pending', 'in_progress'],
        due_date__gte=timezone.now()
    ).order_by('due_date')[:5]
    
    # Get active life care plans
    active_care_plans = CarePlan.objects.filter(
        patient__user=request.user,
        status='active'
    ).order_by('-updated_at')[:5]
    
    # Get recent medical records
    recent_records = MedicalRecord.objects.filter(
        patient__user=request.user
    ).order_by('-date_of_record')[:5]
    
    # Get tasks due today
    today = timezone.now().date()
    tasks_due_today = Task.objects.filter(
        care_plan__patient__user=request.user,
        status__in=['pending', 'in_progress'],
        due_date__date=today
    ).order_by('due_date')
    
    # Get overdue tasks
    overdue_tasks = Task.objects.filter(
        care_plan__patient__user=request.user,
        status__in=['pending', 'in_progress'],
        due_date__lt=timezone.now()
    ).order_by('due_date')
    
    # Calculate task statistics
    total_tasks = Task.objects.filter(care_plan__patient__user=request.user).count()
    completed_tasks = Task.objects.filter(
        care_plan__patient__user=request.user,
        status='completed'
    ).count()
    completion_rate = (completed_tasks / total_tasks * 100) if total_tasks > 0 else 0
    
    return TemplateResponse(
        request,
        "dashboard/user_dashboard.html",
        context={
            "active_tab": "dashboard",
            "patients": patients,
            "upcoming_tasks": upcoming_tasks,
            "active_care_plans": active_care_plans,
            "recent_records": recent_records,
            "tasks_due_today": tasks_due_today,
            "overdue_tasks": overdue_tasks,
            "total_tasks": total_tasks,
            "completed_tasks": completed_tasks,
            "completion_rate": round(completion_rate, 1),
        },
    )


@login_required
def export_care_plan(request, plan_id):
    """
    Export life care plan details to Word document
    """
    care_plan = get_object_or_404(CarePlan, id=plan_id, patient__user=request.user)
    
    # Create Word document
    doc = Document()
    doc.add_heading(f'Life Care Plan: {care_plan.title}', 0)
    
    # Evaluee Information
    doc.add_heading('Evaluee Information', level=1)
    doc.add_paragraph(f'Name: {care_plan.patient.first_name} {care_plan.patient.last_name}')
    doc.add_paragraph(f'Medical Record Number: {care_plan.patient.medical_record_number}')
    doc.add_paragraph(f'Primary Diagnosis: {care_plan.patient.primary_diagnosis}')
    
    # Plan Details
    doc.add_heading('Plan Details', level=1)
    doc.add_paragraph(f'Status: {care_plan.get_status_display()}')
    doc.add_paragraph(f'Start Date: {care_plan.start_date}')
    if care_plan.end_date:
        doc.add_paragraph(f'End Date: {care_plan.end_date}')
    
    # Medical Requirements
    doc.add_heading('Medical Requirements', level=1)
    for req in care_plan.medical_requirements.all():
        doc.add_paragraph(f'• {req.title} ({req.get_category_display()})')
        doc.add_paragraph(f'  Description: {req.description}')
        doc.add_paragraph(f'  Frequency: {req.frequency}')
    
    # Treatment Timeline
    doc.add_heading('Treatment Timeline', level=1)
    for treatment in care_plan.treatments.all():
        doc.add_paragraph(f'• {treatment.title} - {treatment.get_status_display()}')
        doc.add_paragraph(f'  Date: {treatment.date}')
        doc.add_paragraph(f'  Description: {treatment.description}')
    
    # Medical Costs
    doc.add_heading('Medical Costs Summary', level=1)
    doc.add_paragraph(f'Total Medical Costs: ${care_plan.total_medical_costs:,.2f}')
    doc.add_paragraph(f'Monthly Cost Average: ${care_plan.monthly_cost_average:,.2f}')
    
    # Life Expectancy
    if care_plan.life_expectancy:
        doc.add_heading('Life Expectancy Estimate', level=1)
        doc.add_paragraph(f'Estimated Years: {care_plan.life_expectancy}')
    
    # Save to temporary file and serve
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document')
    response['Content-Disposition'] = f'attachment; filename=life_care_plan_{plan_id}.docx'
    doc.save(response)
    
    return response

@login_required
def care_plan_list(request):
    """
    Display list of all life care plans
    """
    care_plans = CarePlan.objects.filter(
        patient__user=request.user
    ).select_related('patient').order_by('-created_at')
    
    return TemplateResponse(
        request,
        "dashboard/care_plan_list.html",
        context={
            "active_tab": "life-care-plans",
            "care_plans": care_plans,
        },
    )

@login_required
def care_plan_detail(request, plan_id):
    """
    Display detailed view of a specific life care plan
    """
    care_plan = get_object_or_404(CarePlan, id=plan_id, patient__user=request.user)
    
    return TemplateResponse(
        request,
        "dashboard/care_plan_detail.html",
        context={
            "active_tab": "life-care-plans",
            "care_plan": care_plan,
        },
    )

@login_required
def care_plan_edit(request, plan_id):
    """
    Edit a specific life care plan
    """
    care_plan = get_object_or_404(CarePlan, id=plan_id, patient__user=request.user)
    
    if request.method == "POST":
        # Update basic life care plan info
        care_plan.title = request.POST.get('title')
        care_plan.status = request.POST.get('status')
        care_plan.start_date = request.POST.get('start_date')
        care_plan.end_date = request.POST.get('end_date') or None
        
        # Handle medical requirements
        care_plan.medical_requirements.all().delete()  # Remove existing requirements
        requirement_titles = request.POST.getlist('requirement_title[]')
        requirement_categories = request.POST.getlist('requirement_category[]')
        requirement_descriptions = request.POST.getlist('requirement_description[]')
        requirement_frequencies = request.POST.getlist('requirement_frequency[]')
        
        for i in range(len(requirement_titles)):
            if requirement_titles[i]:  # Only create if title exists
                MedicalRequirement.objects.create(
                    care_plan=care_plan,
                    title=requirement_titles[i],
                    category=requirement_categories[i],
                    description=requirement_descriptions[i],
                    frequency=requirement_frequencies[i]
                )
        
        # Handle treatments
        care_plan.treatments.all().delete()  # Remove existing treatments
        treatment_titles = request.POST.getlist('treatment_title[]')
        treatment_statuses = request.POST.getlist('treatment_status[]')
        treatment_descriptions = request.POST.getlist('treatment_description[]')
        treatment_dates = request.POST.getlist('treatment_date[]')
        
        for i in range(len(treatment_titles)):
            if treatment_titles[i]:  # Only create if title exists
                Treatment.objects.create(
                    care_plan=care_plan,
                    title=treatment_titles[i],
                    status=treatment_statuses[i],
                    description=treatment_descriptions[i],
                    date=treatment_dates[i]
                )
        
        care_plan.save()
        return redirect('dashboard:care_plan_detail', plan_id=plan_id)
    
    return TemplateResponse(
        request,
        "dashboard/care_plan_edit.html",
        context={
            "active_tab": "life-care-plans",
            "care_plan": care_plan,
        },
    )

@login_required
def medical_costs(request, plan_id=None):
    """
    Medical costs calculator view
    """
    care_plan = None
    if plan_id:
        care_plan = get_object_or_404(CarePlan, id=plan_id, patient__user=request.user)
    
    if request.method == "POST" and care_plan:
        # Calculate and save costs
        emergency_cost = float(request.POST.get('emergency_cost', 0))
        hospital_cost = float(request.POST.get('hospital_cost', 0))
        medication_cost = float(request.POST.get('medication_cost', 0))
        therapy_cost = float(request.POST.get('therapy_cost', 0))
        equipment_cost = float(request.POST.get('equipment_cost', 0))
        supplies_cost = float(request.POST.get('supplies_cost', 0))
        
        # Calculate totals
        one_time_costs = emergency_cost + hospital_cost + equipment_cost
        monthly_costs = medication_cost + (therapy_cost * 4) + supplies_cost
        annual_costs = monthly_costs * 12
        
        # Update care plan
        care_plan.total_medical_costs = one_time_costs + annual_costs
        care_plan.monthly_cost_average = monthly_costs
        care_plan.save()
        
        return redirect('dashboard:care_plan_detail', plan_id=plan_id)
    
    return TemplateResponse(
        request,
        "dashboard/medical_costs.html",
        context={
            "active_tab": "medical-costs",
            "care_plan": care_plan,
        },
    )

@login_required
def life_expectancy(request, plan_id=None):
    """
    Life expectancy calculator view
    """
    care_plan = None
    if plan_id:
        care_plan = get_object_or_404(CarePlan, id=plan_id, patient__user=request.user)
    
    if request.method == "POST" and care_plan:
        # Calculate life expectancy
        age = int(request.POST.get('age', 0))
        gender = request.POST.get('gender')
        smoking = request.POST.get('smoking')
        activity = request.POST.get('activity')
        parents_age = int(request.POST.get('parents_age', 0))
        grandparents_age = int(request.POST.get('grandparents_age', 0))
        
        # Base life expectancy
        base_expectancy = 81 if gender == 'female' else 76
        
        # Health impact
        health_impact = 0
        if request.POST.get('condition_diabetes'): health_impact -= 5
        if request.POST.get('condition_heart'): health_impact -= 7
        if request.POST.get('condition_cancer'): health_impact -= 8
        if request.POST.get('condition_respiratory'): health_impact -= 6
        
        # Lifestyle impact
        lifestyle_impact = 0
        if smoking == 'current': lifestyle_impact -= 10
        elif smoking == 'former': lifestyle_impact -= 5
        
        if activity == 'active': lifestyle_impact += 5
        elif activity == 'sedentary': lifestyle_impact -= 3
        
        # Genetic impact
        genetic_impact = 0
        if parents_age and grandparents_age:
            family_longevity = (parents_age + grandparents_age) / 2
            genetic_impact = 5 if family_longevity > 80 else (2 if family_longevity > 70 else -2)
        
        # Calculate final estimate
        estimate = max(age + 1, base_expectancy + health_impact + lifestyle_impact + genetic_impact)
        
        # Update care plan
        care_plan.life_expectancy = round(estimate)
        care_plan.save()
        
        return redirect('dashboard:life_care_plan_detail', plan_id=plan_id)
    
    return TemplateResponse(
        request,
        "dashboard/life_expectancy.html",
        context={
            "active_tab": "life-expectancy",
            "care_plan": care_plan,
        },
    )
