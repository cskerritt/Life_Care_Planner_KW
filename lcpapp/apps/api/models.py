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


class Evaluee(models.Model):
    """An evaluee in the Life Care Planning system"""
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="evaluees")
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
    """A care plan for an evaluee"""
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('active', 'Active'),
        ('completed', 'Completed'),
        ('archived', 'Archived'),
    ]

    evaluee = models.ForeignKey(Evaluee, on_delete=models.CASCADE, related_name="care_plans")
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
        return f"{self.title} - {self.evaluee}"

    class Meta:
        ordering = ['-created_at']


class CarePlanItem(models.Model):
    """Base class for all care plan items"""
    CATEGORY_CHOICES = [
        ('physician_evaluation', 'Physician Evaluation'),
        ('physician_followup', 'Physician Follow Up'),
        ('diagnostics', 'Diagnostics'),
        ('medications', 'Medications'),
        ('therapy_evaluations', 'Therapy Evaluations'),
        ('therapies', 'Therapies'),
        ('interventional', 'Interventional'),
        ('surgeries', 'Surgeries'),
        ('aids_independence', 'Aids for Independence'),
        ('prosthetics_orthotics', 'Prosthetics/Orthotics'),
        ('supplies', 'Supplies'),
        ('home_services', 'Home Services'),
        ('home_maintenance', 'Home Maintenance'),
        ('home_modification', 'Home Modification'),
        ('case_management', 'Case Management'),
        ('transportation', 'Transportation'),
    ]

    STATUS_CHOICES = [
        ('scheduled', 'Scheduled'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
    ]

    care_plan = models.ForeignKey(CarePlan, on_delete=models.CASCADE, related_name='items')
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    title = models.CharField(max_length=200)
    description = models.TextField()
    frequency = models.CharField(max_length=100)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='scheduled')
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    cost = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.title} - {self.get_category_display()}"

    class Meta:
        ordering = ['category', 'start_date']


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
    completed_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['due_date', '-priority']
