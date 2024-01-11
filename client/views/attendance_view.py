from typing import Any
from django.db.models import Q
from django.db.models.query import QuerySet
from django.views.generic import ListView, TemplateView, DetailView

from api.models import  Activity

from . custom_mixins import LoginRequiredMixin

__all__ = ['AttendanceWindow',] 
    
class AttendanceWindow(LoginRequiredMixin, DetailView): 
    model = Activity
    template_name = 'client/attendance-window.html'
    context_object_name = 'activity'
    
    def get_queryset(self):
        return super().get_queryset().filter(status='open')

    
