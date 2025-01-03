from datetime import datetime, timedelta
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.utils import timezone
from apps.api.models import Patient, CarePlan, Task, MedicalRecord, CareTeamMember

User = get_user_model()

class Command(BaseCommand):
    help = 'Creates test data for the Life Care Planner app'

    def handle(self, *args, **kwargs):
        # Create test user if doesn't exist
        user, created = User.objects.get_or_create(
            username='testuser',
            email='test@example.com',
            defaults={'is_staff': True}
        )
        if created:
            user.set_password('testpass123')
            user.save()
            self.stdout.write(self.style.SUCCESS(f'Created test user: {user.username}'))
        
        # Create test patients
        patient1 = Patient.objects.create(
            user=user,
            first_name='John',
            last_name='Doe',
            date_of_birth='1945-01-15',
            medical_record_number='MRN001',
            primary_diagnosis='Type 2 Diabetes'
        )
        
        patient2 = Patient.objects.create(
            user=user,
            first_name='Jane',
            last_name='Smith',
            date_of_birth='1950-03-20',
            medical_record_number='MRN002',
            primary_diagnosis='Hypertension'
        )
        
        # Create care team members
        doctor = CareTeamMember.objects.create(
            patient=patient1,
            name='Dr. Sarah Johnson',
            role='doctor',
            contact_email='sarah@hospital.com',
            contact_phone='555-0123'
        )
        
        nurse = CareTeamMember.objects.create(
            patient=patient1,
            name='Michael Chen',
            role='nurse',
            contact_email='michael@hospital.com',
            contact_phone='555-0124'
        )
        
        # Create care plans
        care_plan1 = CarePlan.objects.create(
            patient=patient1,
            title='Diabetes Management Plan',
            description='Comprehensive plan for managing type 2 diabetes',
            start_date=timezone.now().date(),
            status='active'
        )
        
        care_plan2 = CarePlan.objects.create(
            patient=patient2,
            title='Blood Pressure Management',
            description='Plan for controlling hypertension',
            start_date=timezone.now().date(),
            status='active'
        )
        
        # Create tasks
        Task.objects.create(
            care_plan=care_plan1,
            title='Blood Sugar Check',
            description='Check and record blood sugar levels',
            due_date=timezone.now() + timedelta(hours=2),
            priority='high',
            assigned_to=nurse
        )
        
        Task.objects.create(
            care_plan=care_plan1,
            title='Medication Review',
            description='Review current medications',
            due_date=timezone.now() + timedelta(days=1),
            priority='medium',
            assigned_to=doctor
        )
        
        Task.objects.create(
            care_plan=care_plan2,
            title='Blood Pressure Reading',
            description='Take blood pressure reading',
            due_date=timezone.now() + timedelta(hours=4),
            priority='medium'
        )
        
        # Create medical records
        MedicalRecord.objects.create(
            patient=patient1,
            record_type='lab',
            title='A1C Test Results',
            content='A1C level: 7.2%',
            date_of_record=timezone.now().date(),
            provider=doctor
        )
        
        MedicalRecord.objects.create(
            patient=patient1,
            record_type='note',
            title='Follow-up Visit Notes',
            content='Patient showing improvement in glucose control',
            date_of_record=timezone.now().date() - timedelta(days=2),
            provider=doctor
        )
        
        MedicalRecord.objects.create(
            patient=patient2,
            record_type='lab',
            title='Blood Pressure Reading',
            content='BP: 138/88',
            date_of_record=timezone.now().date(),
        )
        
        self.stdout.write(self.style.SUCCESS('Successfully created test data'))