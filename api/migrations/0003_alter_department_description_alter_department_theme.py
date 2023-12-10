# Generated by Django 4.2.8 on 2023-12-09 09:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_department'),
    ]

    operations = [
        migrations.AlterField(
            model_name='department',
            name='description',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='department',
            name='theme',
            field=models.CharField(default='#4e73df', max_length=255),
        ),
    ]