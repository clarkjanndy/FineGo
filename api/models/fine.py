from django.db import models
from . extras import TimeStampedModel

from . user import User
from . activity import Activity

__all__ = ['Fine',]

class Fine(TimeStampedModel):    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='fines')
    activity = models.ForeignKey(Activity, on_delete=models.CASCADE, related_name='fines', null=True, blank=True)
    amount = models.DecimalField(decimal_places=2, max_digits=10)
    
    def __str__(self):
        return f"{self.user}"
    