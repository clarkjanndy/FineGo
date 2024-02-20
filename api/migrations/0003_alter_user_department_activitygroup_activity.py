# Generated by Django 4.2.8 on 2024-01-10 08:03

import api.models.activity
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_user_department'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='department',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='members', to='api.department'),
        ),
        migrations.CreateModel(
            name='ActivityGroup',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('modified_at', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=255)),
                ('description', models.TextField(blank=True, null=True)),
                ('status', models.CharField(choices=[('active', 'Active'), ('inactive', 'Inactive')], max_length=10)),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='created_activity_group', to=settings.AUTH_USER_MODEL)),
                ('participants', models.ManyToManyField(default=api.models.activity.default_participants, related_name='activity_groups', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Activity',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('modified_at', models.DateTimeField(auto_now=True)),
                ('start_time', models.DateField()),
                ('end_time', models.DateField()),
                ('status', models.CharField(choices=[('draft', 'Draft'), ('active', 'Active'), ('open', 'Open'), ('closing', 'Closing'), ('closed', 'Closed')], default='active', max_length=10)),
                ('group', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='activities', to='api.activitygroup')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]