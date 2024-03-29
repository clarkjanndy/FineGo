from . extras import CustomModelSerializer
from api.models import Notification

__all__ = ['NotificationSerializer']

class NotificationSerializer(CustomModelSerializer):
    class Meta:
        model = Notification
        fields = ('relation', 'content', 'link', 'status', 'created_at')