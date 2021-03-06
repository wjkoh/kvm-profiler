import os
import sys
sys.path.append(sys.path[0] + '/..')

import numpy
import matplotlib.pyplot as pyplot
import json
import datetime

from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.db.models import F
from django.db.models.aggregates import Max

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
    duration = int(request.GET.get('duration', 100))

    pyplot.clf()
    for guest in guests:
        times = []
        values = []

        measurements = Measurement.objects.filter(guest=guest, measure=measure)
        maxTime = datetime.datetime(1900, 1, 1)
        for measurement in measurements:
            if maxTime < measurement.time:
                maxTime = measurement.time

        minTime = maxTime - datetime.timedelta(seconds=duration)
        
        for measurement in measurements:
            if minTime <= measurement.time:
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
    measurements = Measurement.objects.values('measure').distinct()
    for measurement in measurements:
        print measurement
        result.add(measurement['measure'])
    return HttpResponse(json.dumps(list(result)), mimetype='application/json')


def guests(request):
    result = set()
    connection = libvirt_wrapper.Connection()
    guests = connection.get_guests()
    for guest in guests:
        result.add(guest.get_name())
    return HttpResponse(json.dumps(list(result)), mimetype='application/json')


def threat_llc_loads(request):
    measure = 'CPU_MEM/LLC-loads'
    max_time = Measurement.objects.aggregate(Max('time'))['time__max']
    measurements = Measurement.objects.filter(measure='CPU_MEM/LLC-loads', time=max_time)
    total_value = 0
    max_value = 0
    guest = None
    for measurement in measurements:
        total_value += measurement.value
        if max_value < measurement.value:
            max_value = measurement.value
            guest = measurement.guest
    return HttpResponse(json.dumps({'value': total_value, 'max_guest': guest}), mimetype='application/json')
