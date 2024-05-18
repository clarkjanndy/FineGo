from datetime import datetime
from io import BytesIO
from xhtml2pdf import pisa
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter

import PyPDF2


class PDFGenerator():
    '''this class is dedicated to generate a pdf file using 
    the django template engine and xhtml2pdf library'''

    def __init__(self, template, context):
        '''parameters
            template(django.template.loader.get_template)   : the html template to where we are going to render the data 
            context(json, dict)                             : structured data that we are going to render on the template
        '''
        self.template = template
        self.context = context

    def generate(self, password = None):
        '''a function that will generate the pdf file 
        parameter:
            pdf_destination(str)     : location of the pdf after generation 
            password(str)            : password of the pdf file in case you want to protect it with a password
        return 
            pdf(BytesIO)             : the resulting PDF
        '''
        pdf = BytesIO()
        html = self.template.render(self.context)
        pisa.CreatePDF(BytesIO(html.encode("UTF-8")), dest=pdf)
        pdf.seek(0)
        
        if password:            
            enc_pdf = self.encrypt_pdf(password, pdf)
            return enc_pdf

        return pdf

    def encrypt_pdf(self, password, pdf, pdf_destination='/'):
        '''
        function that will encrypt a pdf file
        parameter:
            pdf_destination(str)     : location of the pdf after generation 
            password(str)            : password of the pdf file in case you want to protect it with a password
            pdf(BytesIO)             : the pdf that will be encrypted
        return 
            encypted_pdf(BytesIO)    : the resulting encrypted PDF
        '''
        try:
            inputpdf = PyPDF2.PdfFileReader(pdf)
            pages_no = inputpdf.numPages
            output = PyPDF2.PdfFileWriter()

            for i in range(pages_no):
                output.addPage(inputpdf.getPage(i))
                output.encrypt(password)

                with open(pdf_destination, "w+b") as outputStream:
                    output.write(outputStream)

            encypted_pdf = open(pdf_destination, "r+b")
            encypted_pdf.seek(0)
            
            return encypted_pdf 
        except Exception as e:
            print(e)
            
    @staticmethod
    def generate_from_html(html):
        '''
        generates a pdf from a given html
        parameter:
            html(str)     : location of the pdf after generation 
        return 
            pdf(BytesIO)  : the resulting PDF
        '''
        pdf = BytesIO()

        if pisa.CreatePDF(BytesIO(html.encode("UTF-8")), dest=pdf).err:
            raise RuntimeError('Error generating pdf')

        pdf.seek(0)
        return pdf

    @staticmethod
    def add_watermark(pdf, watermark_text):
        # Create a PDF reader object for the input PDF
        pdf_reader = PyPDF2.PdfFileReader(pdf)

        # Create a PDF writer object for the output PDF
        pdf_writer = PyPDF2.PdfFileWriter()

        # Generate the a watermark file as a buffer
        water_mark_buffer = BytesIO()
        c = canvas.Canvas(water_mark_buffer, pagesize=letter)
        # Set the color
        c.setFillColor('gray', alpha=0.40)
        # Rotate according to the configured parameter
        c.rotate(45)
        # Position according to the configured parameter
        for i in range(-2, 6):
            y = i * 150
            for j in range(6):
                x = j * 450 
                c.setFont('Helvetica', 50)
                c.drawString(x, y,'CONFIDENTIAL')
                c.setFont('Helvetica', 20)
                c.drawString(x, y - 20, f"{watermark_text} * {str(datetime.now().strftime('%Y-%m-%d'))}")
        c.save()

        # Create a watermark PDF page
        watermark_page = PyPDF2.PdfFileReader(water_mark_buffer).pages[0]

        # Iterate through each page in the input PDF and add the watermark
        for page_num in range(pdf_reader.getNumPages()):
            page = pdf_reader.getPage(page_num)
            page.mergePage(watermark_page)
            pdf_writer.addPage(page)

        # Write the watermarked PDF to the output buffer
        output_buffer = BytesIO()
        pdf_writer.write(output_buffer)

        # Seek to initial
        output_buffer.seek(0)

        return output_buffer
