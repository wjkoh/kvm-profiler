import subprocess

def mac_to_ip(mac):
    output = subprocess.Popen(["arp", "-n"], stdout=subprocess.PIPE).communicate()[0]
    lines = [line.split() for line in output.split("\n")[1:]]
    ip = [line[0] for line in lines if (line and (line[2] == mac))]
    if len(ip) == 0:
        raise Exception("IP address not found for MAC address %s" % mac)
    return ip[0]

if __name__ == "__main__":
    print mac_to_ip("52:54:00:88:ee:f9")
    print mac_to_ip("52:54:00:88:ee:f0")
