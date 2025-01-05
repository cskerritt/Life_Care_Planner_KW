from django import forms
from django.utils.translation import gettext_lazy as _
from .models import Patient, CaseManagement, Equipment, HomeCare, MedicalCare, Medication
from .constants import US_STATES


class DateRangeForm(forms.Form):
    start = forms.DateField(widget=forms.DateInput(attrs={"type": "date"}))
    end = forms.DateField(widget=forms.DateInput(attrs={"type": "date"}))


class LifeCarePlanForm(forms.Form):
    patient_name = forms.CharField(
        min_length=2,
        widget=forms.TextInput(attrs={
            'class': 'form-input',
            'placeholder': _('John Doe')
        }),
        help_text=_('Enter the full name of the patient.')
    )
    
    date_of_birth = forms.DateField(
        widget=forms.DateInput(attrs={
            'class': 'form-input',
            'type': 'date'
        }),
        help_text=_('Enter the patient\'s date of birth.')
    )
    
    date_of_injury = forms.DateField(
        widget=forms.DateInput(attrs={
            'class': 'form-input',
            'type': 'date'
        }),
        help_text=_('Enter the date of the patient\'s injury.')
    )
    
    diagnosis = forms.CharField(
        min_length=2,
        widget=forms.TextInput(attrs={
            'class': 'form-input',
            'placeholder': _('Primary diagnosis')
        }),
        help_text=_('Enter the primary diagnosis for the patient.')
    )
    
    medical_history = forms.CharField(
        min_length=10,
        widget=forms.Textarea(attrs={
            'class': 'form-textarea min-h-[100px]',
            'placeholder': _('Enter patient\'s relevant medical history')
        }),
        help_text=_('Provide a brief summary of the patient\'s relevant medical history.')
    )


class CaseManagementForm(forms.ModelForm):
    class Meta:
        model = CaseManagement
        fields = ['title', 'description', 'client', 'assigned_to', 'priority', 'status', 'due_date', 'notes']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
            'notes': forms.Textarea(attrs={'rows': 4}),
            'due_date': forms.DateInput(attrs={'type': 'date'}),
            'priority': forms.Select(attrs={'class': 'form-select'}),
            'status': forms.Select(attrs={'class': 'form-select'}),
        }


class EquipmentForm(forms.ModelForm):
    class Meta:
        model = Equipment
        fields = [
            'name', 'description', 'category', 'manufacturer', 'model_number',
            'cost', 'replacement_frequency', 'life_expectancy', 'notes',
            'supplier', 'supplier_contact'
        ]
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
            'notes': forms.Textarea(attrs={'rows': 3}),
            'cost': forms.NumberInput(attrs={'step': '0.01', 'min': '0'}),
            'life_expectancy': forms.NumberInput(attrs={'min': '1'}),
        }

    def clean_life_expectancy(self):
        frequency = self.cleaned_data.get('replacement_frequency')
        life_expectancy = self.cleaned_data.get('life_expectancy')
        
        if frequency == 'one_time' and not life_expectancy:
            raise forms.ValidationError(_('Life expectancy is required for one-time equipment.'))
        
        return life_expectancy


class HomeCareForm(forms.ModelForm):
    class Meta:
        model = HomeCare
        fields = [
            'service_type', 'provider_type', 'provider_name', 'frequency',
            'hours_per_visit', 'rate_per_hour', 'description', 'requirements',
            'provider_contact', 'provider_credentials', 'notes'
        ]
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
            'requirements': forms.Textarea(attrs={'rows': 3}),
            'notes': forms.Textarea(attrs={'rows': 3}),
            'hours_per_visit': forms.NumberInput(attrs={'step': '0.5', 'min': '0.5'}),
            'rate_per_hour': forms.NumberInput(attrs={'step': '0.01', 'min': '0'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        hours = cleaned_data.get('hours_per_visit')
        rate = cleaned_data.get('rate_per_hour')
        
        if hours and rate:
            if hours <= 0:
                raise forms.ValidationError(_('Hours per visit must be greater than 0'))
            if rate <= 0:
                raise forms.ValidationError(_('Rate per hour must be greater than 0'))
        
        return cleaned_data


class MedicalCareForm(forms.ModelForm):
    class Meta:
        model = MedicalCare
        fields = [
            'care_type',
            'provider_name',
            'provider_specialty',
            'provider_contact',
            'facility_name',
            'facility_address',
            'description',
            'frequency',
            'duration',
            'cost_per_visit',
            'insurance_coverage',
            'start_date',
            'end_date',
            'notes',
            'requirements',
        ]
        widgets = {
            'care_type': forms.Select(attrs={'class': 'form-select'}),
            'provider_name': forms.TextInput(attrs={'class': 'form-input'}),
            'provider_specialty': forms.TextInput(attrs={'class': 'form-input'}),
            'provider_contact': forms.TextInput(attrs={'class': 'form-input'}),
            'facility_name': forms.TextInput(attrs={'class': 'form-input'}),
            'facility_address': forms.Textarea(attrs={'class': 'form-textarea', 'rows': 3}),
            'description': forms.Textarea(attrs={'class': 'form-textarea', 'rows': 4}),
            'frequency': forms.Select(attrs={'class': 'form-select'}),
            'duration': forms.NumberInput(attrs={'class': 'form-input', 'min': '0'}),
            'cost_per_visit': forms.NumberInput(attrs={'class': 'form-input', 'min': '0', 'step': '0.01'}),
            'insurance_coverage': forms.NumberInput(attrs={'class': 'form-input', 'min': '0', 'max': '100', 'step': '0.01'}),
            'start_date': forms.DateInput(attrs={'class': 'form-input', 'type': 'date'}),
            'end_date': forms.DateInput(attrs={'class': 'form-input', 'type': 'date'}),
            'notes': forms.Textarea(attrs={'class': 'form-textarea', 'rows': 4}),
            'requirements': forms.Textarea(attrs={'class': 'form-textarea', 'rows': 4}),
        }

    def clean(self):
        cleaned_data = super().clean()
        start_date = cleaned_data.get('start_date')
        end_date = cleaned_data.get('end_date')

        if start_date and end_date and end_date < start_date:
            raise forms.ValidationError(_('End date must be after start date.'))

        return cleaned_data


class MedicationForm(forms.ModelForm):
    class Meta:
        model = Medication
        fields = [
            'name', 'generic_name', 'strength', 'dosage', 'frequency', 'route',
            'prescribing_doctor', 'pharmacy', 'cost_per_refill', 'insurance_coverage',
            'refill_quantity', 'refill_interval', 'start_date', 'end_date',
            'purpose', 'side_effects', 'special_instructions', 'notes'
        ]
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'end_date': forms.DateInput(attrs={'type': 'date'}),
            'purpose': forms.Textarea(attrs={'rows': 3}),
            'side_effects': forms.Textarea(attrs={'rows': 3}),
            'special_instructions': forms.Textarea(attrs={'rows': 3}),
            'notes': forms.Textarea(attrs={'rows': 3}),
        }

    def clean(self):
        cleaned_data = super().clean()
        start_date = cleaned_data.get('start_date')
        end_date = cleaned_data.get('end_date')

        if start_date and end_date and end_date < start_date:
            raise forms.ValidationError(_('End date cannot be before start date.'))

        return cleaned_data


class PatientForm(forms.ModelForm):
    class Meta:
        model = Patient
        fields = [
            'first_name', 'middle_name', 'last_name', 'date_of_birth', 'gender',
            'marital_status', 'ssn', 'email', 'phone_primary', 'phone_secondary',
            'address_line1', 'address_line2', 'city', 'state', 'zip_code',
            'emergency_contact_name', 'emergency_contact_relationship', 'emergency_contact_phone',
            'primary_insurance', 'primary_insurance_id', 'primary_insurance_group',
            'secondary_insurance', 'secondary_insurance_id', 'secondary_insurance_group',
            'primary_physician', 'primary_physician_phone', 'preferred_pharmacy',
            'preferred_pharmacy_phone', 'allergies', 'medical_conditions',
            'occupation', 'employer', 'notes'
        ]
        widgets = {
            'date_of_birth': forms.DateInput(attrs={'type': 'date'}),
            'ssn': forms.TextInput(attrs={'pattern': r'\d{3}-\d{2}-\d{4}', 'placeholder': '123-45-6789'}),
            'phone_primary': forms.TextInput(attrs={'pattern': r'\(\d{3}\) \d{3}-\d{4}', 'placeholder': '(123) 456-7890'}),
            'phone_secondary': forms.TextInput(attrs={'pattern': r'\(\d{3}\) \d{3}-\d{4}', 'placeholder': '(123) 456-7890'}),
            'emergency_contact_phone': forms.TextInput(attrs={'pattern': r'\(\d{3}\) \d{3}-\d{4}', 'placeholder': '(123) 456-7890'}),
            'primary_physician_phone': forms.TextInput(attrs={'pattern': r'\(\d{3}\) \d{3}-\d{4}', 'placeholder': '(123) 456-7890'}),
            'preferred_pharmacy_phone': forms.TextInput(attrs={'pattern': r'\(\d{3}\) \d{3}-\d{4}', 'placeholder': '(123) 456-7890'}),
            'state': forms.Select(choices=US_STATES),
            'allergies': forms.Textarea(attrs={'rows': 3}),
            'medical_conditions': forms.Textarea(attrs={'rows': 3}),
            'notes': forms.Textarea(attrs={'rows': 3}),
        }

    def clean_ssn(self):
        """Validate and format SSN."""
        ssn = self.cleaned_data.get('ssn')
        if ssn:
            # Remove any non-digit characters
            ssn_digits = ''.join(filter(str.isdigit, ssn))
            if len(ssn_digits) != 9:
                raise forms.ValidationError(_('SSN must be 9 digits.'))
            # Format as XXX-XX-XXXX
            return f"{ssn_digits[:3]}-{ssn_digits[3:5]}-{ssn_digits[5:]}"
        return ssn

    def clean_phone(self, phone):
        """Validate and format phone number."""
        if phone:
            # Remove any non-digit characters
            phone_digits = ''.join(filter(str.isdigit, phone))
            if len(phone_digits) != 10:
                raise forms.ValidationError(_('Phone number must be 10 digits.'))
            # Format as (XXX) XXX-XXXX
            return f"({phone_digits[:3]}) {phone_digits[3:6]}-{phone_digits[6:]}"
        return phone

    def clean_phone_primary(self):
        return self.clean_phone(self.cleaned_data.get('phone_primary'))

    def clean_phone_secondary(self):
        return self.clean_phone(self.cleaned_data.get('phone_secondary'))

    def clean_emergency_contact_phone(self):
        return self.clean_phone(self.cleaned_data.get('emergency_contact_phone'))

    def clean_primary_physician_phone(self):
        return self.clean_phone(self.cleaned_data.get('primary_physician_phone'))

    def clean_preferred_pharmacy_phone(self):
        return self.clean_phone(self.cleaned_data.get('preferred_pharmacy_phone'))

    def clean_zip_code(self):
        """Validate ZIP code."""
        zip_code = self.cleaned_data.get('zip_code')
        if zip_code:
            # Remove any non-digit characters
            zip_digits = ''.join(filter(str.isdigit, zip_code))
            if len(zip_digits) not in [5, 9]:
                raise forms.ValidationError(_('ZIP code must be 5 or 9 digits.'))
            # Format as XXXXX or XXXXX-XXXX
            if len(zip_digits) == 9:
                return f"{zip_digits[:5]}-{zip_digits[5:]}"
            return zip_digits
        return zip_code
