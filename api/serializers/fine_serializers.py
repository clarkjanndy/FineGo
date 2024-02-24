from rest_framework import serializers

from . extras import CustomModelSerializer
from api.models import Fine

__all__ = ['FineSerializer']

class FineSerializer(CustomModelSerializer):
    activity_detail = serializers.SerializerMethodField()
    user_detail = serializers.SerializerMethodField()
    amount = serializers.ReadOnlyField()
    
    class Meta:
        model = Fine
        fields = ('id', 'activity_detail', 'user_detail', 'status', 'amount', 'created_at')
        
    def get_activity_detail(self, instance):
        return {
            'group': instance.activity.group.name,
            'activity': instance.activity.name
        }
    
    def get_user_detail(self, instance):
        return {
            'full_name': instance.user.get_full_name
        }