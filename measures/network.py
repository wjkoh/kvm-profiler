def get(guest):
    rx_bytes = 0
    rx_packets = 0
    rx_errs = 0
    rx_drop = 0
    tx_bytes = 0
    tx_packets = 0
    tx_errs = 0
    tx_drop = 0

    for dev in guest.get_target_devices('interface'):
        stats = guest.get_domain().interfaceStats(dev)

        rx_bytes += stats[0]
        rx_packets += stats[1]
        rx_errs += stats[2]
        rx_drop += stats[3]
        tx_bytes += stats[4]
        tx_packets += stats[5]
        tx_errs += stats[6]
        tx_drop += stats[7]

    result = {}
    result['RX_BYTES'] = rx_bytes
    result['RX_PACKETS'] = rx_packets
    result['TX_BYTES'] = tx_bytes
    result['TX_PACKETS'] = tx_packets
    return result
