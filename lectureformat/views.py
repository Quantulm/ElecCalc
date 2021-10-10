from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse
from django.template import loader
import matplotlib.pyplot as plt
from matplotlib import pylab
from pylab import *
import matplotlib
import io
import urllib, base64
from PIL import Image
import numpy as np
import lectureformat.scripts as s

from .models import LectureHall
from .models import Faculty


# Create your views here.
def home(request):
    return render(request, "home.html")

def calculator(request):
    lecture_hall_list = LectureHall.objects.order_by('hall_name')
    faculty_list = Faculty.objects.order_by('faculty_name')
    template = loader.get_template('calculator.html')
    context = {
        'lecture_hall_list': lecture_hall_list,
        'faculty_list': faculty_list,
    }
    return HttpResponse(template.render(context, request))
    #return render(request, "calculator.html")


def lectureformat(request):
    num = request.POST['num_stud']
    lec_type = request.POST['lec_type']
    season = request.POST['season']
    lecture_hall = get_object_or_404(LectureHall, pk=request.POST['lecture_halls'])



    if num.isdigit() and lec_type.isdigit() and season.isdigit():
        if season != 0 or season != 1:
            # Default to winter if wrong season is specified
            season = 0
        num = int(num)
        lec_type = int(lec_type)/100
        data, res = s.toycalc(num, lec_type, season)
        context = {}
        context['graph'] = data
        context['result'] = res
        context['hall'] = lecture_hall
        return render(request, 'result.html', context)

    else:
        res = "Only digits are allowed"
        return render(request, "result.html", {"result": res})


def result(request):
    def return_graph():

        x = np.arange(0,np.pi*3,.1)
        y = np.sin(x)

        fig = plt.figure()
        plt.plot(x,y)

        imgdata = io.StringIO()
        fig.savefig(imgdata, format='svg')
        imgdata.seek(0)

        data = imgdata.getvalue()
        return data

    context = {'graph' : []}
    context['graph'] = return_graph()
    context['result'] = str(5000)
    return render(request, 'result.html', context)