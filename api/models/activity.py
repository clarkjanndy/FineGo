from django.db import models
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
    group = models.ForeignKey(ActivityGroup, on_delete=models.CASCADE, related_name='activities')
    name = models.CharField(max_length=255)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    status = models.CharField(choices=STATUS, max_length=10, default='active')
    
    def __str__(self):
        return f"{self.name}"
    
    class Meta:
        verbose_name_plural = 'activities'
    