from django.db import models
from django.db.models import Count
from background_task import background

from . extras import TimeStampedModel
from . user import User
from . notification import Notification

__all__ = ['ActivityGroup', 'Activity']

def default_participants():
    participants = User.objects.filter(role='student')
    return participants

@background(schedule=5)
def notify_users_for_activity_changes(activity_id, activity_status):
    # get activity instance
    activity = Activity.objects.filter(id=activity_id).first()
    # check activity
    if not activity:
        return False
    
    notified_user = 0
    participants = activity.group.participants.all()  
    for participant in participants:
        content = f'{activity.group.name} - {activity.name} is now {activity_status}.'
        Notification.objects.create(
            user = participant,
            relation = 'activity',
            content = content,
            link = '/on-going-activities' 
        )
        notified_user += 1
    
    print(f'Successfully notified {notified_user} users for activity changes of {activity.name}')
    return True

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
        ('closing-error', 'Closing Error'),
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
    status = models.CharField(choices=STATUS, max_length=15, default='active')
    fine_amount = models.DecimalField(decimal_places=2, max_digits=10)
    allowed_action = models.CharField(choices=ALLOWED_ACTION, null=True, blank=True, max_length=10)
    
    class Meta:
        verbose_name_plural = 'activities'
    
    def __str__(self):
        return f"{self.name}"
    
    def save(self, *args, **kwargs):
        # check if it is an update to create notification
        if self.pk:
            old_instance = Activity.objects.get(id = self.pk)
            if not old_instance.status == self.status:                     
               notify_users_for_activity_changes(self.pk, self.status)           
               
        super().save(*args, **kwargs)
    
    @property
    def status_color(self):
        MAP = {
            'draft': 'secondary',
            'active': 'primary',
            'open': 'success',
            'closing': 'warning',
            'closing-error': 'danger',
            'closed': 'secondary'            
        }
        return MAP.get(self.status, 'secondary')
    
    @property
    def is_openable(self):
        return self.status in ['active', 'closed']
    
    @property
    def is_closable(self):
        return self.status in ['open', 'closing-error']
        
    @property
    def get_num_attendee_incomplete(self):
        count = self.attendance.filter(time_out__isnull=True).aggregate(count=Count('pk'))['count']
        return count
    
    @property
    def get_num_attendee_complete(self):
        count = self.attendance.filter(time_in__isnull=False, time_out__isnull=False).aggregate(count=Count('pk'))['count']
        return count
    