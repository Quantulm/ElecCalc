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
from .models import Question
import numpy as np
import lectureformat.scripts as s


# Create your views here.
def home(request):
    return render(request, "home.html")

def calculator(request):
    return render(request, "calculator.html")

def toymodel(request):
    num = request.POST['num_stud']
    lec_type = request.POST['lec_type']

    def toymodel(sel_num_stud, lec_type):
        # Just a simple dummy toy model.
        # Ideally this function would be imported from our external model library
        num_students = np.linspace(0, 500, 50)
        baseline = np.full_like(num_students, 174000+500000)
        lighting = 68000
        energy_std = lighting + lec_type * num_students * 50
        server = 60000
        energy_on =server+ 10 * num_students + 1.0 * num_students * 50

        c_hyb = [0.2, 0.4, 0.6, 0.8]
        energ_cons = []
        for c in c_hyb:
            energ_cons.append(c*energy_on + (1-c)*energy_std)
        breakeven = 30 # Simplification, not really good
        
        if sel_num_stud < num_students[breakeven]:
            res = "Online"
        else:
            res = "On-Site"
        
        fig = plt.figure()
        for c in c_hyb:
            plt.plot(num_students, c*energy_on + (1-c)*energy_std, label=r"C$_{online}$=%s" % str(c))
        ymin = plt.gca().get_ylim()[0]
        ymax = plt.gca().get_ylim()[1]
        plt.vlines(sel_num_stud, ymin, ymax, label="Selected number of students", color="red", linestyle="--")
        plt.vlines(num_students[breakeven], ymin, ymax, label="Breakeven", color="black", linestyle=":")
        plt.fill_between([num_students[breakeven]*0.9, num_students[breakeven]*1.1], ymin, y2=ymax, color="black", alpha=0.3, label="10% tolerance")

        plt.xlabel("Number of Students")
        plt.ylabel("Energy consumption (kWh)")
        plt.legend()
        plt.title("Hybrid lectures")

        imgdata = io.StringIO()
        fig.savefig(imgdata, format='svg')
        imgdata.seek(0)

        data = imgdata.getvalue()
        
        return data, res

    if num.isdigit() and lec_type.isdigit():
        num = int(num)
        lec_type = int(lec_type)/100
        data, res = toymodel(num, lec_type)
        context = {}
        context['graph'] = data
        context['result'] = res
        return render(request, 'result.html', context)

    else:
        res = "Only digits are allowed"
        return render(request, "result.html", {"result": res})

def lectureformat(request):
    num = request.POST['num_stud']
    lec_type = request.POST['lec_type']
    season = request.POST['season']



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
