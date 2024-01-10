from django.contrib import messages

from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, RetrieveUpdateAPIView
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError

from api.serializers import ActivityGroupSerializer, ActivitySerializer
from api.models import ActivityGroup, Activity, Attendance, Fine
from api.permissions import IsAdminOrReadOnly

from api.exceptions import SerializerValidationError, ClientError

__all__ = ['ActivityGroupListCreate', 'ActivityGroupById', 'ActivityListCreate', 'ActivityById', 'ActivityClose']

class ActivityGroupListCreate(ListCreateAPIView):
    permission_classes = (IsAdminOrReadOnly, )
    queryset = ActivityGroup.objects.all()
    serializer_class = ActivityGroupSerializer

    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        
        messages.success(request, "Activity group created successfully!")
        return Response({
            "status": "success", 
            "data": response.data
        })
    
    def get(self, request, *args, **kwargs):
        response = super().get(request, *args, **kwargs)

        return Response({
            "status": "success", 
            "data": response.data
        })
    
class ActivityGroupById(RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAdminOrReadOnly, )
    queryset = ActivityGroup.objects.all()
    lookup_field='pk'
    serializer_class = ActivityGroupSerializer

    def get(self, request, *args, **kwargs):
        response = super().get(request, *args, **kwargs)

        return Response({
            "status": "success", 
            "data": response.data
        })
    
    def patch(self, request, *args, **kwargs):
        response = super().patch(request, *args, **kwargs)
        
        messages.success(request, "Activity group updated succesfully!")
        return Response({
            "status": "success", 
            "data": response.data
        })

    def delete(self, request, *args, **kwargs):
        response = super().delete(request, *args, **kwargs)
        msg = 'Activity group deleted successfully!'
        
        messages.success(request, msg)
        return Response({
            "status": "success", 
            "data": {
                "message": msg
            }
        })
        
class ActivityListCreate(ListCreateAPIView):
    permission_classes = (IsAdminOrReadOnly, )
    queryset = Activity.objects.all()
    serializer_class = ActivitySerializer
    
    def get_queryset(self, *args, **kwargs):
        queryset = super().get_queryset()
        return queryset.filter(group = self.kwargs['group'])

    def post(self, request, *args, **kwargs):
        try:
            # get group 
            group = ActivityGroup.objects.filter(pk = kwargs['group']).first()
            if not group:
                raise ValidationError({'group': 'Invalid group'})
            
            serializer = self.serializer_class(data = request.data)
            serializer.is_valid()
            serializer.save(group=group)            
        
            messages.success(request, "Activity created successfully!")
            return Response({
                "status": "success", 
                "data": serializer.data
            })
        
        except SerializerValidationError as err:
            raise err
        
    def get(self, request, *args, **kwargs):
        response = super().get(request, *args, **kwargs)

        return Response({
            "status": "success", 
            "data": response.data
        })
        
class ActivityById(RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAdminOrReadOnly, )
    queryset = Activity.objects.all()
    serializer_class = ActivitySerializer
    allowed_methods = ['GET', 'PATCH', "DELETE"]
    
    def get_queryset(self, *args, **kwargs):
        queryset = super().get_queryset()
        return queryset.filter(group = self.kwargs['group'])
    
    def get_object(self):
        activity = self.get_queryset().filter(pk=self.kwargs['pk']).first()
        if not activity:
            raise ClientError({"message": "Not found"}, 404)
        return activity
            
    def patch(self, request, *args, **kwargs):
        try:
            # get group 
            group = ActivityGroup.objects.filter(pk = kwargs['group']).first()
            if not group:
                raise ValidationError({'group': 'Invalid group'})
            
            instance = self.get_object()
            serializer = self.serializer_class(instance, data = request.data, partial=True)
            serializer.is_valid()
            serializer.save(group=group)            
        
            messages.success(request, "Activity updated successfully!")
            return Response({
                "status": "success", 
                "data": serializer.data
            })
        
        except SerializerValidationError as err:
            raise err
        
    def get(self, request, *args, **kwargs):
        response = super().get(request, *args, **kwargs)

        return Response({
            "status": "success", 
            "data": response.data
        })
        
    def delete(self, request, *args, **kwargs):
        response = super().delete(request, *args, **kwargs)
        msg = 'Activity deleted successfully!'
        
        messages.success(request, msg)
        return Response({
            "status": "success", 
            "data": {
                "message": msg
            }
        })
        
class ActivityClose(ActivityById):
    permission_classes = (IsAdminUser, )
    allowed_methods = ['POST']
    
    def post(self, request, *args, **kwargs):
        activity = self.get_object()
        if not activity.status == 'open':
            messages.error(request, message:='Unable to close activity')
            raise ClientError({"message": message})
        
        activity.status = 'closing'
        activity.save()
        message = 'Activity is now closing.'
        
        try:
            participants = activity.group.participants.all()
            fine_issued = 0
            
            for participant in participants:
                attendance = Attendance.objects.filter(activity=activity, user=participant, time_out__isnull=False).first()
                if not attendance:
                    fine = Fine.objects.get_or_create(user=participant, activity=activity, amount=activity.fine_amount)
                    fine_issued += 1
                    
            activity.status = 'closed'
            message = 'Activity successfully closed.'
            activity.save()
        
        except Exception as err:
            messages.error(request, message:=f'An error has occured while closing activity. {str(err)}')
            raise ClientError({"message": message})
                  
        return Response({
            "status": "success", 
            "data": {
                "message": message,
                "fine_issued": fine_issued
            }
        })
    
    