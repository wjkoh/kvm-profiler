def get(guest):
    rreq = 0
    rbytes = 0
    wreq = 0
    wbytes = 0

    for dev in guest.get_target_devices('disk'):
        stats = guest.get_domain().blockStats(dev)
        rreq += stats[0]
        rbytes += stats[1]
        wreq += stats[2]
        wbytes += stats[3]

    result = {}
    result['RREQ'] = rreq
    result['RBYTES'] = rbytes
    result['WREQ'] = wreq
    result['WBYTES'] = wbytes
    return result;
