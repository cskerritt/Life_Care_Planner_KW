from django.db import migrations

def copy_patient_to_evaluee(apps, schema_editor):
    Patient = apps.get_model('api', 'Patient')
    Evaluee = apps.get_model('api', 'Evaluee')
    CarePlan = apps.get_model('api', 'CarePlan')
    CareTeamMember = apps.get_model('api', 'CareTeamMember')
    MedicalRecord = apps.get_model('api', 'MedicalRecord')

    # Create a mapping of Patient IDs to Evaluee IDs
    patient_to_evaluee = {}

    # Copy all Patient records to Evaluee
    for patient in Patient.objects.all():
        evaluee = Evaluee.objects.create(
            user=patient.user,
            first_name=patient.first_name,
            last_name=patient.last_name,
            date_of_birth=patient.date_of_birth,
            medical_record_number=patient.medical_record_number,
            primary_diagnosis=patient.primary_diagnosis,
            notes=patient.notes,
            created_at=patient.created_at,
            updated_at=patient.updated_at
        )
        patient_to_evaluee[patient.id] = evaluee

    # Update CarePlan records
    for care_plan in CarePlan.objects.all():
        if care_plan.patient_id in patient_to_evaluee:
            care_plan.evaluee = patient_to_evaluee[care_plan.patient_id]
            care_plan.save()

    # Update CareTeamMember records
    for team_member in CareTeamMember.objects.all():
        if team_member.patient_id in patient_to_evaluee:
            team_member.evaluee = patient_to_evaluee[team_member.patient_id]
            team_member.save()

    # Update MedicalRecord records
    for record in MedicalRecord.objects.all():
        if record.patient_id in patient_to_evaluee:
            record.evaluee = patient_to_evaluee[record.patient_id]
            record.save()

def reverse_copy_patient_to_evaluee(apps, schema_editor):
    Evaluee = apps.get_model('api', 'Evaluee')
    CarePlan = apps.get_model('api', 'CarePlan')
    CareTeamMember = apps.get_model('api', 'CareTeamMember')
    MedicalRecord = apps.get_model('api', 'MedicalRecord')

    # Remove evaluee references from related models
    CarePlan.objects.all().update(evaluee=None)
    CareTeamMember.objects.all().update(evaluee=None)
    MedicalRecord.objects.all().update(evaluee=None)

    # Delete all Evaluee records
    Evaluee.objects.all().delete()


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0004_add_evaluee_model'),
    ]

    operations = [
        migrations.RunPython(copy_patient_to_evaluee, reverse_copy_patient_to_evaluee),
    ]
