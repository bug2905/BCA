from django.shortcuts import render

# Create your views here.

from django.http import HttpResponse

def home(request):
    return HttpResponse("<html>"\
                            "<body bgcolor='#ffe4c4'>" \
                                "<h1>My Name Kushal Shah </h1>" \
                                "<h2>I Am BCA Student</h2>" \
                                "<p>Hi All Of You , How Are You ..? I Hope You All Are Well ...?</p>"\
                            "</body>" \
                        "</html>")
    