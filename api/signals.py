from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver

from .models import Fine, Notification

@receiver(post_save, sender=Fine)
def fine_post_save(sender, instance=None, created=False, **kwargs):
    # create
    if created:
         Notification.objects.create(
            user = instance.user,
            relation = 'fine',
            content = f'You have been issued an amount of {instance.amount} pesos for not attending {instance.activity.group.name} - {instance.activity.name}.',
            link = '/my-fines'        
        )
        
    # update
    else:
        Notification.objects.create(
            user = instance.user,
            relation = 'fine',
            content = f'Your fine for not attending {instance.activity.group.name} - {instance.activity.name} has been moved to {instance.status}.',
            link = '/my-fines' 
        )
       
        