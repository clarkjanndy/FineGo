from . extras import CustomModelSerializer
from api.models import Department

__all__ = ['DepartmentSerializer']

class DepartmentSerializer(CustomModelSerializer):
    class Meta:
        model = Department
        fields = '__all__'