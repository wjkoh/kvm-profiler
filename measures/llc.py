import subprocess
from lxml import etree

class LLC_Data:
    def __init__(self):
        self.refs = 0
        self.misses = 0

def get(guest):
    refs_old = guest.llc_data.refs
    args = ["opreport", "-l", "event:LLC_REFS", "tid:"+str(guest.get_pid()), "--merge=cpu", "-X"]
    p = subprocess.Popen( args, stdout = subprocess.PIPE, stderr = open('/dev/null') )
    p.wait()
    data = ""

    for line in p.stdout:
        data = data + line + "\n"
    
    try:
        desc = etree.fromstring( data )
        guest.llc_data.refs = int( desc.find("process/count").text )
    except etree.XMLSyntaxError, e:
        pass

    misses_old = guest.llc_data.misses
    args = ["opreport", "-l", "event:LLC_MISSES", "tid:"+str(guest.get_pid()), "--merge=cpu", "-X"]
    p = subprocess.Popen( args, stdout = subprocess.PIPE, stderr = open('/dev/null') )
    p.wait()
    data = ""

    for line in p.stdout:
        data = data + line + "\n"
    
    try:
        desc = etree.fromstring( data )
        guest.llc_data.misses = int( desc.find("process/count").text )
#        print guest.llc_data.misses.text
#        print [ child for child in guest.llc_data.misses.attrib ]
    except etree.XMLSyntaxError, e:
        pass

    res = {}
    res[ "LLC_REFS" ] = guest.llc_data.refs - refs_old
    res[ "LLC_MISSES" ] = guest.llc_data.misses - misses_old

    return res

    