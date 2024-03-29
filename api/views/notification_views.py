import time
import json

from django.http import StreamingHttpResponse

from rest_framework.generics import ListAPIView, GenericAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from api.serializers import NotificationSerializer
from api.models import Notification
from api.exceptions import ClientError

__all__ = ['NotificationList', 'NotificationMarkRead', 'NotificationMarkReadAll', 'StreamEvent']

class NotificationList(ListAPIView):
    permission_classes = (IsAuthenticated, )
    queryset = Notification.objects.all().order_by('-status', '-created_at')
    serializer_class = NotificationSerializer
    
    def get_queryset(self):
        return super().get_queryset().filter(user = self.request.user)
    
    def get(self, request, *args, **kwargs):
        unseen = self.get_queryset().filter(status='unseen')
        count = unseen.count()
        
        queryset = self.get_queryset()[:5]
        serializer = self.serializer_class(queryset, many=True)

        return Response({
            "status": "success", 
            "data": {
                "count": count,
                "rows": serializer.data
            }
        })
        
class NotificationMarkRead(GenericAPIView):
    permission_classes = (IsAuthenticated, )
    queryset = Notification.objects.all().order_by('-status', '-modified_at')
    serializer_class = NotificationSerializer
    
    def get_queryset(self):
        request = self.request
        return super().get_queryset().filter(user = request.user)
    
    def get_object(self):
        try:
            notif_id = self.kwargs.get('pk')
            obj = self.get_queryset().get(id=notif_id)
        except Notification.DoesNotExist:
            raise ClientError({"message": "Not found"}, 404)
        
        return obj
        
    def post(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.status = 'seen'
        instance.save()
        
        serializer = self.get_serializer(instance)
        
        return Response({
            "status": "success", 
            "data": serializer.data
        })
        
class NotificationMarkReadAll(GenericAPIView):
    permission_classes = (IsAuthenticated, )
    queryset = Notification.objects.all().order_by('-status', '-modified_at')
    serializer_class = NotificationSerializer
    
    def get_queryset(self):
        request = self.request
        return super().get_queryset().filter(user = request.user, status='unseen')
        
    def post(self, request, *args, **kwargs):
        self.get_queryset().update(status='seen')
        serializer = self.get_serializer(self.get_queryset(), many=True)
        return Response({
            "status": "success", 
            "data": serializer.data
        })
        
class StreamEvent(GenericAPIView):
    permission_classes = (IsAuthenticated, )
    queryset = Notification.objects.all().order_by('-status', '-modified_at')
    serializer_class = NotificationSerializer
        
    def get(self, request, *args, **kwargs):
        def event_stream():
            chunk_size = int(request.query_params.get('chunk_size', 5)) # Number of items to fetch per chunk
            delay_between_chunks = 1  # Delay between each chunk in seconds
            
            start_index = 0

            while True:
                # Fetch a chunk of data from the queryset
                queryset_chunk = Notification.objects.all()[start_index:start_index + chunk_size]
                
                if not queryset_chunk:
                    break
                
                # Serialize chunk data to JSON
                serialized_data = NotificationSerializer(queryset_chunk, many=True).data

                # Send JSON data as SSE event
                yield f"data: {json.dumps(serialized_data)}\n\n"
                time.sleep(delay_between_chunks)
                start_index += chunk_size
        response = StreamingHttpResponse(event_stream(), content_type='text/event-stream')
        response['Cache-Control'] = 'no-cache'
        return response
            
    