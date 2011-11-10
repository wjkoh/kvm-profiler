import xmlrpclib
import socket
import errno

def get(guest):
    result = {}
    stats = None

    try:
        proxy = xmlrpclib.ServerProxy('http://%s:8000/' % guest.get_ip())
        stats = proxy.disk_io_counters()
    except socket.error as e:
        if e.errno == errno.ECONNREFUSED:
            print 'warning: guest tools need to be installed on %s' % guest.get_name()
            return result
        else:
            raise

    for k, v in stats.iteritems():
        stats[k] = int(v)

    result['RREQ'] = stats['read_count']
    result['RBYTES'] = stats['read_bytes']
    result['WREQ'] = stats['write_count']
    result['WBYTES'] = stats['write_bytes']
    return result
