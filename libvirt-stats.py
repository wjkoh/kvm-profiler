#We need libvirt and ElementTree.
import libvirt
from xml.etree import ElementTree
import time
import datetime

#Function to return a list of block devices used.
def get_target_devices(dom, dev):
    #Create a XML tree from the domain XML description.
    tree=ElementTree.fromstring(dom.XMLDesc(0))

    #The list of block device names.
    devices=[]

    #Iterate through all disk target elements of the domain.
    for target in tree.findall("devices/" + dev + "/target"):
        #Get the device name.
        dev=target.get("dev")

        #Check if we have already found the device name for this domain.
        if not dev in devices:
            devices.append(dev)

    #Completed device name list.
    return devices

def get_disk_stat(dom, stat):
    #Initialize our block stat counters.
    rreq=0
    rbytes=0
    wreq=0
    wbytes=0

    #Iterate through each device name used by this domain.
    for dev in get_target_devices(dom, 'disk'):
        #Retrieve the block stats for this device used by this domain.
        stats=dom.blockStats(dev)

        #Update the block stat counters
        rreq+=stats[0]
        rbytes+=stats[1]
        wreq+=stats[2]
        wbytes+=stats[3]

    stat['RREQ'] = rreq
    stat['RBYTES'] = rbytes
    stat['WREQ'] = wreq
    stat['WBYTES'] = wbytes

    #display the results for this domain.
    print "\n%s Block Stats"%(dom.UUIDString())
    print "Read Requests:  %s"%(rreq)
    print "Read Bytes:     %s"%(rbytes)
    print "Write Requests: %s"%(wreq)
    print "Written Bytes:  %s"%(wbytes)

def get_network_stat(dom, stat):
    #Initialize our interface stat counters.
    rx_bytes=0
    rx_packets=0
    rx_errs=0
    rx_drop=0
    tx_bytes=0
    tx_packets=0
    tx_errs=0
    tx_drop=0

    #Iterate through each device name used by this domain.
    for dev in get_target_devices(dom, 'interface'):
        #Retrieve the interface stats for this device used by this domain.
        stats=dom.interfaceStats(dev)

        #Update the interface stat counters
        rx_bytes+=stats[0]
        rx_packets+=stats[1]
        rx_errs+=stats[2]
        rx_drop+=stats[3]
        tx_bytes+=stats[4]
        tx_packets+=stats[5]
        tx_errs+=stats[6]
        tx_drop+=stats[7]

    stat['RX_BYTES'] = rx_bytes
    stat['RX_PACKETS'] = rx_packets
    stat['TX_BYTES'] = tx_bytes
    stat['TX_PACKETS'] = tx_packets

    #Display the results for this domain.
    print "\n%s Interface Stats"%(dom.UUIDString())
    print "Read Bytes:      %s"%(rx_bytes)
    print "Read Packets:    %s"%(rx_packets)
    print "Read Errors:     %s"%(rx_errs)
    print "Read Drops:      %s"%(rx_drop)
    print "Written Bytes:   %s"%(tx_bytes)
    print "Written Packets: %s"%(tx_packets)
    print "Write Errors:    %s"%(tx_errs)
    print "Write Drops:     %s"%(tx_drop)

def get_cpu_mem_stat(dom, stat):
    nodeName = dom.name()
    state, maxMem, memory, numVirtCpu, cpuTime = dom.info()

    stat['NAME'] = nodeName
    stat['CPU'] = cpuTime/1000000
    stat['MEM'] = memory

    #    uuid = dom.UUID()
    #    ostype = dom.OSType()
    #    print """Domain: %s, %s state (%s), %d CPUs, %d seconds, %d milliseconds, mem/max (%d/%d) """ \
    #          % (nodeName, ostype, state, numVirtCpu, cpuTime/float(1000000000), cpuTime/float(1000000), memory, maxMem )
    print "Nodename:  %s" % (nodeName)
    print "CPU time:  %d" % (cpuTime/float(1000000))
    print "Memory:    %d" % (memory)

from rrd_writer import rrd_writer

if __name__=="__main__":
    #Connect to some hypervisor.
    conn=libvirt.open("qemu:///system")

    # TODO: domains on/off
    init_dom_lst = [conn.lookupByID(id).name() for id in conn.listDomainsID()]
    rrd = rrd_writer(init_dom_lst)

    stats = {}
    for x in range(1*60):
        now_ut = int(time.mktime(datetime.datetime.now().timetuple()))

        #Iterate through all available domains.
        dom_lst = []
        stat_lst = []
        for id in conn.listDomainsID():
            #Initialize the domain object.
            dom = conn.lookupByID(id)
            dom_lst.append(dom.name())

            stat = {'TIME': now_ut}
            get_cpu_mem_stat(dom, stat)
            get_disk_stat(dom, stat)
            get_network_stat(dom, stat)

            print stat

            if id not in stats:
                stats[id] = []
            stats[id].append(stat)
            stat_lst.append(str(stat['CPU']))

        rrd.myRRD.bufferValue(now_ut, *stat_lst)
        rrd.myRRD.update(template = ':'.join(dom_lst))
        time.sleep(1)

    rrd.end_ut = int(time.mktime(datetime.datetime.now().timetuple()))
    rrd.draw()
    rrd.myRRD.info()

    print stats
