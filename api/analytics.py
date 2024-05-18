from decimal import Decimal
from django.db.models import Count, Sum, F

from api.models import User, Activity, Fine, Department, Attendance

def user_count(is_admin_included: bool = False):
    user_count = User.objects.filter(is_superuser = is_admin_included).aggregate(count = Count('id'))['count']
    return user_count

def activity_count(on_going_only: bool = False, return_objects = False):
    activities = Activity.objects.all()
    if on_going_only:
        activities = activities.filter(status__in =['open', 'closing-error']) 
    activity_count = activities.aggregate(count = Count('id'))['count']
    
    if return_objects:
        return activities, activity_count
    
    return activity_count

def fine_issued():
    fine_amount: Decimal = Fine.objects.exclude(status='removed').aggregate(count = Sum('amount'))['count']
    return fine_amount.quantize(Decimal('0.01')) if fine_amount else 0.00

def fines_per_activity_group(num_rows=10):
    queryset = Fine.objects.select_related('activity').\
               values('activity__group').\
               annotate(fines = Sum('amount')).\
               values('activity__group__id', 'activity__group__name', 'fines')[:num_rows]

    return queryset 

def attendance_recent(num_rows=10):
    if not num_rows:
        return []
    
    return Attendance.objects.all().order_by('-modified_at')[:num_rows]

def user_distribution_pie_chart():
    grouped_users = Department.objects.prefetch_related('members').annotate(
        member_count = Count('members')
    ).values_list("abbreviation", "member_count")
    
    data = {
        "labels": [item[0] for item in grouped_users],
        "series": [item[1] for item in grouped_users],
    }
    return data
    
def attendance_and_fines_bar_graph():
    qs = Department.objects.prefetch_related(
        'members'
    ).annotate(
        attendance_count = Count('members__attendance'),
        fines_count = Count('members__fines'),        
    ).values('abbreviation', 'attendance_count', 'fines_count').order_by("abbreviation")
    
    # create categories
    categories = [q['abbreviation'] for q in qs]
    series = []
    # create series
    attendance_series = {"name": "Attendance","data": [a['attendance_count'] for a in qs], "color": '#0d6efd'}
    series.append(attendance_series)
    fines_series = {"name": "Fines", "data": [f['fines_count'] for f in qs], "color": "#dc3545"}
    series.append(fines_series)
    
    return {
        "series": series,
        "categories": categories
        
    }    

def fine_reports():
    paid_fines = Fine.objects.filter(status='paid').\
        values('user').annotate(
            fine_amount = Sum('amount'), 
            full_name = User.full_name_query(),
            student_id = F('user__student_id')
        ).values('student_id', 'full_name', 'fine_amount' )
        
    unpaid_fines = Fine.objects.filter(status='unpaid').\
        values('user').annotate(
            fine_amount = Sum('amount'), 
            full_name = User.full_name_query(),
            student_id = F('user__student_id')
        ).values('student_id', 'full_name', 'fine_amount' )
    
   
    total_paid_fine = paid_fines.aggregate(amount=Sum('fine_amount'))['amount'] or Decimal(0)
    total_unpaid_fine = unpaid_fines.aggregate(amount=Sum('fine_amount'))['amount'] or Decimal(0)
    total_fine = total_paid_fine + total_unpaid_fine
    
    return {
        'paid_fines': paid_fines,
        'unpaid_fines': unpaid_fines,
        'aggregates':{
            'total_paid_fine': total_paid_fine,
            'total_unpaid_fine': total_unpaid_fine,
            'total_fine': total_fine
        }
    }
    
def recent_activity_attendance_pie_chart():
    open_activity = Activity.objects.filter(status='open').order_by('-modified_at').first()
    
    if not open_activity:
        return {}
    
    qs = Department.objects.prefetch_related(
        'members'
    ).filter(
        members__attendance__activity = open_activity
    ).annotate(
        attendance_count = Count('members__attendance'),     
    ).values('abbreviation', 'attendance_count',).order_by("abbreviation")
    
    data = {
        "labels": [item['abbreviation'] for item in qs],
        "series": [item['attendance_count'] for item in qs],
        "activity_name": f"{open_activity.group.name} - {open_activity.name}"
    }
    
    return data
    
    