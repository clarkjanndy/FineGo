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
    
    @property
    def total_time(self):
        if not self.time_out:
            return f'0 hours, 0 minutes'
        
        total_time = self.time_out - self.time_in
        total_seconds = total_time.total_seconds()
        
        if total_seconds < 0:
            return f'0 hours, 0 minutes'
                    
        hours, remainder = divmod(total_seconds, 3600)
        minutes, _ = divmod(remainder, 60)
        
        return f'{int(hours)} hours, {int(minutes)} minutes'


        
        
    