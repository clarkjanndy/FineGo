from django.views.generic import TemplateView
from .custom_mixins import AdminRequiredMixin
from api import analytics

__all__ = ['DashboardView']

class DashboardView(AdminRequiredMixin, TemplateView):
    template_name = 'client/admin/dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['current_page'] =  'admin-dashboard'
        
        # add analytics data
        user_count = analytics.user_count()
        activity_count = analytics.activity_count()
        on_going_activities, on_going_activity_count = analytics.activity_count(on_going_only=True, return_objects=True)
        fine_issued = analytics.fine_issued()
        fines_per_activity_group = analytics.fines_per_activity_group()
        attendance_recent = analytics.attendance_recent()
        
        context['user_count'] =  user_count
        context['activity_count'] =  activity_count
        context['on_going_activity_count'] =  on_going_activity_count
        context['on_going_activities'] =  on_going_activities
        context['fine_issued'] =  fine_issued 
        context['fines_per_activity_group'] =  fines_per_activity_group 
        context['attendance_recent'] = attendance_recent

        return context