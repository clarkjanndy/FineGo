from django.contrib import messages

from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response

from api.permissions import IsAdminOrReadOnly
from api.serializers import FAQSerializer
from api.models import FAQ

__all__ = ['FAQListCreate', 'FAQById']

class FAQListCreate(ListCreateAPIView):
    permission_classes = (IsAdminOrReadOnly, )
    queryset = FAQ.objects.all()
    serializer_class = FAQSerializer

    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        
        messages.success(request, "FAQ entry created successfully!")
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
    
class FAQById(RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAdminUser, )
    queryset = FAQ.objects.all()
    lookup_field='pk'
    serializer_class = FAQSerializer

    def get(self, request, *args, **kwargs):
        response = super().get(request, *args, **kwargs)

        return Response({
            "status": "success", 
            "data": response.data
        })
    
    def patch(self, request, *args, **kwargs):
        response = super().patch(request, *args, **kwargs)
        
        messages.success(request, "FAQ entry updated succesfully!")
        return Response({
            "status": "success", 
            "data": response.data
        })

    def delete(self, request, *args, **kwargs):
        response = super().delete(request, *args, **kwargs)
        msg = 'FAQ entry deleted successfully!'
        
        messages.success(request, msg)
        return Response({
            "status": "success", 
            "data": {
                "message": msg
            }
        })