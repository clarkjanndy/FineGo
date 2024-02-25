from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from api.serializers import NotificationSerializer
from api.models import Notification

__all__ = ['NotificationList']

class NotificationList(ListAPIView):
    permission_classes = (IsAuthenticated, )
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer
    
    def get_queryset(self):
        queryset = super().get_queryset().filter(user = self.request.user)
        return queryset
    
    def get(self, request, *args, **kwargs):
        response = super().get(request, *args, **kwargs)

        return Response({
            "status": "success", 
            "data": response.data
        })