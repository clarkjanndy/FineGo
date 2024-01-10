from django.utils import timezone
from django.contrib import messages

from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.serializers import ValidationError

from api.serializers import AttendanceSerializer
from api.models import Attendance

from api.exceptions import SerializerValidationError, ClientError

__all__ = ['AttendanceCreate', ]

class AttendanceCreate(CreateAPIView):
    permission_classes = (IsAuthenticated, )
    queryset = Attendance.objects.all()
    serializer_class = AttendanceSerializer

    def post(self, request, *args, **kwargs):
        data = request.data
        user = request.user
        
        serializer = self.serializer_class(data=data, context={"request": request})
        serializer.is_valid()
        validated_data = serializer.validated_data
        
        if validated_data['action'] == 'time_in':
            attendance, created = Attendance.objects.get_or_create(activity=validated_data['activity'], user=user )
            if not created:
                message = 'You already Time-In.'
                raise ClientError({'message': message})
            
            message = 'Time-In success.'
           
        else:
            attendance =  Attendance.objects.filter(activity=validated_data['activity'], user=user).first()
            if not attendance:
                message = 'Unable to time-out'
                raise ClientError({'message': message})
            
            if attendance.time_out:
                message = 'You already Time-out.'   
                raise ClientError({'message': message})
             
            attendance.time_out = timezone.now()
            attendance.save()
            message = 'Time-Out success.'
          
        data = self.serializer_class(attendance).data
        data['message'] = message
        return Response({
            "status": "success", 
            "data": data
        })
                
     
        
        