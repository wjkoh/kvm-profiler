import os
from django.http import HttpResponse
from django.shortcuts import render_to_response
from pygooglechart import SimpleLineChart
from pygooglechart import Axis

def index(request):
    return render_to_response('index.html')


def image(request):
    # Set the vertical range from 0 to 50
    max_y = 50
    chart = SimpleLineChart(200, 125, y_range=[0, max_y])

    # First value is the highest Y value. Two of them are needed to be
    # plottable.
    chart.add_data([max_y] * 2)

    # 3 sets of real data
    chart.add_data([28, 30, 31, 33, 35, 36, 42, 48, 43, 37, 32, 24, 28])
    chart.add_data([16, 18, 18, 21, 23, 23, 29, 36, 31, 25, 20, 12, 17])
    chart.add_data([7, 9, 9, 12, 14, 14, 20, 27, 21, 15, 10, 3, 7])

    # Last value is the lowest in the Y axis.
    chart.add_data([0] * 2)

    # Black lines
    chart.set_colours(['000000'] * 5)

    # Filled colours
    # from the top to the first real data
    chart.add_fill_range('76A4FB', 0, 1)

    # Between the 3 data values
    chart.add_fill_range('224499', 1, 2)
    chart.add_fill_range('FF0000', 2, 3)

    # from the last real data to the
    chart.add_fill_range('80C65A', 3, 4)

    # Some axis data
    chart.set_axis_labels(Axis.LEFT, ['', max_y / 2, max_y])
    chart.set_axis_labels(Axis.BOTTOM, ['Sep', 'Oct', 'Nov', 'Dec'])

    # TODO: we should draw the chart dynamically
    
    name = os.tempnam()
    chart.download(name)
    data = open(name).read()
    os.remove(name)

    return HttpResponse(data, mimetype="image/png")
