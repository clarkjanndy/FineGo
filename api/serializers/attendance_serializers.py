
from rest_framework.exceptions import ValidationError
from rest_framework import serializers

from . extras import CustomModelSerializer
from api.models import Attendance, User

__all__ = ['AttendanceSerializer']

class StudentIdRelatedField(serializers.RelatedField):
    def to_representation(self, value):
        return getattr(value, 'student_id')
    
    def to_internal_value(self, value):
        # Convert serialized data back into a related User object
        try:
            return User.objects.get(student_id=value)
        except (ValueError, User.DoesNotExist):
            raise serializers.ValidationError("Invalid Student ID")

class AttendanceSerializer(CustomModelSerializer):
    ACTIONS = (
        ('time-in', 'Time-In'),
        ('time-out', 'Time-Out')
    )
    action = serializers.ChoiceField(choices=ACTIONS, write_only=True)
    user = StudentIdRelatedField(queryset=User.objects.filter(is_superuser=False))
    
    class Meta:
        model = Attendance
        fields = '__all__'   
        read_only_fields = ('time_in', 'time_out'); 
        
    def validate(self, attrs):
        attrs = super().validate(attrs)
        activity = attrs.get('activity')
        user = attrs.get('user')
        partcipants = activity.group.participants.all()
        
        if not user in partcipants:
            raise ValidationError({'message': 'You are not a participant of this activity group.'})        
        
        if not activity.status == 'open':
            raise ValidationError({'activity': 'Activity no longer accepts attendance'})
        
        return attrs