from django.contrib import messages

from rest_framework.viewsets import ViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser

from api import analytics

from api.models import User

__all__ = ['AnalyticsView']

class AnalyticsView(ViewSet):
    queryset = User.objects.all()
    permission_classes = (IsAdminUser, )
    
    @action(methods=['GET'], detail=False, url_path='user-distribution-pie-chart')  
    def user_distribution_pie_chart(self, request):
       data = analytics.user_distribution_pie_chart()
       return Response({
           "type": "success",
           "data": data
       })
       
    @action(methods=['GET'], detail=False, url_path='recent-activity-attendance-pie-chart')  
    def recent_activity_attendance_pie_chart(self, request):
        data = analytics.recent_activity_attendance_pie_chart()
        return Response({
           "type": "success",
           "data": data
       })
    
    @action(methods=['GET'], detail=False, url_path='attendance-and-fines-bar-graph')  
    def attendance_and_fines_bar_graph(self, request):
        data = analytics.attendance_and_fines_bar_graph()
        return Response({
           "type": "success",
           "data": data
       })
        
    
        

    
    
    