import guest
import os

class OProfile:
    def __init__(self):
        os.system("opcontrol --reset")
        os.system("opcontrol --shutdown")
        os.system("opcontrol --start")
        os.system("opcontrol -e=LLC_REFS:6000 -e=LLC_MISSES:6000")

    def __del__(self):
        os.system("opcontrol --shutdown")

    def refresh(self):
        os.system("opcontrol --dump")

if __name__ == "__main__":
    oprofile = OProfile()
#    guests = conn.get_guests()
#    for guest in guests:
#        print guest.get_name(), ":", guest.get_pid(), ":", guest.get_mac(), ":", guest.get_ip()
