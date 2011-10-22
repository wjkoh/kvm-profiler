from pyrrd.rrd import DataSource, RRA, RRD
import time
import datetime

class rrd_writer:
    def __init__(self, dom_lst):
        self.start_ut = int(time.mktime(datetime.datetime.now().timetuple())) - 1
        self.end_ut = 0
        self.dataSources = []

        filename = './test.rrd'
        roundRobinArchives = []
        for d in dom_lst:
            dataSource = DataSource(dsName=d, dsType='COUNTER', heartbeat=2)
            self.dataSources.append(dataSource)

        roundRobinArchives.append(RRA(cf='AVERAGE', xff=0.5, steps=1, rows=3600))
        roundRobinArchives.append(RRA(cf='AVERAGE', xff=0.5, steps=3600, rows=24))
        self.myRRD = RRD(filename, ds=self.dataSources, rra=roundRobinArchives, start=self.start_ut, step = 1)
        self.myRRD.create()

    def draw(self):
        from pyrrd.graph import DEF, CDEF, VDEF, LINE, AREA, GPRINT

        defs = []
        areas = []
        i = 0
        colors = ['#006600', '#000099']
        for d in self.dataSources:
            defs.append(DEF(rrdfile=self.myRRD.filename, vname=d.name, dsName=d.name))
            areas.append(AREA(defObj=defs[-1], color=colors[i], legend = d.name, stack = True))
            i += 1

        #cdef1 = CDEF(vname='kmh', rpn='%s' % def1.vname)
        #vdef1 = VDEF(vname='mymax', rpn='%s,MAXIMUM' % cdef1.vname)
        #vdef2 = VDEF(vname='myavg', rpn='%s,AVERAGE' % cdef1.vname)

        #area1 = AREA(defObj=cdef1, color='#006600', legend='Good Speed')
        #line2 = LINE(defObj=vdef2, color='#000099', legend='My Average', stack=True)
        #gprint1 = GPRINT(vdef2, '%6.2lf kph')

        from pyrrd.graph import ColorAttributes
        ca = ColorAttributes()
        ca.back = '#333333'
        ca.canvas = '#333333'
        ca.shadea = '#000000'
        ca.shadeb = '#111111'
        ca.mgrid = '#CCCCCC'
        ca.axis = '#FFFFFF'
        ca.frame = '#AAAAAA'
        ca.font = '#FFFFFF'
        ca.arrow = '#FFFFFF'

        from pyrrd.graph import Graph
        graphfile = "./rrdgraph.png"
        g = Graph(graphfile, start=self.start_ut, end=self.end_ut, vertical_label='seconds') #, color=ca
        #g.data.extend([def1, cdef1, vdef1, vdef2, area1, line2, gprint1])
        g.data.extend(defs + areas)
        g.write()
