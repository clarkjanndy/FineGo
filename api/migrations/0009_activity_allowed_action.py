# Generated by Django 4.1.5 on 2024-01-11 14:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0008_remove_fine_attendance_fine_activity'),
    ]

    operations = [
        migrations.AddField(
            model_name='activity',
            name='allowed_action',
            field=models.CharField(blank=True, choices=[('time-in', 'Time-In'), ('time-out', 'Time-Out')], max_length=10, null=True),
        ),
    ]