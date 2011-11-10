import time
import datetime

import arp
import draw
import libvirt_wrapper
import oprofile_wrapper
import measures.disk
import measures.disk_guest
import measures.network
import measures.cpu_mem

if __name__ == "__main__":
    conn = libvirt_wrapper.Connection()
    guests = conn.get_guests()
    drawer = draw.Drawer()
    oprofile = oprofile_wrapper.OProfile()

    for x in range(1*60):
        timestamp = int(time.mktime(datetime.datetime.now().timetuple()))
        oprofile.refresh()

        for guest in guests:
            stats = {'NAME': guest.get_name(), 'TIME': timestamp}
            stats['CPU_MEM'] = measures.cpu_mem.get(guest)
            stats['DISK'] = measures.disk.get(guest)
            stats['DISK_GUEST'] = measures.disk_guest.get(guest)
            stats['NETWORK'] = measures.network.get(guest)
            stats['LLC'] = measures.llc.get(guest)

            print stats

        # TODO
        drawer.feed(guests)

        time.sleep(1)

    drawer.draw()
