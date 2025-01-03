from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.utils import timezone
from datetime import timedelta
from apps.api.models import (
    Patient, CarePlan, MedicalRequirement, Treatment
)

User = get_user_model()

class Command(BaseCommand):
    help = 'Creates sample data for testing the care plan functionality'

    def handle(self, *args, **kwargs):
        # Create test user if not exists
        user, created = User.objects.get_or_create(
            username='demo',
            email='demo@example.com',
            defaults={'is_staff': True}
        )
        if created:
            user.set_password('demo123')
            user.save()
            self.stdout.write(self.style.SUCCESS('Created demo user'))

        # Create sample patients
        patients = [
            {
                'first_name': 'John',
                'last_name': 'Smith',
                'date_of_birth': '1955-05-15',
                'medical_record_number': 'MRN001',
                'primary_diagnosis': 'Type 2 Diabetes with Cardiovascular Complications',
            },
            {
                'first_name': 'Sarah',
                'last_name': 'Johnson',
                'date_of_birth': '1962-08-23',
                'medical_record_number': 'MRN002',
                'primary_diagnosis': 'Early-stage Alzheimer\'s Disease',
            },
            {
                'first_name': 'Michael',
                'last_name': 'Chen',
                'date_of_birth': '1978-11-30',
                'medical_record_number': 'MRN003',
                'primary_diagnosis': 'Spinal Cord Injury - T6 Complete',
            }
        ]

        created_patients = []
        for patient_data in patients:
            patient, created = Patient.objects.get_or_create(
                user=user,
                medical_record_number=patient_data['medical_record_number'],
                defaults=patient_data
            )
            created_patients.append(patient)
            if created:
                self.stdout.write(self.style.SUCCESS(f'Created patient: {patient}'))

        # Create care plans with different scenarios
        care_plans = [
            {
                'patient': created_patients[0],
                'title': 'Diabetes Management Plan',
                'description': 'Comprehensive care plan for managing diabetes and cardiovascular health',
                'status': 'active',
                'total_medical_costs': 25000.00,
                'monthly_cost_average': 1200.00,
                'life_expectancy': 78,
                'requirements': [
                    {
                        'title': 'Blood Sugar Monitoring',
                        'category': 'equipment',
                        'description': 'Daily blood glucose monitoring with CGM device',
                        'frequency': 'Continuous monitoring with 2x daily checks'
                    },
                    {
                        'title': 'Insulin Management',
                        'category': 'medication',
                        'description': 'Long-acting and meal-time insulin administration',
                        'frequency': '3-4 times daily'
                    }
                ],
                'treatments': [
                    {
                        'title': 'Diabetes Education Program',
                        'description': 'Comprehensive diabetes management training',
                        'date': timezone.now().date(),
                        'status': 'completed'
                    },
                    {
                        'title': 'Cardiology Follow-up',
                        'description': 'Regular heart health monitoring',
                        'date': timezone.now().date() + timedelta(days=30),
                        'status': 'scheduled'
                    }
                ]
            },
            {
                'patient': created_patients[1],
                'title': 'Alzheimer\'s Care Plan',
                'description': 'Early intervention and support plan for Alzheimer\'s management',
                'status': 'active',
                'total_medical_costs': 35000.00,
                'monthly_cost_average': 2500.00,
                'life_expectancy': 75,
                'requirements': [
                    {
                        'title': 'Cognitive Therapy',
                        'category': 'therapy',
                        'description': 'Regular cognitive stimulation therapy sessions',
                        'frequency': 'Twice weekly'
                    },
                    {
                        'title': 'Memory Medications',
                        'category': 'medication',
                        'description': 'Prescribed medications for memory support',
                        'frequency': 'Daily'
                    }
                ],
                'treatments': [
                    {
                        'title': 'Memory Care Assessment',
                        'description': 'Baseline cognitive assessment',
                        'date': timezone.now().date() - timedelta(days=15),
                        'status': 'completed'
                    },
                    {
                        'title': 'Family Care Training',
                        'description': 'Training session for family caregivers',
                        'date': timezone.now().date() + timedelta(days=15),
                        'status': 'scheduled'
                    }
                ]
            },
            {
                'patient': created_patients[2],
                'title': 'Spinal Injury Rehabilitation Plan',
                'description': 'Comprehensive rehabilitation and support plan',
                'status': 'active',
                'total_medical_costs': 150000.00,
                'monthly_cost_average': 8000.00,
                'life_expectancy': 72,
                'requirements': [
                    {
                        'title': 'Physical Therapy',
                        'category': 'therapy',
                        'description': 'Intensive physical therapy program',
                        'frequency': '5 times per week'
                    },
                    {
                        'title': 'Mobility Equipment',
                        'category': 'equipment',
                        'description': 'Wheelchair and transfer equipment',
                        'frequency': 'Daily use, maintenance every 3 months'
                    }
                ],
                'treatments': [
                    {
                        'title': 'Rehabilitation Assessment',
                        'description': 'Initial rehabilitation evaluation',
                        'date': timezone.now().date() - timedelta(days=30),
                        'status': 'completed'
                    },
                    {
                        'title': 'Home Modification Planning',
                        'description': 'Assessment for necessary home modifications',
                        'date': timezone.now().date() + timedelta(days=7),
                        'status': 'scheduled'
                    }
                ]
            }
        ]

        for plan_data in care_plans:
            care_plan, created = CarePlan.objects.get_or_create(
                patient=plan_data['patient'],
                title=plan_data['title'],
                defaults={
                    'description': plan_data['description'],
                    'status': plan_data['status'],
                    'start_date': timezone.now().date(),
                    'total_medical_costs': plan_data['total_medical_costs'],
                    'monthly_cost_average': plan_data['monthly_cost_average'],
                    'life_expectancy': plan_data['life_expectancy']
                }
            )
            
            if created:
                self.stdout.write(self.style.SUCCESS(f'Created care plan: {care_plan}'))
                
                # Create requirements
                for req_data in plan_data['requirements']:
                    requirement = MedicalRequirement.objects.create(
                        care_plan=care_plan,
                        title=req_data['title'],
                        category=req_data['category'],
                        description=req_data['description'],
                        frequency=req_data['frequency']
                    )
                    self.stdout.write(self.style.SUCCESS(f'Created requirement: {requirement}'))
                
                # Create treatments
                for treatment_data in plan_data['treatments']:
                    treatment = Treatment.objects.create(
                        care_plan=care_plan,
                        title=treatment_data['title'],
                        description=treatment_data['description'],
                        date=treatment_data['date'],
                        status=treatment_data['status']
                    )
                    self.stdout.write(self.style.SUCCESS(f'Created treatment: {treatment}'))

        self.stdout.write(self.style.SUCCESS('Successfully created all sample data'))
