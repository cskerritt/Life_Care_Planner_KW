from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0005_copy_patient_to_evaluee'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='careplan',
            name='patient',
        ),
        migrations.RemoveField(
            model_name='careteammember',
            name='patient',
        ),
        migrations.RemoveField(
            model_name='medicalrecord',
            name='patient',
        ),
        migrations.DeleteModel(
            name='Patient',
        ),
    ]
