from django.conf import settings
from django.db import models
from rest_framework_api_key.models import AbstractAPIKey


class UserAPIKey(AbstractAPIKey):
    """
    API Key associated with a User, allowing you to scope the key's API access based on what the user
    is allowed to view/do.
    """

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="api_keys")

    class Meta(AbstractAPIKey.Meta):
        verbose_name = "User API key"
        verbose_name_plural = "User API keys"


class Patient(models.Model):
    """A patient/client in the Life Care Planning system"""
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="patients")
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    date_of_birth = models.DateField()
    medical_record_number = models.CharField(max_length=50, blank=True)
    primary_diagnosis = models.TextField()
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    class Meta:
        ordering = ['-created_at']


class CarePlan(models.Model):
    """A care plan for a patient"""
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('active', 'Active'),
        ('completed', 'Completed'),
        ('archived', 'Archived'),
    ]

    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name="care_plans")
    title = models.CharField(max_length=200)
    description = models.TextField()
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')
    total_medical_costs = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    monthly_cost_average = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    life_expectancy = models.IntegerField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.title} - {self.patient}"

    class Meta:
        ordering = ['-created_at']


class MedicalRequirement(models.Model):
    """Medical requirements for a care plan"""
    CATEGORY_CHOICES = [
        ('medication', 'Medication'),
        ('therapy', 'Therapy'),
        ('equipment', 'Equipment'),
        ('other', 'Other'),
    ]

    care_plan = models.ForeignKey(CarePlan, on_delete=models.CASCADE, related_name='medical_requirements')
    title = models.CharField(max_length=200)
    description = models.TextField()
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    frequency = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.title} - {self.care_plan}"

    class Meta:
        ordering = ['category', 'title']


class Treatment(models.Model):
    """Treatments in a care plan timeline"""
    STATUS_CHOICES = [
        ('scheduled', 'Scheduled'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
    ]

    care_plan = models.ForeignKey(CarePlan, on_delete=models.CASCADE, related_name='treatments')
    title = models.CharField(max_length=200)
    description = models.TextField()
    date = models.DateField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='scheduled')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.title} - {self.care_plan}"

    class Meta:
        ordering = ['date']


class CareTeamMember(models.Model):
    """A member of a patient's care team"""
    ROLE_CHOICES = [
        ('doctor', 'Doctor'),
        ('nurse', 'Nurse'),
        ('therapist', 'Therapist'),
        ('caregiver', 'Caregiver'),
        ('family', 'Family Member'),
        ('other', 'Other'),
    ]

    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name="care_team")
    name = models.CharField(max_length=200)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    contact_email = models.EmailField()
    contact_phone = models.CharField(max_length=20, blank=True)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} ({self.role})"

    class Meta:
        ordering = ['role', 'name']


class Task(models.Model):
    """A task or appointment in a care plan"""
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]
    PRIORITY_CHOICES = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
        ('urgent', 'Urgent'),
    ]

    care_plan = models.ForeignKey(CarePlan, on_delete=models.CASCADE, related_name="tasks")
    title = models.CharField(max_length=200)
    description = models.TextField()
    due_date = models.DateTimeField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    priority = models.CharField(max_length=20, choices=PRIORITY_CHOICES, default='medium')
    assigned_to = models.ForeignKey(CareTeamMember, on_delete=models.SET_NULL, null=True, blank=True, related_name="assigned_tasks")
    completed_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['due_date', '-priority']


class MedicalRecord(models.Model):
    """A medical record entry for a patient"""
    RECORD_TYPES = [
        ('note', 'Clinical Note'),
        ('lab', 'Lab Result'),
        ('imaging', 'Imaging Result'),
        ('medication', 'Medication'),
        ('procedure', 'Procedure'),
        ('other', 'Other'),
    ]

    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name="medical_records")
    record_type = models.CharField(max_length=20, choices=RECORD_TYPES)
    title = models.CharField(max_length=200)
    content = models.TextField()
    date_of_record = models.DateField()
    provider = models.ForeignKey(CareTeamMember, on_delete=models.SET_NULL, null=True, blank=True, related_name="medical_records")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.record_type}: {self.title}"

    class Meta:
        ordering = ['-date_of_record']
