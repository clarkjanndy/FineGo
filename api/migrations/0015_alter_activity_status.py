# Generated by Django 4.2.8 on 2024-02-25 15:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0014_alter_notification_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='activity',
            name='status',
            field=models.CharField(choices=[('draft', 'Draft'), ('active', 'Active'), ('open', 'Open'), ('closing', 'Closing'), ('closing-error', 'Closing Error'), ('closed', 'Closed')], default='active', max_length=15),
        ),
    ]