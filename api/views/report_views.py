from django.http import HttpResponse
from django.template.loader import get_template

from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAdminUser

from api.utils.pdf_generator import PDFGenerator
from api.utils.constants import base_64_finego_logo, base_64_bcc_logo
from api.analytics import fine_reports


__all__ = ['ReportPDF']

class ReportPDF(GenericAPIView):
    permission_classes = (IsAdminUser, )
    
    def get(self, request, *args, **kwargs):
        template = get_template('api/report.html')
        data = fine_reports()
        context = {
            'data': data,
            'base_64_finego_logo': base_64_finego_logo,
            'base_64_bcc_logo': base_64_bcc_logo
        }
        
        generator = PDFGenerator(template, context)
        pdf = generator.generate()
        
        response = HttpResponse(content=pdf.read(), content_type='application/pdf')
        response['Content-Disposition'] = 'filename="report.pdf"'
        
        return response

        