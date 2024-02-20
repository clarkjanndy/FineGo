# Generated by Django 4.2.8 on 2024-02-20 17:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0010_fine_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='fine',
            name='status',
            field=models.CharField(choices=[('paid', 'Paid'), ('unpaid', 'Unpaid')], default='unpaid', max_length=8),
        ),
    ]
