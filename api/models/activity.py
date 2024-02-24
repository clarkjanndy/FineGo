from django.db import models
from django.db.models import Count

from . extras import TimeStampedModel
from . user import User

__all__ = ['ActivityGroup', 'Activity']

def default_participants():
    participants = User.objects.filter(role='student')
    return participants

class ActivityGroup(TimeStampedModel):
    
    STATUS = (
        ('active', 'Active'),
        ('inactive', 'Inactive'),
    )
    name = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    status = models.CharField(choices=STATUS, max_length=10)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_activity_group')
    participants = models.ManyToManyField(User, default=default_participants , related_name='activity_groups')
    
    def __str__(self):
        return f"{self.name}"
    
class Activity(TimeStampedModel):    
    STATUS = (
        ('draft', 'Draft'),
        ('active', 'Active'),
        ('open', 'Open'),
        ('closing', 'Closing'),
        ('closed', 'Closed')
    )
    ALLOWED_ACTION = (
        ('time-in', 'Time-In'),
        ('time-out', 'Time-Out')
    )
    group = models.ForeignKey(ActivityGroup, on_delete=models.CASCADE, related_name='activities')
    name = models.CharField(max_length=255)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    status = models.CharField(choices=STATUS, max_length=10, default='active')
    fine_amount = models.DecimalField(decimal_places=2, max_digits=10)
    allowed_action = models.CharField(choices=ALLOWED_ACTION, null=True, blank=True, max_length=10)
    
    class Meta:
        verbose_name_plural = 'activities'
    
    def __str__(self):
        return f"{self.name}"
    
    @property
    def status_color(self):
        MAP = {
            'draft': 'secondary',
            'active': 'primary',
            'open': 'success',
            'closing': 'warning',
            'closed': 'danger'            
        }
        return MAP.get(self.status, 'secondary')
    
    @property
    def is_openable(self):
        return self.status in ['active', 'closed']
    
    @property
    def is_closable(self):
        return self.status in ['open', 'closing']
        
    @property
    def get_num_attendee_incomplete(self):
        count = self.attendance.filter(time_out__isnull=True).aggregate(count=Count('pk'))['count']
        return count
    
    @property
    def get_num_attendee_complete(self):
        count = self.attendance.filter(time_in__isnull=False, time_out__isnull=False).aggregate(count=Count('pk'))['count']
        return count
    