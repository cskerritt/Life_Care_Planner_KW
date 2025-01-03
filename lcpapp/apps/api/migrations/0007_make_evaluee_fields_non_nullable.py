from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0006_remove_patient_model_and_fields'),
    ]

    operations = [
        migrations.AlterField(
            model_name='careplan',
            name='evaluee',
            field=models.ForeignKey(on_delete=models.deletion.CASCADE, related_name='care_plans', to='api.evaluee'),
        ),
        migrations.AlterField(
            model_name='careteammember',
            name='evaluee',
            field=models.ForeignKey(on_delete=models.deletion.CASCADE, related_name='care_team', to='api.evaluee'),
        ),
        migrations.AlterField(
            model_name='medicalrecord',
            name='evaluee',
            field=models.ForeignKey(on_delete=models.deletion.CASCADE, related_name='medical_records', to='api.evaluee'),
        ),
    ]
