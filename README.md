# py-nvtool
"Hiveos nvtool" en Python pour Linux et Windows

A cause de la librairie nvml de Nvidia, ```--setmem``` ne fonctionne que pour les GPU s�rie 30xx et suivantes

## Install
```
wget https://github.com/Akisoft41/py-nvtool/releases/download/v0.2.0/py-nvtool.py
```

#### Linux

```
chmod +x py-nvtool.py
cp py-nvtool.py /usr/sbin/

sudo py-nvtool.py [options]
```


## Run
```
py-nvtool.py [options]

  -i|--index NUM                Query specified GPU only
  -a|--all                      Get GPU infos 
  --setpl NUM                   Set GPU power limit (W), 0 - default
  --setcore NUM                 Set GPU locked clocks (MHz), 0 - default
  --setmem NUM                  Set MEM locked clocks (MHz), 0 - default
  --setfan NUM                  Set fan speed (%), 0 - default
  --setcoreoffset NUM           Set CORE clocks offset (MHz), 0 - default
  --setmemoffset NUM            Set MEM clocks offset (MHz), 0 - default
```

### Exemple

```
py-nvtool.py --setclocks 1400 --setcoreoffset 200 --setmem 6800 --setmemoffset 2000 --setpl 120 --setfan 50
```

## Docs

### NVIDIA Device Commands
https://docs.nvidia.com/deploy/nvml-api/group__nvmlDeviceCommands.html

### Python bindings to the NVIDIA Management Library
https://pypi.org/project/nvidia-ml-py/


______________

Ce projet est Open Source sous licence GPL-3.0-or-later
