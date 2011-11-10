import time
import datetime

import draw
import libvirt_wrapper
import oprofile_wrapper
import measures.disk
import measures.disk_guest
import measures.network
import measures.cpu_mem

from django.core.management import setup_environ
from web import settings
setup_environ(settings)

from web.graph.models import Measurement


def putMeasurements(guest, now, stats, prefix):
    if stats == []:
        return

    for key in stats:
        if isinstance(stats[key], dict):
            putMeasurements(guest, now, stats[key], prefix + key + '/')
        else:
            measurement = Measurement(guest=guest, time=now, measure=prefix + key, value=stats[key])
            measurement.save()

    
if __name__ == "__main__":
    conn = libvirt_wrapper.Connection()
    guests = conn.get_guests()
    drawer = draw.Drawer()
    oprofile = oprofile_wrapper.OProfile()

    while True:
        oprofile.refresh()

        for guest in guests:
            guest_name = guest.get_name()
            now = datetime.datetime.now()

            stats = {}
            stats['DISK'] = measures.disk.get(guest)
            stats['DISK_GUEST'] = measures.disk_guest.get(guest)
            stats['NETWORK'] = measures.network.get(guest)
            stats['LLC'] = measures.llc.get(guest)

            putMeasurements(guest_name, now, stats, '')

        time.sleep(1)
