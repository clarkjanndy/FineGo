from django.contrib import messages

from rest_framework.generics import RetrieveUpdateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from api.serializers import FineSerializer
from api.models import Fine

__all__ = ['FineById']
    
class FineById(RetrieveUpdateAPIView):
    permission_classes = (IsAuthenticated, )
    queryset = Fine.objects.all()
    lookup_field='pk'
    serializer_class = FineSerializer
    
    def get_queryset(self):
        user = self.request.user
        queryset = super().get_queryset()

        if not user.is_superuser:
            return queryset.filter(user=user)
            
        return queryset

    def get(self, request, *args, **kwargs):
        response = super().get(request, *args, **kwargs)

        return Response({
            "status": "success", 
            "data": response.data
        })
    
    def patch(self, request, *args, **kwargs):
        response = super().patch(request, *args, **kwargs)
        data = response.data
        status = data['status']
        
        messages.success(request, f"Fine succesfully marked as {status}.")
        return Response({
            "status": "success", 
            "data": response.data
        })