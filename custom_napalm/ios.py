from napalm.ios.ios import IOSDriver
import re

class CustomIOSDriver(IOSDriver):
    """ Extended Naplams get_network_driver to provide additional functionality for legacy IOS devices """
    name_mapping = { 
        'Gig': 'GigabitEthernet',
        'Ten': 'TenGigabitEthernet',
        'Fas': 'FastEthernet'
        }
    cdp_neighbours = { 'count': 0, 'neighbours': {} }
    parent = None

        
    def getCDPNeighbours(self):
        """Returns a list of CDP Neighbours by parsing the cli command: show cdp neighbours"""
        output = self._send_command('show cdp neigh')

        re_cmd_cdp_1 = re.compile("(([a-zA-Z0-9\-\_\.]+)[\s\t\r\n]+(Fas|Gig|Ten|Po)[\s\t]+([0-9\/]+)[\s\t]+([0-9]+)[\s\t]+([RSI\s]+)[\s\t]+([^ ]+)[\s\t]+(Gig|Fas|Ten|vmnic)[\s\t]+([0-9\/]+)[\n]+)")
        t = re.findall(re_cmd_cdp_1,output)
        #print(json.dumps(t,indent=4))
        if t != None:
            # loop through each entry - matches as:
            # 0 = full match, 1 = remote host, 2 = remote int, 3 = remote intnum, 4 = holdtime, 5 = capabilities, 6 = remote device ver (substring, do not use as real identifier)
            # 7 = remote int name, 8 = remote int subname
            for i in t:
                if i[2] in self.name_mapping.keys():
                    local_intname = self.name_mapping[i[2]]
                else:
                    local_intname = i[2]
                if i[7] in self.name_mapping.keys():
                    remote_intname = self.name_mapping[i[7]]
                else:
                    remote_intname = i[7]
                
                local_fullintname = local_intname + i[3]
                remote_fullintname = remote_intname + i[8]
                
                # inc count, create a dict entry of type list if it doesn't already exit
                self.cdp_neighbours['count'] = self.cdp_neighbours['count'] + 1
                if local_fullintname not in self.cdp_neighbours['neighbours'].keys():
                    self.cdp_neighbours['neighbours'][local_fullintname] = []
                
                local_entry = {}
                local_entry['holdtime'] = i[4]
                local_entry['capabilities'] = i[5]
                local_entry['remote_device_model'] = i[6]
                local_entry['remote_device'] = i[1]
                local_entry['remote_interface'] = remote_fullintname
                self.cdp_neighbours['neighbours'][local_fullintname].append(local_entry.copy())
                
        return(self.cdp_neighbours)
