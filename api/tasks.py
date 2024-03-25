from background_task import background
from api.models import Fine, Notification, User, Attendance, Activity

@background(schedule=5)
def issue_fines(activity_id):
    # get activity instance
    activity = Activity.objects.filter(id=activity_id).first()
    # check activity
    if not activity:
        return False
    
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
    return True