# Generated by Django 4.2.8 on 2023-12-10 02:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0003_alter_department_description_alter_department_theme'),
    ]

    operations = [
        migrations.AddField(
            model_name='department',
            name='abbreviation',
            field=models.CharField(default='AR', max_length=4),
            preserve_default=False,
        ),
    ]
