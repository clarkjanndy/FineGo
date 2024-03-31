import pandas

from django.contrib import messages

from rest_framework.generics import ListCreateAPIView, RetrieveUpdateAPIView, GenericAPIView
from rest_framework.permissions import IsAdminUser, IsAuthenticated, AllowAny
from rest_framework.response import Response

from api.exceptions import ClientError
from api.serializers import UserSerializer, UserImportSerializer
from api.models import User
from api.exceptions import ClientError, ServerError

from api.utils.user_importer import UserImporter
from api.utils.exceptions import InvalidFileHeaderException

__all__ = ['UserListCreate', 'UserImport','UserById', 'UserActivateDeactivate', 'UserMyProfile']

class UserListCreate(ListCreateAPIView):
    permission_classes = (IsAdminUser, )
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        
        messages.success(request, "User created successfully!")
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
        
class UserImport(GenericAPIView):
    permission_classes = (IsAdminUser, )
    serializer_class = UserImportSerializer

    def post(self, request, *args, **kwargs):      
        data = request.data
        serializer = self.serializer_class(data=data)
        serializer.is_valid()
        file = serializer.validated_data['file']
        
        try:
            importer = UserImporter(file=file)
            importer.start_parsing()
            stats = importer.start_import()
            
        except InvalidFileHeaderException as e:
            raise ClientError({"message": str(e)}, 400)
        
        return Response({
            "status": "success",
            "data": stats
        })
         
class UserById(RetrieveUpdateAPIView):
    permission_classes = (AllowAny, )
    queryset = User.objects.all()
    lookup_field='pk'
    serializer_class = UserSerializer

    def get(self, request, *args, **kwargs):
        response = super().get(request, *args, **kwargs)

        return Response({
            "status": "success", 
            "data": response.data
        })
    
    def patch(self, request, *args, **kwargs):
        response = super().patch(request, *args, **kwargs)
        
        messages.success(request, "User updated succesfully!")
        return Response({
            "status": "success", 
            "data": response.data
        })
    
class UserActivateDeactivate(GenericAPIView):
    permission_classes = (IsAdminUser, )
    queryset = User.objects.all()
    lookup_field='pk'
    serializer_class = UserSerializer

    def patch(self, request, *args, **kwargs):
        user = request.user
        instance = self.get_object()
        if instance.pk == user.pk and user.is_active:
            message = "Unable to deactivate current logged in user."
            messages.error(request, message)
            raise ClientError({'message': message})

        # Reverse the current status
        instance.is_active = not instance.is_active
        instance.save()
        
        message = f"User {'activated' if instance.is_active else 'deactivated'} succesfully!"
        messages.success(request, message)
        return Response({
            "status": "success", 
            "data": {
                'message': message
            }
        })


class UserMyProfile(RetrieveUpdateAPIView):
    permission_classes = (IsAuthenticated, )
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_object(self):
        return self.request.user
    
    def patch(self, request, *args, **kwargs):
        data = request.data

        # ignore the value of role passed 
        if 'role' in data:
            data.pop('role')

        # update the object
        user = self.get_object()
        serializer = self.serializer_class(user, data, partial = True, context = {"request": request})
        serializer.is_valid()
        serializer.save()
        
        messages.success(request, "Profile updated succesfully!")
        return Response({
            "status": "success", 
            "data": serializer.data
        })
    
    def get(self, request, *args, **kwargs):
        response = super().get(request, *args, **kwargs)

        return Response({
            "status": "success", 
            "data": response.data
        })
    









        
            