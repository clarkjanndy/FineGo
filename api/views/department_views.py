from django.contrib import messages

from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response

from api.serializers import DepartmentSerializer
from api.models import Department

__all__ = ['DepartmentListCreate', 'DepartmentById']

class DepartmentListCreate(ListCreateAPIView):
    permission_classes = (IsAdminUser, )
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer

    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        
        messages.success(request, "Department created successfully!")
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
    
class DepartmentById(RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAdminUser, )
    queryset = Department.objects.all()
    lookup_field='pk'
    serializer_class = DepartmentSerializer

    def get(self, request, *args, **kwargs):
        response = super().get(request, *args, **kwargs)

        return Response({
            "status": "success", 
            "data": response.data
        })
    
    def patch(self, request, *args, **kwargs):
        response = super().patch(request, *args, **kwargs)
        
        messages.success(request, "Department updated succesfully!")
        return Response({
            "status": "success", 
            "data": response.data
        })

    def delete(self, request, *args, **kwargs):
        response = super().delete(request, *args, **kwargs)
        msg = 'Department deleted successfully!'
        
        messages.success(request, msg)
        return Response({
            "status": "success", 
            "data": {
                "message": msg
            }
        })