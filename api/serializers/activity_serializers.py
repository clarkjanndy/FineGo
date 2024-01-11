from . extras import CustomModelSerializer
from api.models import ActivityGroup, Activity, User

from rest_framework.exceptions import ValidationError

__all__ = ['ActivityGroupSerializer', 'ActivitySerializer']

class ActivityGroupSerializer(CustomModelSerializer):
    class Meta:
        model = ActivityGroup
        fields = '__all__'
        read_only_fields = ('created_by', )
        
    def create(self, validated_data):
        request = self.context.get('request')
        # append current user as creator
        validated_data['created_by'] = request.user
        validated_data['participants'] = User.objects.filter(role='student')
        return super().create(validated_data)
        
class ActivitySerializer(CustomModelSerializer):
    
    def validate(self, attrs):
        attrs = super().validate(attrs)
        start_time = attrs.get('start_time')
        end_time =  attrs.get('end_time')
        
        if start_time and end_time:
            if start_time > end_time:
                raise ValidationError({'start_time': 'Must be earlier than ending date.'})
            
        return attrs
    
    class Meta:
        model = Activity
        fields = '__all__'
        read_only_fields = ('group', )