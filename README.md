# Introduction

extensions to the IOS napalm driver to do some useful things

Requires `napalm` module.

See [getting started for details](#getting-started).

# Usage

```
import json
import napalm

driver = napalm.get_network_driver("ios")
device = driver('your_hostname', 'your_username', 'your_password', optional_args={'transport': 'ssh', 'secret': 'your_enable_secret'})
device.open()

cdp_neighbours = device.<function> (See: function list for details](#function_list).
print(json.dumps(cdp_neighbours,indent=4))
```

#function_list
## Function List
### getCDPNeighbours()
#### Description

Gets a list of CDP neighbours from the device, returns a dict with full interface names as keys

#### Usage

```
<device_driver_var>.getCDPNeighbours()
```
#### Sample Output

{
    "count": 2,
    "neighbours": {
        "GigabitEthernet1/0/2": [
            {
                "holdtime": "171",
                "capabilities": "S I  ",
                "remote_device_model": "WS-C2960-",
                "remote_device": "switch1",
                "remote_interface": "FastEthernet0/8"
            }
        ],
        "GigabitEthernet1/0/18": [
            {
                "holdtime": "148",
                "capabilities": "R S I ",
                "remote_device_model": "WS-C3750X",
                "remote_device": "switch2.name",
                "remote_interface": "GigabitEthernet3/0/24"
            }
        ]
    }
}
```

