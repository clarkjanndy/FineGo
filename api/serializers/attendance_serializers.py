
from rest_framework.exceptions import ValidationError
from rest_framework import serializers

from . extras import CustomModelSerializer
from api.models import Attendance

__all__ = ['AttendanceSerializer']

class AttendanceSerializer(CustomModelSerializer):
    ACTIONS = (
        ('time_in', 'Time-In'),
        ('time_out', 'Time-Out')
    )
    action = serializers.ChoiceField(choices=ACTIONS, write_only=True)
    
    class Meta:
        model = Attendance
        fields = '__all__'   
        read_only_fields = ('user', 'time_in', 'time_out'); 
        
    def validate(self, attrs):
        request = self.context.get('request')
        attrs = super().validate(attrs)
        activity = attrs.get('activity')
        partcipants = activity.group.participants.all()
        
        if not request.user in partcipants:
            raise ValidationError({'message': 'You are not a participant of this activity group.'})        
        
        if not activity.status == 'active':
            raise ValidationError({'activity': 'Activity no longer accepts attendance'})
        
        return attrs