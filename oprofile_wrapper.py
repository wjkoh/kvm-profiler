import guest
import os
import arp
import subprocess
from lxml import etree

cycles = 100000

class OProfile:
    def __init__(self):
        os.system("opcontrol -e=LLC_REFS:%d -e=LLC_MISSES:%d -e=CPU_CLK_UNHALTED:%d -e=INST_RETIRED:%d" % ( cycles, cycles, cycles, cycles ) )
        os.system("opcontrol --reset")
        os.system("opcontrol --shutdown")
        os.system("opcontrol --start")

    def __del__(self):
        os.system("opcontrol --shutdown")

    def refresh(self):
        os.system("opcontrol --dump")

class OP_Data:
    def __init__(self):
        self.refs = 0
        self.misses = 0
        self.inst_retired = 0
        self.cpu_clk_unhalted = 0

def get_measure(guest, mes_name, old_data):
    args = ["opreport", "-l", "event:"+mes_name, "tid:"+str(guest.get_pid()), "--merge=cpu", "-X"]

    p = subprocess.Popen( args, stdout = subprocess.PIPE, stderr = open( "/dev/null" ) )
    p.wait()
    data = ""

    for line in p.stdout:
        data = data + line + "\n"
    
    try:
        desc = etree.fromstring( data )
        return int( desc.find("process/count").text )
    except etree.XMLSyntaxError, e:
        return old_data

if __name__ == "__main__":
    oprofile = OProfile()
