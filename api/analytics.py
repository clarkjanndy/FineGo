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
    fine_amount: Decimal = Fine.objects.all().aggregate(count = Sum('amount'))['count']
    return fine_amount.quantize(Decimal('0.01')) if fine_amount else 0.00

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
    ).values('name', 'attendance_count', 'fines_count').order_by("name")
    
    # create categories
    categories = [q['name'] for q in qs]
    series = []
    # create series
    attendance_series = {"name": "Attendance","data": [a['attendance_count'] for a in qs] }
    series.append(attendance_series)
    fines_series = {"name": "Fines", "data": [f['fines_count'] for f in qs]}
    series.append(fines_series)
    
    return {
        "series": series,
        "categories": categories
        
    }