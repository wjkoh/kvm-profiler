import os
import sys
sys.path.append(sys.path[0] + '/..')

import datetime
import numpy
import matplotlib.pyplot as pyplot
import json

from django.http import HttpResponse
from django.shortcuts import render_to_response

from graph.models import Measurement

import libvirt_wrapper

def index(request):
    return render_to_response('index.html')


def image(request):
    guests = request.GET.get('guests', '')
    guests = guests.split(',')
    if guests == ['']:
        guests = []
    measure = request.GET.get('measure', None)

    pyplot.clf()
    for guest in guests:
        times = []
        values = []
        # TODO: duration
        measurements = Measurement.objects.filter(guest=guest, measure=measure)
        for measurement in measurements:
            times.append(measurement.time)
            values.append(measurement.value)
        pyplot.plot(times, values, 'o-', label=guest)

    pyplot.xlabel('time')
    pyplot.ylabel('value')
    pyplot.title(measure)
    pyplot.legend()

    tmpfile = os.tmpfile()
    pyplot.savefig(tmpfile, dpi=(640/8))
    
    tmpfile.seek(0)
    data = tmpfile.read()
    tmpfile.close()

    return HttpResponse(data, mimetype="image/png")


def measures(request):
    result = set()
    measurements = Measurement.objects.all()
    for measurement in measurements:
        result.add(measurement.measure)
    return HttpResponse(json.dumps(list(result)), mimetype='application/json')


def guests(request):
    result = set()
    connection = libvirt_wrapper.Connection()
    guests = connection.get_guests()
    for guest in guests:
        result.add(guest.get_name())
    return HttpResponse(json.dumps(list(result)), mimetype='application/json')