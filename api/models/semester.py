from django.db import models
from . extras import TimeStampedModel

from . user import User

__all__ = ['Semester']

class Semester(TimeStampedModel):    
    academic_year = models.CharField(max_length=255)
    date_open = models.DateField()
    date_close = models.DateField()
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_semester')
 
    def __str__(self):
        return f"{self.academic_year}"
