from django.db import models
from . extras import TimeStampedModel

from . user import User
from . activity import Activity

__all__ = ['Fine',]

class Fine(TimeStampedModel):    
    STATUS = (
        ('paid', 'Paid'),
        ('unpaid', 'Unpaid'),
        ('removed', 'Removed')
    )
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='fines')
    activity = models.ForeignKey(Activity, on_delete=models.CASCADE, related_name='fines', null=True, blank=True)
    amount = models.DecimalField(decimal_places=2, max_digits=10)
    status = models.CharField(max_length=8, default='unpaid', choices=STATUS)
    
    def __str__(self):
        return f"{self.user}"
    