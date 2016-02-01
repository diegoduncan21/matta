from django.http import HttpResponse
from django.conf import settings


def cv(request):
    with open('matta/static/images/cv.pdf', 'rb') as pdf:
        response = HttpResponse(pdf.read(), content_type='application/pdf')
        response['Content-Disposition'] = 'inline;filename=cv.pdf'
        return response
    pdf.closed