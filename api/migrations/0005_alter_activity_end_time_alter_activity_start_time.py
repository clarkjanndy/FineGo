# Generated by Django 4.2.8 on 2024-01-10 09:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0004_activity_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='activity',
            name='end_time',
            field=models.DateTimeField(),
        ),
        migrations.AlterField(
            model_name='activity',
            name='start_time',
            field=models.DateTimeField(),
        ),
    ]