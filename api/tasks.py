from background_task import background
from api.models import Fine, Notification, User, Attendance, Activity

@background(schedule=5)  
def notify_user_for_issued_fine(fine_id):
    fine = Fine.objects.select_related('activity', 'user').get(id = fine_id)
    notification = Notification.objects.create(
        user = fine.user,
        relation = 'fine',
        content = f'''
        You have been issued an amount of {fine.amount} pesos for not attending 
        {fine.activity.group.name} - {fine.activity.name}.
        '''
    )
    print(f'Successfully notified user {notification.user} for fine issued.')
  

@background(schedule=5)
def issue_fines(activity_id):
    # get activity instance
    activity = Activity.objects.get(id=activity_id)
    # get activity participants
    participants = activity.group.participants.all()
   
    fine_issued = 0
    try:
        # loop all participants and check if they
        for participant in participants:
            # check if they have attendance
            attendance = Attendance.objects.filter(activity=activity, user=participant, time_out__isnull=False).first()
            if not attendance:
                fine, created = Fine.objects.get_or_create(user=participant, activity=activity, amount=activity.fine_amount)
                if created:
                    notify_user_for_issued_fine(fine.id, verbose_name="Notify User For Issued Fine")
                    fine_issued += 1
                    
        # set status to closed after successfull issuance
        activity.status = 'closed'
        activity.allowed_action = None
        activity.save()  
        
    except:
        # set status to closing-error if something happens
        activity.status = 'closing-error'
        activity.allowed_action = None
        activity.save()  
                
    print(f'Successfully issued {fine_issued} fines for activity {activity.name}')
  
