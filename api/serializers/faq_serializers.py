from . extras import CustomModelSerializer
from api.models import FAQ

__all__ = ['FAQSerializer']

class FAQSerializer(CustomModelSerializer):
    class Meta:
        model = FAQ
        fields = '__all__'