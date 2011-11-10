import libvirt
import psutil

import guest

class Connection:
    def __init__(self):
        self.conn = libvirt.open("qemu:///system")

    def get_guests(self):
        kvm_processes = [process
                         for process
                         in psutil.get_process_list()
                         if process.name == "kvm"]
        pid_for_name = {}
        for process in kvm_processes:
            flag = False
            for arg in process.cmdline:
                if flag:
                    pid_for_name[arg] = process.pid
                    break
                if arg == "-name":
                    flag = True
        
        domains = [self.conn.lookupByID(id)
                   for id
                   in self.conn.listDomainsID()]
        result = []

        for domain in domains:
            result.append(guest.Guest(domain, pid_for_name[domain.name()]))

        return result

if __name__ == "__main__":
    conn = Connection()
    guests = conn.get_guests()
    for guest in guests:
        print guest.get_name(), ":", guest.get_pid(), ":", guest.get_mac(), ":", guest.get_ip()
