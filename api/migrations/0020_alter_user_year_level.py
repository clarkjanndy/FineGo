# Generated by Django 4.2.10 on 2024-03-29 08:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0019_user_year_level'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='year_level',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
