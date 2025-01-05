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
from django.db import models
from datetime import datetime
import json
from django.http import JsonResponse, HttpResponse
from django.views.decorators.http import require_http_methods
from django.contrib import messages
from .forms import LifeCarePlanForm, CaseManagementForm, EquipmentForm, HomeCareForm, MedicalCareForm, MedicationForm, PatientForm

from apps.api.models import (
    Evaluee, Task, CarePlan, CarePlanItem, CaseManagement, Equipment, HomeCare, MedicalCare, Medication
)

from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView, ListView, CreateView, UpdateView, DeleteView, DetailView
from rest_framework import viewsets
from .serializers import CalendarEventSerializer
from .models import CalendarEvent
from django.core.paginator import Paginator
from django.contrib.auth.models import User

@login_required
def create_care_plan(request):
    """
    Create a new life care plan
    """
    # Check for evaluee_id in GET parameters (from evaluee list)
    initial_evaluee_id = request.GET.get('evaluee_id')
    initial_evaluee = None
    if initial_evaluee_id:
        initial_evaluee = get_object_or_404(Evaluee, id=initial_evaluee_id, user=request.user)

    # Get all evaluees for the dropdown
    evaluees = Evaluee.objects.filter(user=request.user)
    form = LifeCarePlanForm()

    if request.method == "POST":
        form = LifeCarePlanForm(request.POST)
        if form.is_valid():
            evaluee_id = request.POST.get('evaluee_id')
            evaluee = get_object_or_404(Evaluee, id=evaluee_id, user=request.user)
            
            # Create the care plan
            care_plan = CarePlan.objects.create(
                evaluee=evaluee,
                title=f"Life Care Plan for {form.cleaned_data['patient_name']}",
                status='draft'
            )
            
            # Create evaluee details
            evaluee.first_name = form.cleaned_data['patient_name'].split()[0]
            evaluee.last_name = ' '.join(form.cleaned_data['patient_name'].split()[1:])
            evaluee.date_of_birth = form.cleaned_data['date_of_birth']
            evaluee.date_of_injury = form.cleaned_data['date_of_injury']
            evaluee.primary_diagnosis = form.cleaned_data['diagnosis']
            evaluee.medical_history = form.cleaned_data['medical_history']
            evaluee.save()
            
            messages.success(request, _('Life Care Plan created successfully.'))
            return redirect('dashboard:care_plan_edit', plan_id=care_plan.id)
        else:
            messages.error(request, _('Please correct the errors below.'))
    
    return TemplateResponse(
        request,
        "dashboard/care_plan_create.html",
        context={
            "active_tab": "life-care-plans",
            "form": form,
            "evaluees": evaluees,
            "initial_evaluee": initial_evaluee,
        },
    )

@login_required
def evaluee_list(request):
    """
    Display list of all evaluees
    """
    evaluees = Evaluee.objects.filter(user=request.user).order_by('-created_at')
    return TemplateResponse(
        request,
        "dashboard/evaluee_list.html",
        context={
            "active_tab": "evaluees",
            "evaluees": evaluees,
        },
    )

@login_required
def evaluee_create(request):
    """
    Create a new evaluee
    """
    if request.method == "POST":
        evaluee = Evaluee.objects.create(
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
            "active_tab": "evaluees",
        },
    )

@login_required
def evaluee_detail(request, evaluee_id):
    """
    Display detailed view of a specific evaluee
    """
    evaluee = get_object_or_404(Evaluee, id=evaluee_id, user=request.user)
    care_plans = CarePlan.objects.filter(evaluee=evaluee).order_by('-created_at')
    
    return TemplateResponse(
        request,
        "dashboard/evaluee_detail.html",
        context={
            "active_tab": "evaluees",
            "evaluee": evaluee,
            "care_plans": care_plans,
        },
    )

@login_required
def evaluee_edit(request, evaluee_id):
    """
    Edit a specific evaluee
    """
    evaluee = get_object_or_404(Evaluee, id=evaluee_id, user=request.user)
    
    if request.method == "POST":
        evaluee.first_name = request.POST.get('first_name')
        evaluee.last_name = request.POST.get('last_name')
        evaluee.date_of_birth = request.POST.get('date_of_birth')
        evaluee.medical_record_number = request.POST.get('medical_record_number')
        evaluee.primary_diagnosis = request.POST.get('primary_diagnosis')
        evaluee.notes = request.POST.get('notes', '')
        evaluee.save()
        return redirect('dashboard:evaluee_detail', evaluee_id=evaluee_id)
    
    return TemplateResponse(
        request,
        "dashboard/evaluee_edit.html",
        context={
            "active_tab": "evaluees",
            "evaluee": evaluee,
        },
    )

@login_required
def dashboard(request):
    # Get statistics
    total_plans = CarePlan.objects.count()
    active_plans = CarePlan.objects.filter(status='active').count()
    pending_plans = CarePlan.objects.filter(status='in_review').count()
    total_evaluees = Evaluee.objects.count()
    
    # Get recent life care plans
    recent_plans = CarePlan.objects.select_related('evaluee').order_by('-created_at')[:5]
    
    # Get recent activity
    recent_activity = []
    
    # Recent plan creations
    recent_creations = CarePlan.objects.select_related('evaluee').order_by('-created_at')[:3]
    for plan in recent_creations:
        recent_activity.append({
            'type': 'create',
            'description': _('New life care plan created for'),
            'care_plan': plan,
            'created_at': plan.created_at,
        })
    
    # Recent plan updates
    recent_updates = CarePlan.objects.select_related('evaluee').order_by('-updated_at')[:3]
    for plan in recent_updates:
        if plan.updated_at > plan.created_at:  # Only show if it was actually updated
            recent_activity.append({
                'type': 'update',
                'description': _('Life care plan updated for'),
                'care_plan': plan,
                'created_at': plan.updated_at,
            })
    
    # Sort activity by date
    recent_activity.sort(key=lambda x: x['created_at'], reverse=True)
    recent_activity = recent_activity[:5]  # Keep only the 5 most recent activities
    
    context = {
        'total_plans': total_plans,
        'active_plans': active_plans,
        'pending_plans': pending_plans,
        'total_evaluees': total_evaluees,
        'recent_plans': recent_plans,
        'recent_activity': recent_activity,
        'active_tab': 'dashboard',
    }
    
    return render(request, 'dashboard/dashboard.html', context)

@login_required
def export_care_plan(request, plan_id):
    care_plan = get_object_or_404(CarePlan, id=plan_id)
    
    if request.method == 'POST':
        # Get export options
        sections = request.POST.get('sections', '').split(',')
        export_format = request.POST.get('format', 'pdf')
        
        # Create the report
        report_generator = CarePlanReportGenerator(care_plan, sections)
        
        if export_format == 'pdf':
            response = HttpResponse(content_type='application/pdf')
            filename = f'life_care_plan_{care_plan.id}.pdf'
            response['Content-Disposition'] = f'attachment; filename="{filename}"'
            
            # Generate PDF
            report_generator.generate_pdf(response)
            
        else:  # Excel format
            response = HttpResponse(content_type='application/vnd.ms-excel')
            filename = f'life_care_plan_{care_plan.id}.xlsx'
            response['Content-Disposition'] = f'attachment; filename="{filename}"'
            
            # Generate Excel
            report_generator.generate_excel(response)
        
        return response
    
    context = {
        'care_plan': care_plan,
        'active_tab': 'care_plans',
    }
    
    return render(request, 'dashboard/care_plan_export.html', context)

@login_required
@require_http_methods(["GET", "POST"])
def export_care_plan(request, care_plan_id):
    care_plan = get_object_or_404(CarePlan, id=care_plan_id, evaluee__user=request.user)
    
    if request.method == "GET":
        return render(request, 'dashboard/export_report.html', {
            'care_plan': care_plan
        })
    
    # Handle POST request for actual export
    try:
        data = json.loads(request.body)
        sections = data.get('sections', [])
        
        # Create a new Word document
        doc = Document()
        
        # Add title
        doc.add_heading(f'Life Care Plan Report - {care_plan.evaluee.full_name}', 0)
        
        # Add sections based on selection
        if 'patient_info' in sections:
            doc.add_heading('Patient Information', level=1)
            doc.add_paragraph(f'Name: {care_plan.evaluee.full_name}')
            # Add more patient info here
        
        if 'medical_care' in sections:
            doc.add_heading('Medical Care', level=1)
            # Add medical care details
        
        if 'medications' in sections:
            doc.add_heading('Medications', level=1)
            # Add medications details
        
        if 'therapies' in sections:
            doc.add_heading('Therapies', level=1)
            # Add therapies details
        
        if 'equipment' in sections:
            doc.add_heading('Equipment', level=1)
            # Add equipment details
        
        if 'home_care' in sections:
            doc.add_heading('Home Care', level=1)
            # Add home care details
        
        if 'vocational' in sections:
            doc.add_heading('Vocational', level=1)
            # Add vocational details
        
        if 'education' in sections:
            doc.add_heading('Education', level=1)
            # Add education details
        
        if 'cost_projections' in sections:
            doc.add_heading('Cost Projections', level=1)
            # Add cost projections details
        
        # Create the response
        response = HttpResponse(
            content_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document'
        )
        response['Content-Disposition'] = f'attachment; filename=life_care_plan_{care_plan_id}.docx'
        
        # Save the document to the response
        doc.save(response)
        
        return response
        
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@login_required
def care_plan_list(request):
    """
    Display list of all life care plans
    """
    care_plans = CarePlan.objects.filter(
        evaluee__user=request.user
    ).select_related('evaluee').order_by('-created_at')
    
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
    care_plan = get_object_or_404(CarePlan, id=plan_id, evaluee__user=request.user)
    
    # Organize items by category for the tabbed interface
    items = {
        'medical_care': [],
        'medications': [],
        'therapies': [],
        'equipment': []
    }
    
    for item in care_plan.items.all():
        category = item.category.lower()
        if category in items:
            items[category].append(item)
    
    # Add items to care plan object for easy access in template
    care_plan.items = items
    
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
    care_plan = get_object_or_404(CarePlan, id=plan_id, evaluee__user=request.user)
    
    if request.method == "POST":
        # Update basic life care plan info
        care_plan.title = request.POST.get('title')
        care_plan.status = request.POST.get('status')
        care_plan.start_date = request.POST.get('start_date')
        care_plan.end_date = request.POST.get('end_date') or None
        
        # Handle items
        care_plan.items.all().delete()  # Remove existing items
        
        # Get all the arrays from POST
        item_titles = request.POST.getlist('item_title[]')
        item_categories = request.POST.getlist('item_category[]')
        item_descriptions = request.POST.getlist('item_description[]')
        item_frequencies = request.POST.getlist('item_frequency[]')
        item_costs = request.POST.getlist('item_cost[]')
        item_start_dates = request.POST.getlist('item_start_date[]')
        item_end_dates = request.POST.getlist('item_end_date[]')
        item_statuses = request.POST.getlist('item_status[]')
        
        # Create new items
        total_costs = 0
        for i in range(len(item_titles)):
            if item_titles[i]:  # Only create if title exists
                cost = float(item_costs[i] or 0)
                total_costs += cost
                
                CarePlanItem.objects.create(
                    care_plan=care_plan,
                    title=item_titles[i],
                    category=item_categories[i],
                    description=item_descriptions[i],
                    frequency=item_frequencies[i],
                    cost=cost,
                    start_date=item_start_dates[i],
                    end_date=item_end_dates[i] or None,
                    status=item_statuses[i]
                )
        
        # Update care plan costs
        care_plan.total_medical_costs = total_costs
        care_plan.monthly_cost_average = total_costs / 12  # Simple average, could be more sophisticated
        
        care_plan.save()
        return redirect('dashboard:care_plan_detail', plan_id=plan_id)
    
    # Group items by category for display
    items_by_category = {}
    for item in care_plan.items.all():
        category = item.get_category_display()
        if category not in items_by_category:
            items_by_category[category] = []
        items_by_category[category].append(item)
    
    return TemplateResponse(
        request,
        "dashboard/care_plan_edit.html",
        context={
            "active_tab": "life-care-plans",
            "care_plan": care_plan,
            "items_by_category": items_by_category,
            "categories": CarePlanItem.CATEGORY_CHOICES,
        },
    )

@login_required
def medical_costs(request, plan_id=None):
    """
    Medical costs calculator view
    """
    care_plan = None
    if plan_id:
        care_plan = get_object_or_404(CarePlan, id=plan_id, evaluee__user=request.user)
    
    if request.method == "POST" and care_plan:
        # Calculate total costs from all items
        total_costs = care_plan.items.aggregate(models.Sum('cost'))['cost__sum'] or 0
        monthly_costs = total_costs / 12  # Simple average, could be more sophisticated
        
        # Update care plan
        care_plan.total_medical_costs = total_costs
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
        care_plan = get_object_or_404(CarePlan, id=plan_id, evaluee__user=request.user)
    
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
        
        return redirect('dashboard:care_plan_detail', plan_id=plan_id)
    
    return TemplateResponse(
        request,
        "dashboard/life_expectancy.html",
        context={
            "active_tab": "life-expectancy",
            "care_plan": care_plan,
        },
    )

@login_required
def case_management_create(request):
    if request.method == 'POST':
        form = CaseManagementForm(request.POST)
        if form.is_valid():
            case = form.save(commit=False)
            case.save()
            messages.success(request, _('Case management entry created successfully.'))
            return redirect('dashboard:case_management_list')
    else:
        form = CaseManagementForm()
    
    return render(
        request,
        'dashboard/case_management_form.html',
        {
            'form': form,
            'active_tab': 'case_management',
        }
    )

@login_required
def case_management_list(request):
    queryset = CaseManagement.objects.all().select_related('client', 'assigned_to')
    
    # Apply filters
    status = request.GET.get('status')
    priority = request.GET.get('priority')
    assigned_to = request.GET.get('assigned_to')
    
    if status:
        queryset = queryset.filter(status=status)
    if priority:
        queryset = queryset.filter(priority=priority)
    if assigned_to:
        queryset = queryset.filter(assigned_to_id=assigned_to)
    
    # Pagination
    paginator = Paginator(queryset, 10)  # Show 10 cases per page
    page = request.GET.get('page')
    try:
        cases = paginator.page(page)
    except PageNotAnInteger:
        cases = paginator.page(1)
    except EmptyPage:
        cases = paginator.page(paginator.num_pages)
    
    # Get choices for filters
    users = User.objects.filter(is_active=True).order_by('first_name', 'last_name')
    
    context = {
        'cases': cases,
        'active_tab': 'case_management',
        'status_choices': CaseManagement.STATUS_CHOICES,
        'priority_choices': CaseManagement.PRIORITY_CHOICES,
        'users': users,
        'status': status,
        'priority': priority,
        'assigned_to': assigned_to,
        'is_paginated': True,
        'page_obj': cases,
    }
    
    return render(request, 'dashboard/case_management_list.html', context)

@login_required
def case_management_detail(request, case_id):
    case = get_object_or_404(CaseManagement, id=case_id)
    
    return render(
        request,
        'dashboard/case_management_detail.html',
        {
            'case': case,
            'active_tab': 'case_management',
        }
    )

@login_required
def case_management_edit(request, case_id):
    case = get_object_or_404(CaseManagement, id=case_id)
    
    if request.method == 'POST':
        form = CaseManagementForm(request.POST, instance=case)
        if form.is_valid():
            form.save()
            messages.success(request, _('Case management entry updated successfully.'))
            return redirect('dashboard:case_management_detail', case_id=case.id)
    else:
        form = CaseManagementForm(instance=case)
    
    return render(
        request,
        'dashboard/case_management_form.html',
        {
            'form': form,
            'case': case,
            'active_tab': 'case_management',
        }
    )

@login_required
def equipment_create(request, plan_id):
    care_plan = get_object_or_404(CarePlan, id=plan_id)
    
    if request.method == 'POST':
        form = EquipmentForm(request.POST)
        if form.is_valid():
            equipment = form.save(commit=False)
            equipment.care_plan = care_plan
            equipment.save()
            messages.success(request, _('Equipment added successfully.'))
            return redirect('dashboard:care_plan_detail', plan_id=plan_id)
    else:
        form = EquipmentForm()
    
    return render(
        request,
        'dashboard/equipment_form.html',
        {
            'form': form,
            'care_plan': care_plan,
            'active_tab': 'care_plans',
        }
    )

@login_required
def equipment_edit(request, plan_id, equipment_id):
    care_plan = get_object_or_404(CarePlan, id=plan_id)
    equipment = get_object_or_404(Equipment, id=equipment_id, care_plan=care_plan)
    
    if request.method == 'POST':
        form = EquipmentForm(request.POST, instance=equipment)
        if form.is_valid():
            form.save()
            messages.success(request, _('Equipment updated successfully.'))
            return redirect('dashboard:care_plan_detail', plan_id=plan_id)
    else:
        form = EquipmentForm(instance=equipment)
    
    return render(
        request,
        'dashboard/equipment_form.html',
        {
            'form': form,
            'care_plan': care_plan,
            'equipment': equipment,
            'active_tab': 'care_plans',
        }
    )

@login_required
def equipment_delete(request, plan_id, equipment_id):
    care_plan = get_object_or_404(CarePlan, id=plan_id)
    equipment = get_object_or_404(Equipment, id=equipment_id, care_plan=care_plan)
    
    if request.method == 'POST':
        equipment.delete()
        messages.success(request, _('Equipment deleted successfully.'))
        return redirect('dashboard:care_plan_detail', plan_id=plan_id)
    
    return render(
        request,
        'dashboard/equipment_confirm_delete.html',
        {
            'equipment': equipment,
            'care_plan': care_plan,
            'active_tab': 'care_plans',
        }
    )

@login_required
def equipment_list(request):
    # Get filter parameters
    category = request.GET.get('category', '')
    frequency = request.GET.get('frequency', '')
    sort = request.GET.get('sort', 'name')
    
    # Base queryset
    queryset = Equipment.objects.all()
    
    # Apply filters
    if category:
        queryset = queryset.filter(category=category)
    if frequency:
        queryset = queryset.filter(replacement_frequency=frequency)
    
    # Apply sorting
    if sort == 'name':
        queryset = queryset.order_by('name')
    elif sort == 'category':
        queryset = queryset.order_by('category', 'name')
    elif sort == 'cost':
        queryset = queryset.order_by('cost', 'name')
    elif sort == '-created_at':
        queryset = queryset.order_by('-created_at')
    
    # Pagination
    paginator = Paginator(queryset, 10)  # Show 10 items per page
    page = request.GET.get('page')
    try:
        equipment_list = paginator.page(page)
    except PageNotAnInteger:
        equipment_list = paginator.page(1)
    except EmptyPage:
        equipment_list = paginator.page(paginator.num_pages)
    
    context = {
        'equipment_list': equipment_list,
        'category': category,
        'frequency': frequency,
        'sort': sort,
        'category_choices': Equipment.CATEGORY_CHOICES,
        'frequency_choices': Equipment.FREQUENCY_CHOICES,
        'active_tab': 'equipment',
    }
    
    return render(request, 'dashboard/equipment_list.html', context)

@login_required
def home_care_create(request, plan_id):
    care_plan = get_object_or_404(CarePlan, id=plan_id)
    
    if request.method == 'POST':
        form = HomeCareForm(request.POST)
        if form.is_valid():
            home_care = form.save(commit=False)
            home_care.care_plan = care_plan
            home_care.save()
            messages.success(request, _('Home care service added successfully.'))
            return redirect('dashboard:care_plan_detail', plan_id=plan_id)
    else:
        form = HomeCareForm()
    
    return render(
        request,
        'dashboard/home_care_form.html',
        {
            'form': form,
            'care_plan': care_plan,
            'active_tab': 'care_plans',
        }
    )

@login_required
def home_care_edit(request, plan_id, home_care_id):
    care_plan = get_object_or_404(CarePlan, id=plan_id)
    home_care = get_object_or_404(HomeCare, id=home_care_id, care_plan=care_plan)
    
    if request.method == 'POST':
        form = HomeCareForm(request.POST, instance=home_care)
        if form.is_valid():
            form.save()
            messages.success(request, _('Home care service updated successfully.'))
            return redirect('dashboard:care_plan_detail', plan_id=plan_id)
    else:
        form = HomeCareForm(instance=home_care)
    
    return render(
        request,
        'dashboard/home_care_form.html',
        {
            'form': form,
            'care_plan': care_plan,
            'home_care': home_care,
            'active_tab': 'care_plans',
        }
    )

@login_required
def home_care_delete(request, plan_id, home_care_id):
    care_plan = get_object_or_404(CarePlan, id=plan_id)
    home_care = get_object_or_404(HomeCare, id=home_care_id, care_plan=care_plan)
    
    if request.method == 'POST':
        home_care.delete()
        messages.success(request, _('Home care service deleted successfully.'))
        return redirect('dashboard:care_plan_detail', plan_id=plan_id)
    
    return render(
        request,
        'dashboard/home_care_confirm_delete.html',
        {
            'home_care': home_care,
            'care_plan': care_plan,
            'active_tab': 'care_plans',
        }
    )

@login_required
def home_care_list(request):
    # Get filter parameters
    service_type = request.GET.get('service_type', '')
    provider_type = request.GET.get('provider_type', '')
    frequency = request.GET.get('frequency', '')
    sort = request.GET.get('sort', 'service_type')
    
    # Base queryset
    queryset = HomeCare.objects.all()
    
    # Apply filters
    if service_type:
        queryset = queryset.filter(service_type=service_type)
    if provider_type:
        queryset = queryset.filter(provider_type=provider_type)
    if frequency:
        queryset = queryset.filter(frequency=frequency)
    
    # Apply sorting
    if sort == 'service_type':
        queryset = queryset.order_by('service_type', 'provider_name')
    elif sort == 'provider_name':
        queryset = queryset.order_by('provider_name', 'service_type')
    elif sort == 'monthly_cost':
        # Note: This might need to be adjusted based on your specific needs
        queryset = queryset.order_by('-rate_per_hour', '-hours_per_visit')
    elif sort == '-created_at':
        queryset = queryset.order_by('-created_at')
    
    # Pagination
    paginator = Paginator(queryset, 10)  # Show 10 items per page
    page = request.GET.get('page')
    try:
        home_care_list = paginator.page(page)
    except PageNotAnInteger:
        home_care_list = paginator.page(1)
    except EmptyPage:
        home_care_list = paginator.page(paginator.num_pages)
    
    context = {
        'home_care_list': home_care_list,
        'service_type': service_type,
        'provider_type': provider_type,
        'frequency': frequency,
        'sort': sort,
        'service_type_choices': HomeCare.SERVICE_TYPE_CHOICES,
        'provider_type_choices': HomeCare.PROVIDER_TYPE_CHOICES,
        'frequency_choices': HomeCare.FREQUENCY_CHOICES,
        'active_tab': 'home_care',
    }
    
    return render(request, 'dashboard/home_care_list.html', context)

@login_required
def medical_care_create(request, plan_id):
    care_plan = get_object_or_404(CarePlan, id=plan_id)
    
    if request.method == 'POST':
        form = MedicalCareForm(request.POST)
        if form.is_valid():
            medical_care = form.save(commit=False)
            medical_care.care_plan = care_plan
            medical_care.save()
            messages.success(request, _('Medical care entry added successfully.'))
            return redirect('dashboard:care_plan_detail', plan_id=plan_id)
    else:
        form = MedicalCareForm()
    
    context = {
        'form': form,
        'care_plan': care_plan,
        'active_tab': 'care_plans',
    }
    
    return render(request, 'dashboard/medical_care_form.html', context)

@login_required
def medical_care_edit(request, plan_id, medical_care_id):
    care_plan = get_object_or_404(CarePlan, id=plan_id)
    medical_care = get_object_or_404(MedicalCare, id=medical_care_id, care_plan=care_plan)
    
    if request.method == 'POST':
        form = MedicalCareForm(request.POST, instance=medical_care)
        if form.is_valid():
            form.save()
            messages.success(request, _('Medical care entry updated successfully.'))
            return redirect('dashboard:care_plan_detail', plan_id=plan_id)
    else:
        form = MedicalCareForm(instance=medical_care)
    
    context = {
        'form': form,
        'care_plan': care_plan,
        'medical_care': medical_care,
        'active_tab': 'care_plans',
    }
    
    return render(request, 'dashboard/medical_care_form.html', context)

@login_required
def medical_care_delete(request, plan_id, medical_care_id):
    care_plan = get_object_or_404(CarePlan, id=plan_id)
    medical_care = get_object_or_404(MedicalCare, id=medical_care_id, care_plan=care_plan)
    
    if request.method == 'POST':
        medical_care.delete()
        messages.success(request, _('Medical care entry deleted successfully.'))
        return redirect('dashboard:care_plan_detail', plan_id=plan_id)
    
    context = {
        'medical_care': medical_care,
        'care_plan': care_plan,
        'active_tab': 'care_plans',
    }
    
    return render(request, 'dashboard/medical_care_confirm_delete.html', context)

@login_required
def medical_care_list(request, plan_id):
    care_plan = get_object_or_404(CarePlan, id=plan_id)
    
    # Get filter parameters
    care_type = request.GET.get('care_type', '')
    provider_specialty = request.GET.get('provider_specialty', '')
    frequency = request.GET.get('frequency', '')
    sort = request.GET.get('sort', 'care_type')
    
    # Build queryset
    queryset = MedicalCare.objects.filter(care_plan=care_plan)
    
    if care_type:
        queryset = queryset.filter(care_type=care_type)
    if provider_specialty:
        queryset = queryset.filter(provider_specialty=provider_specialty)
    if frequency:
        queryset = queryset.filter(frequency=frequency)
    
    # Apply sorting
    if sort.startswith('-'):
        queryset = queryset.order_by(sort)
    else:
        queryset = queryset.order_by(sort)
    
    # Get unique provider specialties for filter dropdown
    provider_specialties = MedicalCare.objects.filter(care_plan=care_plan).values_list('provider_specialty', flat=True).distinct()
    
    # Pagination
    paginator = Paginator(queryset, 10)  # Show 10 items per page
    page = request.GET.get('page')
    medical_care_list = paginator.get_page(page)
    
    context = {
        'medical_care_list': medical_care_list,
        'care_plan': care_plan,
        'active_tab': 'care_plans',
        'care_type': care_type,
        'provider_specialty': provider_specialty,
        'frequency': frequency,
        'sort': sort,
        'care_type_choices': MedicalCare.CARE_TYPE_CHOICES,
        'frequency_choices': MedicalCare.FREQUENCY_CHOICES,
        'provider_specialties': provider_specialties,
    }
    
    return render(request, 'dashboard/medical_care_list.html', context)

@login_required
def medication_create(request, plan_id):
    care_plan = get_object_or_404(CarePlan, id=plan_id)
    
    if request.method == 'POST':
        form = MedicationForm(request.POST)
        if form.is_valid():
            medication = form.save(commit=False)
            medication.care_plan = care_plan
            medication.save()
            messages.success(request, _('Medication added successfully.'))
            return redirect('dashboard:care_plan_detail', plan_id=plan_id)
    else:
        form = MedicationForm()
    
    context = {
        'form': form,
        'care_plan': care_plan,
        'active_tab': 'care_plans',
    }
    
    return render(request, 'dashboard/medication_form.html', context)

@login_required
def medication_edit(request, plan_id, medication_id):
    care_plan = get_object_or_404(CarePlan, id=plan_id)
    medication = get_object_or_404(Medication, id=medication_id, care_plan=care_plan)
    
    if request.method == 'POST':
        form = MedicationForm(request.POST, instance=medication)
        if form.is_valid():
            form.save()
            messages.success(request, _('Medication updated successfully.'))
            return redirect('dashboard:care_plan_detail', plan_id=plan_id)
    else:
        form = MedicationForm(instance=medication)
    
    context = {
        'form': form,
        'care_plan': care_plan,
        'medication': medication,
        'active_tab': 'care_plans',
    }
    
    return render(request, 'dashboard/medication_form.html', context)

@login_required
def medication_delete(request, plan_id, medication_id):
    care_plan = get_object_or_404(CarePlan, id=plan_id)
    medication = get_object_or_404(Medication, id=medication_id, care_plan=care_plan)
    
    if request.method == 'POST':
        medication.delete()
        messages.success(request, _('Medication deleted successfully.'))
        return redirect('dashboard:care_plan_detail', plan_id=plan_id)
    
    context = {
        'medication': medication,
        'care_plan': care_plan,
        'active_tab': 'care_plans',
    }
    
    return render(request, 'dashboard/medication_confirm_delete.html', context)

@login_required
def medication_list(request, plan_id):
    care_plan = get_object_or_404(CarePlan, id=plan_id)
    
    # Get filter parameters
    search = request.GET.get('search', '')
    frequency = request.GET.get('frequency', '')
    route = request.GET.get('route', '')
    sort = request.GET.get('sort', 'name')
    
    # Build queryset
    queryset = Medication.objects.filter(care_plan=care_plan)
    
    if search:
        queryset = queryset.filter(
            Q(name__icontains=search) |
            Q(generic_name__icontains=search) |
            Q(prescribing_doctor__icontains=search)
        )
    if frequency:
        queryset = queryset.filter(frequency=frequency)
    if route:
        queryset = queryset.filter(route=route)
    
    # Apply sorting
    if sort.startswith('-'):
        queryset = queryset.order_by(sort)
    else:
        queryset = queryset.order_by(sort)
    
    # Pagination
    paginator = Paginator(queryset, 10)  # Show 10 items per page
    page = request.GET.get('page')
    medications = paginator.get_page(page)
    
    context = {
        'medications': medications,
        'care_plan': care_plan,
        'active_tab': 'care_plans',
        'search': search,
        'frequency': frequency,
        'route': route,
        'sort': sort,
        'frequency_choices': Medication.FREQUENCY_CHOICES,
        'route_choices': Medication.ROUTE_CHOICES,
    }
    
    return render(request, 'dashboard/medication_list.html', context)

class CalendarView(LoginRequiredMixin, TemplateView):
    template_name = 'dashboard/calendar.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['active_tab'] = 'calendar'
        return context

class CalendarEventViewSet(viewsets.ModelViewSet):
    serializer_class = CalendarEventSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return CalendarEvent.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class PatientListView(LoginRequiredMixin, ListView):
    model = Patient
    template_name = 'dashboard/patient_list.html'
    context_object_name = 'patients'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        search_query = self.request.GET.get('q')

        if search_query:
            queryset = queryset.filter(
                Q(first_name__icontains=search_query) |
                Q(last_name__icontains=search_query) |
                Q(email__icontains=search_query) |
                Q(phone_primary__icontains=search_query)
            )

        sort_by = self.request.GET.get('sort', 'last_name')
        sort_order = self.request.GET.get('order', 'asc')

        if sort_order == 'desc':
            sort_by = f'-{sort_by}'

        return queryset.order_by(sort_by)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_query'] = self.request.GET.get('q', '')
        context['sort_by'] = self.request.GET.get('sort', 'last_name')
        context['sort_order'] = self.request.GET.get('order', 'asc')
        return context


class PatientCreateView(LoginRequiredMixin, CreateView):
    model = Patient
    form_class = PatientForm
    template_name = 'dashboard/patient_form.html'
    success_url = reverse_lazy('dashboard:patient_list')

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        form.instance.updated_by = self.request.user
        messages.success(self.request, _('Patient added successfully.'))
        return super().form_valid(form)


class PatientUpdateView(LoginRequiredMixin, UpdateView):
    model = Patient
    form_class = PatientForm
    template_name = 'dashboard/patient_form.html'
    success_url = reverse_lazy('dashboard:patient_list')

    def form_valid(self, form):
        form.instance.updated_by = self.request.user
        messages.success(self.request, _('Patient updated successfully.'))
        return super().form_valid(form)


class PatientDeleteView(LoginRequiredMixin, DeleteView):
    model = Patient
    template_name = 'dashboard/patient_confirm_delete.html'
    success_url = reverse_lazy('dashboard:patient_list')

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, _('Patient deleted successfully.'))
        return super().delete(request, *args, **kwargs)


class PatientDetailView(LoginRequiredMixin, DetailView):
    model = Patient
    template_name = 'dashboard/patient_detail.html'
    context_object_name = 'patient'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        patient = self.get_object()
        context['medications'] = patient.medication_set.all()
        context['medical_care'] = patient.medicalcare_set.all()
        context['home_care'] = patient.homecare_set.all()
        context['equipment'] = patient.equipment_set.all()
        return context
