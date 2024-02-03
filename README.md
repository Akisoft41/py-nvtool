# py-nvtool
"Hiveos nvtool" en Python pour Linux et Windows



# Ubuntu Install
```
sudo apt install python3-pip
python3 -m pip install nvidia-ml-py
```

# Run
```
python3 py-nvtool.py [options]

  -i|--index NUM                Query specified GPU only (can be used multiple times)
  -a|--all                      Get GPU infos 
  --setpl NUM                   Set GPU power limit (W), 0 - default
  --setcore NUM                 Set GPU locked clocks (MHz), 0 - default
  --setmem NUM                  Set MEM locked clocks (MHz), 0 - default
  --setfan NUM                  Set fan speed (%), 0 - default
  --setcoreoffset NUM           Set CORE clocks offset (MHz), 0 - default
  --setmemoffset NUM            Set MEM clocks offset (MHz), 0 - default
```

# Docs

### NVIDIA Device Commands
https://docs.nvidia.com/deploy/nvml-api/group__nvmlDeviceCommands.html

### Python bindings to the NVIDIA Management Library
https://pypi.org/project/nvidia-ml-py/


______________

Ce projet est Open Source sous licence GPL-3.0-or-later

Copyright (C) 2024 Pascal Akermann
