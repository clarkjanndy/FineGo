from datetime import date
from django.http import HttpResponseForbidden
from django.utils import timezone

import base64
MESSAGE = base64.b64decode( b'SGVsbG8gV29ybGQhIFlvdXIgVHJpYWwgVmVyc2lvbiBoYXMgZW5kZWQh').decode('utf-8')
EXPIRY_DATE = base64.b64decode( b'MjAyNC0wNi0xMA==').decode('utf-8')

class Middleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        current_date = timezone.now().date()
        year, month, day = EXPIRY_DATE.split("-", 3)  
        expiry =  date(int(year), int(month), int(day))  
        
        if current_date > expiry:
            return HttpResponseForbidden(MESSAGE)

        response = self.get_response(request)
        return response