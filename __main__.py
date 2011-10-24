import time
import datetime

import arp
import draw
import libvirt_wrapper
import measures.disk
import measures.network
import measures.cpu_mem

if __name__ == "__main__":
    conn = libvirt_wrapper.Connection()
    guests = conn.get_guests()
    drawer = draw.Drawer()

    for x in range(1*60):
        timestamp = int(time.mktime(datetime.datetime.now().timetuple()))

        for guest in guests:
            stats = {'NAME': guest.get_name(), 'TIME': timestamp}
            stats['CPU_MEM'] = measures.cpu_mem.get(guest)
            stats['DISK'] = measures.disk.get(guest)
            stats['NETWORK'] = measures.network.get(guest)

            print stats

        # TODO
        drawer.feed(guests)

        time.sleep(1)

    drawer.draw()
