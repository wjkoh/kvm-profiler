def get(guest):
    domain_name = guest.get_domain().name()
    state, maxMem, memory, numVirtCpu, cpuTime = guest.get_domain().info()

    result = {}
    result['CPU'] = cpuTime/1000000
    result['MEM'] = memory
    return result
