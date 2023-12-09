from rest_framework.exceptions import ValidationError, APIException
from rest_framework import status

from django.utils.translation import gettext_lazy as _


__all__ = ['SerializerValidationError', 'AuthenticationFailed', 'ClientError']

class SerializerValidationError(ValidationError):
    '''
    Custom exception for serializer field validation. Normally raised during field valdiation in serializers.    
    Note: Do not use in raising validation error.
    Always use ValidationError when overriding validate method.
    '''
   
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = _('Invalid input.')

    def __init__(self, detail=default_detail, status_code=status_code):       
        self.detail = {
            'status': 'failed',
            'data': detail,
        }       
        self.status_code = status_code

class ClientError(APIException):
    '''
    Custom exception for client-side related errors.
    '''
    
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = _('Invalid request.')

    def __init__(self, detail=default_detail, status_code=status_code):
        self.detail = {
            'status': 'failed',
            'data': detail,
        }
        self.status_code = status_code 

class AuthenticationFailed(APIException):

    status_code = status.HTTP_401_UNAUTHORIZED
    default_detail = _('Invalid username and/or password.')

    def __init__(self, detail=default_detail, status_code=status_code):       
        self.detail = {
            'status': 'failed',
            'data': detail,
        }       
        self.status_code = status_code
    
    