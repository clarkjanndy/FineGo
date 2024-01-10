from django.db import models
from . extras import TimeStampedModel

from . user import User
from . activity import Activity

__all__ = ['Attendance',]

class Attendance(TimeStampedModel):    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='attendance')
    activity = models.ForeignKey(Activity, on_delete=models.CASCADE, related_name='attendance')
    time_in = models.DateTimeField(auto_now_add=True)
    time_out = models.DateTimeField(blank=True, null=True)
    
    def __str__(self):
        return f"{self.activity.name}"
    