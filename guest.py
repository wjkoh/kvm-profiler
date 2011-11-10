from lxml import etree
import arp
import oprofile_wrapper

class Guest:
    def __init__(self, domain, pid):
        self.domain = domain
        self.pid = pid
        self.desc = None
        self.op_data = oprofile_wrapper.OP_Data()

    def get_domain(self):
        return self.domain

    def get_name(self):
        return self.domain.name()

    def get_pid(self):
        return self.pid

    def get_mac(self):
        return self.get_xml_desc().find("devices/interface[@type='network']/mac").attrib["address"].lower().strip()

    def get_ip(self):
        return arp.mac_to_ip(self.get_mac())

    def get_target_devices(self, device_name):
        result = []
        for target in self.get_xml_desc().findall("devices/" + device_name + "/target"):
            device = target.get("dev")
            if not device in result:
                result.append(device)

        return result

    def get_xml_desc(self):
        if self.desc is None:
            self.refresh_xml_desc()
        return self.desc

    def refresh_xml_desc(self):
        self.desc = etree.fromstring(self.domain.XMLDesc(0))
