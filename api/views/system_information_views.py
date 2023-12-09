from django.contrib import messages

from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response

from api.permissions import IsAdminOrReadOnly
from api.serializers import SystemInformationSerializer
from api.models import SystemInformation

__all__ = ['SystemInformationListCreate', 'SystemInformationById']

class SystemInformationListCreate(ListCreateAPIView):
    permission_classes = (IsAdminOrReadOnly, )
    queryset = SystemInformation.objects.all()
    serializer_class = SystemInformationSerializer

    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        
        messages.success(request, f"System information created successfully!")
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
    
class SystemInformationById(RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAdminUser, )
    queryset = SystemInformation.objects.all()
    lookup_field='pk'
    serializer_class = SystemInformationSerializer

    def get(self, request, *args, **kwargs):
        response = super().get(request, *args, **kwargs)

        return Response({
            "status": "success", 
            "data": response.data
        })
    
    def patch(self, request, *args, **kwargs):
        response = super().patch(request, *args, **kwargs)
        
        messages.success(request, "System information updated succesfully!")
        return Response({
            "status": "success", 
            "data": response.data
        })

    def delete(self, request, *args, **kwargs):
        response = super().delete(request, *args, **kwargs)
        msg = 'System information deleted successfully!'
        
        messages.success(request, msg)
        return Response({
            "status": "success", 
            "data": {
                "message": msg
            }
        })