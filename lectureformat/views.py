from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse, Http404
from django.template import loader
from django.utils.datastructures import MultiValueDictKeyError

import matplotlib.pyplot as plt
from matplotlib import pylab
from pylab import *
import matplotlib
import io
import urllib, base64
from PIL import Image
import numpy as np
import lectureformat.scripts as s

from .lecture import *
from .models import *

# Create your views here.
def home(request):
    return render(request, "home.html")


def calculator_home(request):
    university_list = University.objects.order_by("university_name")

    template = loader.get_template("calculator_home.html")
    context = {
        "university_list": university_list,
    }

    return HttpResponse(template.render(context, request))


def calculator_base_selection(request):
    # Get and save university
    university = get_object_or_404(University, pk=request.POST["universitys"])
    request.session["university"] = university.id

    # Create lists for parameters to be selected
    faculty_list = Faculty.objects.filter(university=university).order_by(
        "faculty_name"
    )
    lecture_hall_list = LectureHall.objects.filter(university=university).order_by(
        "hall_name"
    )
    streaming_list = StreamingService.objects.order_by("streaming_name")
    vod_list = VideoOnDemandService.objects.order_by("vod_name")

    template = loader.get_template("calculator_base_selection.html")
    context = {
        "university": university,
        "faculty_list": faculty_list,
        "lecture_hall_list": lecture_hall_list,
        "streaming_list": streaming_list,
        "vod_list": vod_list,
    }
    return HttpResponse(template.render(context, request))


def calculator_option_selection(request):
    # Get and save answers
    request.session["num"] = request.POST["num_stud"]
    try:
        faculty = get_object_or_404(Faculty, pk=request.POST["facultys"])
        request.session["faculty"] = faculty.id
        faculty_name = faculty.faculty_name
    except:
        raise Http404("No valid faculty found")

    try:
        lecture_hall = get_object_or_404(LectureHall, pk=request.POST["lecture_halls"])
        lecture_hall_name = lecture_hall.hall_name
        request.session["lecture_hall"] = lecture_hall.id
    except:
        request.session["lecture_hall"] = None
        lecture_hall_name = "None"

    try:
        streaming = get_object_or_404(StreamingService, pk=request.POST["streaming"])
        streaming_name = streaming.streaming_name
        request.session["streaming"] = streaming.id
    except:
        request.session["streaming"] = None
        streaming_name = "None"

    try:
        vod = get_object_or_404(VideoOnDemandService, pk=request.POST["vod"])
        vod_name = vod.vod_name
        request.session["vod"] = vod.id
    except:
        request.session["vod"] = None
        vod_name = "None"

    template = loader.get_template("calculator_option_selection.html")
    context = {
        "university": University.objects.get(
            pk=request.session.get("university")
        ).university_name,
        "num": request.session.get("num"),
        "faculty": faculty_name,
        "lecture_hall": lecture_hall_name,
        "streaming": streaming_name,
        "vod": vod_name,
    }

    return HttpResponse(template.render(context, request))


options = ["random_living", "random_devices", "option1"]


def calculator_result_selection(request):
    # Get option selections an save them
    sampling = request.POST["sampling"]
    request.session["sampling"] = sampling

    template = loader.get_template("calculator_result_selection.html")
    context = {
        "university": University.objects.get(
            pk=request.session.get("university")
        ).university_name,
        "faculty": Faculty.objects.get(pk=request.session.get("faculty")).faculty_name,
        "num": request.session.get("num"),
    }
    if request.session.get("lecture_hall") is not None:
        context["lecture_hall"] = LectureHall.objects.get(
            pk=request.session.get("lecture_hall")
        ).hall_name
    else:
        context["lecture_hall"] = "None"
    if request.session.get("streaming") is not None:
        context["streaming"] = StreamingService.objects.get(
            pk=request.session.get("streaming")
        ).streaming_name
    else:
        context["streaming"] = "None"
    if request.session.get("vod") is not None:
        context["vod"] = VideoOnDemandService.objects.get(
            pk=request.session.get("vod")
        ).vod_name
    else:
        context["vod"] = "None"

    context["sampling"] = sampling

    opts = []
    for option in options:
        try:
            tmp = request.POST[option]
            opts.append(tmp)
        except:
            tmp = None
        request.session[option] = tmp

    context["options"] = ", ".join(opts)

    return HttpResponse(template.render(context, request))


def calculator_result(request):

    mode = request.POST["action"]
    if mode == "Offline":
        mode = "offline"
    elif mode == "Online - Streaming":
        mode = "online-streaming"
    elif mode == "Online - VoD":
        mode = "online-vod"
    elif mode == "Hybrid - Streaming":
        mode = "hybrid-streaming"
    elif mode == "Hybrid - VoD":
        mode = "hybrid-vod"
    else:
        raise ValueError("Specified mode not supported")

    university = University.objects.get(pk=request.session.get("university"))
    faculty = Faculty.objects.get(pk=request.session.get("faculty"))
    num_stud = request.session.get("num")
    sampling = request.session.get("sampling")

    context = {
        "university": university.university_name,
        "faculty": faculty.faculty_name,
        "num": num_stud,
        "sampling": sampling,
        "mode": mode,
    }
    if request.session.get("lecture_hall") is not None:
        lecture_hall = LectureHall.objects.get(pk=request.session.get("lecture_hall"))
        context["lecture_hall"] = lecture_hall.hall_name
    else:
        lecture_hall = None
        context["lecture_hall"] = "None"
    if request.session.get("streaming") is not None:
        streaming = StreamingService.objects.get(pk=request.session.get("streaming"))
        context["streaming"] = streaming.streaming_name
    else:
        streaming = None
        context["streaming"] = "None"
    if request.session.get("vod") is not None:
        vod = VideoOnDemandService.objects.get(pk=request.session.get("vod"))
        context["vod"] = vod.vod_name
    else:
        vod = None
        context["vod"] = "None"

    opts = []
    for option in options:
        if request.session.get(option) is not None:
            opts.append(request.session.get(option))

    context["options"] = ", ".join(opts)

    lecture = Lecture(
        num_stud=int(num_stud),
        hall=lecture_hall,
        streaming=streaming,
        vod=vod,
        university=university,
        faculty=faculty,
        living=None,
        device=None,
        transport=None,
        options=opts,
    )

    consumption, stat_uncertainty = lecture.get_consumption(mode, sampling.lower())
    context["consumption"] = "{:.2f} +/- {:.2f} kWh".format(
        consumption, stat_uncertainty
    )
    return render(request, "calculator_result.html", context)


# def lectureformat(request):
#    num = request.POST["num_stud"]
#    lec_type = request.POST["lec_type"]
#    season = request.POST["season"]
#    lecture_hall = get_object_or_404(LectureHall, pk=request.POST["lecture_halls"])
#
#    a = LectureHall.objects.all()
#
#    if num.isdigit() and lec_type.isdigit() and season.isdigit():
#        if season != 0 or season != 1:
#           # Default to winter if wrong season is specified
#            season = 0
#        num = int(num)
#        lec_type = int(lec_type) / 100
#        data, res = s.toycalc(num, lec_type, season)
#        context = {}
#        context["graph"] = data
#        context["result"] = a[0].test()
#        context["hall"] = lecture_hall
#        return render(request, "result.html", context)
#
#    else:
#        res = "Only digits are allowed"
#        return render(request, "result.html", {"result": res})


# def result(request):
#    def return_graph():
#
#        x = np.arange(0, np.pi * 3, 0.1)
#        y = np.sin(x)
#
#        fig = plt.figure()
#        plt.plot(x, y)
#
#        imgdata = io.StringIO()
#        fig.savefig(imgdata, format="svg")
#        imgdata.seek(0)
#
#        data = imgdata.getvalue()
#        return data
#
#    context = {"graph": []}
#    context["graph"] = return_graph()
#    context["result"] = str(5000)
#    return render(request, "result.html", context)
