from rest_framework import serializers

from api.exceptions import SerializerValidationError

__all__ = ['CustomSerializer', 'CustomModelSerializer']

class CustomSerializer(serializers.Serializer):
    '''
    Custom Serializer class that will return only the first error of a field during validation.
    '''
    
    def is_valid(self, *, raise_exception = False):
        if not super().is_valid(): # call the method from the parent class
            errors = {}
            for field, field_errors in self.errors.items():
                errors[field] = field_errors[0]  # only include the first error message for each field

            raise SerializerValidationError(errors, 400)

class CustomModelSerializer(serializers.ModelSerializer, CustomSerializer):
    '''
    Custom ModelSerializer class that will return only the first error of a field during validation.
    '''
    
    class Meta:
        pass