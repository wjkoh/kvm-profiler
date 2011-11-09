LISTEN_PORT = 8000

try:
    import psutil
except ImportError, e:
    raise SystemExit("error: can't import psutil module.")

psutil_version =  tuple([int(x) for x in psutil.__version__.split('.')])
if psutil_version < (0, 4, 0):
    raise SystemExit('error: psutil >= 0.4.0 is required.')

def iostat_to_dict(o_dic):
    dic = dict(o_dic._asdict())
    for k, v in dic.iteritems():
        dic[k] = str(v)
    return dic

def disk_io_counters(perdisk = False):
    stats = psutil.disk_io_counters(perdisk)
    if type(stats) == type(dict()): 
        for k, v in stats.iteritems():
            stats[k] = iostat_to_dict(v)
    else:
        stats = iostat_to_dict(stats)
    print stats
    return stats

import xmlrpclib
from SimpleXMLRPCServer import SimpleXMLRPCServer

if __name__ == '__main__':
    server = SimpleXMLRPCServer(('', LISTEN_PORT))
    print 'Listening on port %d...' % LISTEN_PORT
    server.register_function(disk_io_counters, 'disk_io_counters')
    server.serve_forever()
