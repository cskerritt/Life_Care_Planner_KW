from django.db import models
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from django.core.validators import MinValueValidator, MaxValueValidator

User = get_user_model()

class CalendarEvent(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='calendar_events')
    title = models.CharField(_('Title'), max_length=200)
    description = models.TextField(_('Description'), blank=True)
    date = models.DateField(_('Date'))
    time = models.TimeField(_('Time'))
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['date', 'time']
        verbose_name = _('Calendar Event')
        verbose_name_plural = _('Calendar Events')

    def __str__(self):
        return f"{self.title} - {self.date}"

class CaseManagement(models.Model):
    PRIORITY_CHOICES = [
        ('low', _('Low')),
        ('medium', _('Medium')),
        ('high', _('High')),
    ]

    STATUS_CHOICES = [
        ('open', _('Open')),
        ('in_progress', _('In Progress')),
        ('pending', _('Pending')),
        ('closed', _('Closed')),
    ]

    title = models.CharField(_('Title'), max_length=200)
    description = models.TextField(_('Description'))
    client = models.ForeignKey('Evaluee', on_delete=models.CASCADE, related_name='case_management_entries')
    assigned_to = models.ForeignKey(User, on_delete=models.CASCADE, related_name='assigned_cases')
    priority = models.CharField(_('Priority'), max_length=10, choices=PRIORITY_CHOICES, default='medium')
    status = models.CharField(_('Status'), max_length=20, choices=STATUS_CHOICES, default='open')
    due_date = models.DateField(_('Due Date'), null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    notes = models.TextField(_('Notes'), blank=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = _('Case Management Entry')
        verbose_name_plural = _('Case Management Entries')

    def __str__(self):
        return f"{self.title} - {self.client.full_name}"

class Equipment(models.Model):
    FREQUENCY_CHOICES = [
        ('one_time', _('One Time')),
        ('monthly', _('Monthly')),
        ('yearly', _('Yearly')),
        ('as_needed', _('As Needed')),
    ]

    CATEGORY_CHOICES = [
        ('mobility', _('Mobility')),
        ('medical', _('Medical')),
        ('assistive', _('Assistive Technology')),
        ('home_modification', _('Home Modification')),
        ('other', _('Other')),
    ]

    name = models.CharField(_('Name'), max_length=200)
    description = models.TextField(_('Description'))
    category = models.CharField(_('Category'), max_length=20, choices=CATEGORY_CHOICES)
    manufacturer = models.CharField(_('Manufacturer'), max_length=200, blank=True)
    model_number = models.CharField(_('Model Number'), max_length=100, blank=True)
    cost = models.DecimalField(_('Cost'), max_digits=10, decimal_places=2)
    replacement_frequency = models.CharField(_('Replacement Frequency'), max_length=20, choices=FREQUENCY_CHOICES)
    life_expectancy = models.PositiveIntegerField(_('Life Expectancy (years)'), null=True, blank=True)
    notes = models.TextField(_('Notes'), blank=True)
    supplier = models.CharField(_('Supplier'), max_length=200, blank=True)
    supplier_contact = models.CharField(_('Supplier Contact'), max_length=200, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    care_plan = models.ForeignKey('CarePlan', on_delete=models.CASCADE, related_name='equipment')

    class Meta:
        ordering = ['name']
        verbose_name = _('Equipment')
        verbose_name_plural = _('Equipment')

    def __str__(self):
        return f"{self.name} - {self.get_category_display()}"

    @property
    def annual_cost(self):
        if self.replacement_frequency == 'monthly':
            return self.cost * 12
        elif self.replacement_frequency == 'yearly':
            return self.cost
        elif self.replacement_frequency == 'one_time':
            return self.cost / (self.life_expectancy or 1)
        return self.cost

class HomeCare(models.Model):
    FREQUENCY_CHOICES = [
        ('daily', _('Daily')),
        ('weekly', _('Weekly')),
        ('monthly', _('Monthly')),
        ('as_needed', _('As Needed')),
    ]

    SERVICE_TYPE_CHOICES = [
        ('personal_care', _('Personal Care')),
        ('skilled_nursing', _('Skilled Nursing')),
        ('therapy', _('Therapy')),
        ('housekeeping', _('Housekeeping')),
        ('meal_prep', _('Meal Preparation')),
        ('transportation', _('Transportation')),
        ('companionship', _('Companionship')),
        ('other', _('Other')),
    ]

    PROVIDER_TYPE_CHOICES = [
        ('agency', _('Home Care Agency')),
        ('independent', _('Independent Provider')),
        ('family', _('Family Caregiver')),
        ('other', _('Other')),
    ]

    care_plan = models.ForeignKey('CarePlan', on_delete=models.CASCADE, related_name='home_care')
    service_type = models.CharField(_('Service Type'), max_length=20, choices=SERVICE_TYPE_CHOICES)
    provider_type = models.CharField(_('Provider Type'), max_length=20, choices=PROVIDER_TYPE_CHOICES)
    provider_name = models.CharField(_('Provider Name'), max_length=200)
    frequency = models.CharField(_('Frequency'), max_length=20, choices=FREQUENCY_CHOICES)
    hours_per_visit = models.DecimalField(_('Hours per Visit'), max_digits=4, decimal_places=1)
    rate_per_hour = models.DecimalField(_('Rate per Hour'), max_digits=8, decimal_places=2)
    description = models.TextField(_('Description'))
    requirements = models.TextField(_('Special Requirements'), blank=True)
    provider_contact = models.CharField(_('Provider Contact'), max_length=200, blank=True)
    provider_credentials = models.CharField(_('Provider Credentials'), max_length=200, blank=True)
    notes = models.TextField(_('Notes'), blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['service_type', 'provider_name']
        verbose_name = _('Home Care Service')
        verbose_name_plural = _('Home Care Services')

    def __str__(self):
        return f"{self.get_service_type_display()} - {self.provider_name}"

    @property
    def cost_per_visit(self):
        return self.hours_per_visit * self.rate_per_hour

    @property
    def monthly_cost(self):
        if self.frequency == 'daily':
            return self.cost_per_visit * 30
        elif self.frequency == 'weekly':
            return self.cost_per_visit * 4
        elif self.frequency == 'monthly':
            return self.cost_per_visit
        return 0  # For as_needed frequency

    @property
    def annual_cost(self):
        return self.monthly_cost * 12

class MedicalCare(models.Model):
    CARE_TYPE_CHOICES = [
        ('primary', _('Primary Care')),
        ('specialist', _('Specialist Care')),
        ('therapy', _('Therapy')),
        ('surgery', _('Surgery')),
        ('diagnostic', _('Diagnostic Tests')),
        ('emergency', _('Emergency Care')),
        ('preventive', _('Preventive Care')),
        ('other', _('Other')),
    ]

    FREQUENCY_CHOICES = [
        ('once', _('One Time')),
        ('daily', _('Daily')),
        ('weekly', _('Weekly')),
        ('biweekly', _('Bi-weekly')),
        ('monthly', _('Monthly')),
        ('quarterly', _('Quarterly')),
        ('annually', _('Annually')),
        ('as_needed', _('As Needed')),
    ]

    care_plan = models.ForeignKey('CarePlan', on_delete=models.CASCADE)
    care_type = models.CharField(max_length=20, choices=CARE_TYPE_CHOICES)
    provider_name = models.CharField(max_length=255)
    provider_specialty = models.CharField(max_length=255)
    provider_contact = models.CharField(max_length=255, blank=True)
    facility_name = models.CharField(max_length=255, blank=True)
    facility_address = models.TextField(blank=True)
    
    description = models.TextField()
    frequency = models.CharField(max_length=20, choices=FREQUENCY_CHOICES)
    duration = models.PositiveIntegerField(help_text=_("Duration in minutes"))
    cost_per_visit = models.DecimalField(max_digits=10, decimal_places=2)
    insurance_coverage = models.DecimalField(max_digits=5, decimal_places=2, help_text=_("Coverage percentage"), validators=[MinValueValidator(0), MaxValueValidator(100)])
    
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    
    notes = models.TextField(blank=True)
    requirements = models.TextField(blank=True, help_text=_("Special requirements or preparations"))
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _("Medical Care")
        verbose_name_plural = _("Medical Care")
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.get_care_type_display()} - {self.provider_name}"

    def calculate_out_of_pocket_cost(self):
        """Calculate the out-of-pocket cost per visit"""
        coverage_decimal = self.insurance_coverage / 100
        return self.cost_per_visit * (1 - coverage_decimal)

    def calculate_monthly_cost(self):
        """Calculate the estimated monthly cost"""
        visits_per_month = {
            'once': 0,
            'daily': 30,
            'weekly': 4,
            'biweekly': 2,
            'monthly': 1,
            'quarterly': 1/3,
            'annually': 1/12,
            'as_needed': 1,  # Assume once per month for as needed
        }
        
        visits = visits_per_month.get(self.frequency, 0)
        return self.calculate_out_of_pocket_cost() * visits

    def calculate_annual_cost(self):
        """Calculate the estimated annual cost"""
        return self.calculate_monthly_cost() * 12

class Medication(models.Model):
    FREQUENCY_CHOICES = [
        ('once', _('Once')),
        ('daily', _('Daily')),
        ('twice_daily', _('Twice Daily')),
        ('three_times_daily', _('Three Times Daily')),
        ('four_times_daily', _('Four Times Daily')),
        ('weekly', _('Weekly')),
        ('monthly', _('Monthly')),
        ('as_needed', _('As Needed')),
    ]

    ROUTE_CHOICES = [
        ('oral', _('Oral')),
        ('topical', _('Topical')),
        ('injection', _('Injection')),
        ('inhalation', _('Inhalation')),
        ('other', _('Other')),
    ]

    care_plan = models.ForeignKey('CarePlan', on_delete=models.CASCADE, related_name='medications')
    name = models.CharField(_('Medication Name'), max_length=255)
    generic_name = models.CharField(_('Generic Name'), max_length=255, blank=True)
    strength = models.CharField(_('Strength'), max_length=100)
    dosage = models.CharField(_('Dosage'), max_length=100)
    frequency = models.CharField(_('Frequency'), max_length=20, choices=FREQUENCY_CHOICES)
    route = models.CharField(_('Route'), max_length=20, choices=ROUTE_CHOICES)
    prescribing_doctor = models.CharField(_('Prescribing Doctor'), max_length=255)
    pharmacy = models.CharField(_('Pharmacy'), max_length=255, blank=True)
    cost_per_refill = models.DecimalField(_('Cost per Refill'), max_digits=10, decimal_places=2)
    insurance_coverage = models.DecimalField(_('Insurance Coverage (%)'), max_digits=5, decimal_places=2, default=0)
    refill_quantity = models.IntegerField(_('Refill Quantity'))
    refill_interval = models.IntegerField(_('Days Between Refills'))
    start_date = models.DateField(_('Start Date'), null=True, blank=True)
    end_date = models.DateField(_('End Date'), null=True, blank=True)
    purpose = models.TextField(_('Purpose'), blank=True)
    side_effects = models.TextField(_('Side Effects'), blank=True)
    special_instructions = models.TextField(_('Special Instructions'), blank=True)
    notes = models.TextField(_('Notes'), blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['name']
        verbose_name = _('Medication')
        verbose_name_plural = _('Medications')

    def __str__(self):
        return f"{self.name} - {self.strength}"

    def calculate_monthly_cost(self):
        """Calculate the estimated monthly cost of the medication."""
        if not self.cost_per_refill or not self.refill_interval:
            return 0
        
        monthly_refills = 30 / self.refill_interval
        total_cost = self.cost_per_refill * monthly_refills
        insurance_coverage = total_cost * (self.insurance_coverage / 100)
        return total_cost - insurance_coverage

    def calculate_annual_cost(self):
        """Calculate the estimated annual cost of the medication."""
        return self.calculate_monthly_cost() * 12

    def get_next_refill_date(self):
        """Calculate the next refill date based on the last refill and interval."""
        from datetime import date, timedelta
        if not hasattr(self, 'last_refill_date'):
            return None
        return self.last_refill_date + timedelta(days=self.refill_interval)

class Patient(models.Model):
    GENDER_CHOICES = [
        ('M', _('Male')),
        ('F', _('Female')),
        ('O', _('Other')),
    ]

    MARITAL_STATUS_CHOICES = [
        ('single', _('Single')),
        ('married', _('Married')),
        ('divorced', _('Divorced')),
        ('widowed', _('Widowed')),
        ('separated', _('Separated')),
    ]

    # Personal Information
    first_name = models.CharField(_('First Name'), max_length=100)
    middle_name = models.CharField(_('Middle Name'), max_length=100, blank=True)
    last_name = models.CharField(_('Last Name'), max_length=100)
    date_of_birth = models.DateField(_('Date of Birth'))
    gender = models.CharField(_('Gender'), max_length=1, choices=GENDER_CHOICES)
    marital_status = models.CharField(_('Marital Status'), max_length=10, choices=MARITAL_STATUS_CHOICES)
    ssn = models.CharField(_('Social Security Number'), max_length=11, blank=True)
    email = models.EmailField(_('Email'), blank=True)
    phone_primary = models.CharField(_('Primary Phone'), max_length=20)
    phone_secondary = models.CharField(_('Secondary Phone'), max_length=20, blank=True)
    
    # Address Information
    address_line1 = models.CharField(_('Address Line 1'), max_length=255)
    address_line2 = models.CharField(_('Address Line 2'), max_length=255, blank=True)
    city = models.CharField(_('City'), max_length=100)
    state = models.CharField(_('State'), max_length=2)
    zip_code = models.CharField(_('ZIP Code'), max_length=10)
    
    # Emergency Contact
    emergency_contact_name = models.CharField(_('Emergency Contact Name'), max_length=200)
    emergency_contact_relationship = models.CharField(_('Emergency Contact Relationship'), max_length=100)
    emergency_contact_phone = models.CharField(_('Emergency Contact Phone'), max_length=20)
    
    # Insurance Information
    primary_insurance = models.CharField(_('Primary Insurance'), max_length=100, blank=True)
    primary_insurance_id = models.CharField(_('Primary Insurance ID'), max_length=50, blank=True)
    primary_insurance_group = models.CharField(_('Primary Insurance Group'), max_length=50, blank=True)
    secondary_insurance = models.CharField(_('Secondary Insurance'), max_length=100, blank=True)
    secondary_insurance_id = models.CharField(_('Secondary Insurance ID'), max_length=50, blank=True)
    secondary_insurance_group = models.CharField(_('Secondary Insurance Group'), max_length=50, blank=True)
    
    # Medical Information
    primary_physician = models.CharField(_('Primary Physician'), max_length=200, blank=True)
    primary_physician_phone = models.CharField(_('Primary Physician Phone'), max_length=20, blank=True)
    preferred_pharmacy = models.CharField(_('Preferred Pharmacy'), max_length=200, blank=True)
    preferred_pharmacy_phone = models.CharField(_('Preferred Pharmacy Phone'), max_length=20, blank=True)
    allergies = models.TextField(_('Allergies'), blank=True)
    medical_conditions = models.TextField(_('Medical Conditions'), blank=True)
    
    # Additional Information
    occupation = models.CharField(_('Occupation'), max_length=200, blank=True)
    employer = models.CharField(_('Employer'), max_length=200, blank=True)
    notes = models.TextField(_('Notes'), blank=True)
    
    # System Fields
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name='patients_created'
    )
    updated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name='patients_updated'
    )

    class Meta:
        ordering = ['last_name', 'first_name']
        verbose_name = _('Patient')
        verbose_name_plural = _('Patients')

    def __str__(self):
        return f"{self.last_name}, {self.first_name}"

    def get_full_name(self):
        """Returns the patient's full name."""
        if self.middle_name:
            return f"{self.first_name} {self.middle_name} {self.last_name}"
        return f"{self.first_name} {self.last_name}"

    def get_age(self):
        """Calculate patient's age."""
        from datetime import date
        today = date.today()
        age = today.year - self.date_of_birth.year
        if today.month < self.date_of_birth.month or (
            today.month == self.date_of_birth.month and today.day < self.date_of_birth.day
        ):
            age -= 1
        return age

    def get_full_address(self):
        """Returns the patient's full address."""
        address = [self.address_line1]
        if self.address_line2:
            address.append(self.address_line2)
        address.append(f"{self.city}, {self.state} {self.zip_code}")
        return '\n'.join(address)
