from django.db import models
from django.contrib.auth.models import AbstractUser

__all__ = ['User']

class User(AbstractUser):
    ROLES = (
        ('admin', 'Admin'),
        ('student', 'Student')
    )

    GENDERS = (
        ('M', 'Male'),
        ('F', 'Female')
    )

    email = models.EmailField(unique=True)
    role = models.CharField(max_length=15, choices=ROLES, default='student')
    middle_name = models.CharField(max_length=150,  null=True, blank=True)
    suffix = models.CharField(max_length=150,  null=True, blank=True)
    birthday = models.DateField(null=True)
    address = models.CharField(max_length=255, null=True)
    mobile_number = models.CharField(max_length=15, null=True)
    gender = models.CharField(max_length=10, choices=GENDERS, null=True)
    student_id = models.CharField(max_length=150, null=True, unique=True)
    photo = models.ImageField(upload_to='user/photos/', blank=True, null=True)
    bio = models.TextField(blank=True, null=True)

    def save(self, *args, **kwargs):       
        self.is_staff = True if self.role == 'admin' or self.is_staff else False
        self.is_superuser = True if self.role == 'admin' or self.is_superuser else False
    
        return super().save(*args, **kwargs)
    
    @property
    def get_full_name(self):
        return f'{self.first_name or ""} {self.middle_name or ""} {self.last_name or ""} {self.suffix or ""}'
    
    @property
    def get_short_name(self):
        first_name_0 = f'{self.first_name[0]}.' if self.first_name else '.'
        return f'{first_name_0} {self.last_name}'
    
    @property
    def get_status(self):
        return 'active' if self.is_active else 'inactive'
    