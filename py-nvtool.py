# py-nvtool is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or any later version.
# py-nvtool is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.
# You should have received a copy of the GNU General Public License along with py-nvtool. If not, see <https://www.gnu.org/licenses/>

import sys
from pynvml import *


def PrintInfo(handle):
  try:
    #print(f"  BUS ID: {}")
    print(f"  NAME: {nvmlDeviceGetName(handle)}")
    print(f"  VBIOS: {nvmlDeviceGetVbiosVersion(handle)}")
    memory = nvmlDeviceGetMemoryInfo(handle)
    print(f"  MEM TOTAL: {int(memory.total/1024/1024)} MB, USED: {int(memory.used/1024/1024)} MB, FREE: {int(memory.free/1024/1024)} MB")
    print(f"  GPU CLOCKS CURRENT: {nvmlDeviceGetClockInfo(handle, NVML_CLOCK_GRAPHICS)} MHz")
    print(f"  MEM CLOCKS CURRENT: {nvmlDeviceGetClockInfo(handle, NVML_CLOCK_MEM)} MHz")
    print(f"  GPU CLOCKS OFFSET: {nvmlDeviceGetGpcClkVfOffset(handle)} MHz")
    print(f"  MEM CLOCKS OFFSET: {nvmlDeviceGetMemClkVfOffset(handle)} MHz")
    print(f"  POWER USAGE: {int(nvmlDeviceGetPowerUsage(handle)/1000)} W")
    print(f"  POWER LIMIT CURRENT: {int(nvmlDeviceGetPowerManagementLimit(handle)/1000)} W")
    (minLimit, maxLimit) = nvmlDeviceGetPowerManagementLimitConstraints(handle)
    print(f"  POWER LIMIT MIN: {int(minLimit/1000)} W, DEFAULT: {int(nvmlDeviceGetPowerManagementDefaultLimit(handle)/1000)}, MAX: {int(maxLimit/1000)} W")
    print(f"  TEMPERATURE: {nvmlDeviceGetTemperature(handle, NVML_TEMPERATURE_GPU)} C")
    numFans = nvmlDeviceGetNumFans(handle)
    for i in range(numFans):
      print(f"  FAN #{i} SPEED: {nvmlDeviceGetFanSpeed_v2(handle, i)} %, TARGET: {nvmlDeviceGetTargetFanSpeed(handle, i)} %")
    
    print(f"  ARCH: ", end='')
    arch = nvmlDeviceGetArchitecture(handle)
    if arch == NVML_DEVICE_ARCH_KEPLER:
      print(f"KEPLER")
    elif arch == NVML_DEVICE_ARCH_MAXWELL:
      print(f"MAXWELL")
    elif arch == NVML_DEVICE_ARCH_PASCAL: # 10xx
      print(f"PASCAL")
    elif arch == NVML_DEVICE_ARCH_VOLTA:  # Titan V, Quadro GV100
      print(f"VOLTA")
    elif arch == NVML_DEVICE_ARCH_TURING: # 16xx, 20xx
      print(f"TURING")
    elif arch == NVML_DEVICE_ARCH_AMPERE: # 30xx
      print(f"AMPERE")
    elif arch == NVML_DEVICE_ARCH_ADA:    # 40xx
      print(f"ADA")
    elif arch == NVML_DEVICE_ARCH_HOPPER:
      print(f"HOPPER")
    else:
      print(f"UNKNOWN")
    
    print(f"  STATUS: Success")
  except NVMLError as error:
    print(f"  STATUS: Error {error}")


def all(idx):
  if idx >= 0:
    handle = nvmlDeviceGetHandleByIndex(idx)
    print(f"DEVICE #{idx}:")
    PrintInfo(handle)
  else:
    deviceCount = nvmlDeviceGetCount()
    for i in range(deviceCount):
      handle = nvmlDeviceGetHandleByIndex(i)
      print(f"DEVICE #{i}:")
      PrintInfo(handle)



def set(idx, setpl, setcore, setmem, setfan, setcoreoffset, setmemoffset):
  if idx >= 0:
    set1(idx, setpl, setcore, setmem, setfan, setcoreoffset, setmemoffset)
  else:
    deviceCount = nvmlDeviceGetCount()
    for idx in range(deviceCount):
      set1(idx, setpl, setcore, setmem, setfan, setcoreoffset, setmemoffset)



def set1(idx, setpl, setcore, setmem, setfan, setcoreoffset, setmemoffset):
  try:
    print(f"DEVICE #{idx}:")
    handle = nvmlDeviceGetHandleByIndex(idx)
    
    try:
      if setpl == 0:
        print(f"  SET POWER LIMIT: DEFAULT ", end='')
        pl = int(nvmlDeviceGetPowerManagementDefaultLimit(handle)/1000)
        print(f"({pl} W) ", end='')
        nvmlDeviceSetPowerManagementLimit(handle, pl*1000)
        print()
      if setpl > 0:
        print(f"  SET POWER LIMIT: {setpl} W ", end='')
        pl = int(nvmlDeviceGetPowerManagementLimit(handle)/1000)
        if pl != setpl:
          (minLimit, maxLimit) = nvmlDeviceGetPowerManagementLimitConstraints(handle)
          if setpl*1000 >= minLimit and setpl*1000 <= maxLimit:
            nvmlDeviceSetPowerManagementLimit(handle, setpl*1000)
          else:
            print(f"is not in range of {int(minLimit/1000)} to {int(maxLimit/1000)}", end='')
        else:
          print(f"was already set", end='')
        print()
    except NVMLError as error:
      print(f" [{error}]")
      
    try:
      if setfan == 0:
        print(f"  SET FAN SPEED: DEFAULT ", end='')
        for i in range(nvmlDeviceGetNumFans(handle)):
          nvmlDeviceSetDefaultFanSpeed_v2(handle, i)
        print(f" ({nvmlDeviceGetTargetFanSpeed(handle, 0)} %)")
      elif setfan > 0 and setfan <= 100:
        print(f"  SET FAN SPEED: {setfan} % ", end='')
        for i in range(nvmlDeviceGetNumFans(handle)):
          nvmlDeviceSetFanSpeed_v2(handle, i, setfan)
        print()
    except NVMLError as error:
      print(f" [{error}]")
      
    try:
      if setcore == 0:
        print(f"  SET GPU CLOCKS LOCKED: DEFAULT ", end='')
        nvmlDeviceResetGpuLockedClocks(handle)
        newcore = nvmlDeviceGetClockInfo(handle, NVML_CLOCK_GRAPHICS)
        print(f"({newcore} Mhz) ")
      if setcore > 0:
        print(f"  SET GPU CLOCKS LOCKED: {setcore} MHz ", end='')
        oldcore = nvmlDeviceGetClockInfo(handle, NVML_CLOCK_GRAPHICS)
        nvmlDeviceSetGpuLockedClocks(handle, setcore, setcore)
        newcore = nvmlDeviceGetClockInfo(handle, NVML_CLOCK_GRAPHICS)
        if setcore != newcore:
          print(f"({newcore} Mhz) ", end='')
        if oldcore == newcore:
          print(f"was already set", end='')
        print()
    except NVMLError as error:
      print(f" [{error}]")
      
    try:
      if setmem == 0:
        print(f"  SET MEM CLOCKS LOCKED: DEFAULT ", end='')
        nvmlDeviceResetMemoryLockedClocks(handle)
        newmem = nvmlDeviceGetClockInfo(handle, NVML_CLOCK_MEM)
        print(f"({newmem} Mhz) ")
      if setmem > 0:
        print(f"  SET MEM CLOCKS LOCKED: {setmem} MHz ", end='')
        oldmem = nvmlDeviceGetClockInfo(handle, NVML_CLOCK_MEM)
        nvmlDeviceSetMemoryLockedClocks(handle, setmem, setmem)
        newmem = nvmlDeviceGetClockInfo(handle, NVML_CLOCK_MEM)
        if setmem != newmem:
          print(f"({newmem} Mhz) ", end='')
        if oldmem == newmem:
          print(f"was already set", end='')
        print()
    except NVMLError as error:
      print(f" [{error}]")
      
    try:
      if setcoreoffset != -65535:
        print(f"  SET GPU CLOCKS OFFSET: {setcoreoffset} MHz ", end='')
        oldcoreoffset = nvmlDeviceGetGpcClkVfOffset(handle)
        nvmlDeviceSetGpcClkVfOffset(handle, setcoreoffset)
        newcoreoffset = nvmlDeviceGetGpcClkVfOffset(handle)
        if setcoreoffset != newcoreoffset:
          print(f"({newcoreoffset} Mhz) ", end='')
        if oldcoreoffset == newcoreoffset:
          print(f"was already set", end='')
        print()
    except NVMLError as error:
      print(f" [{error}]")
      
    try:
      if setmemoffset != -65535:
        print(f"  SET MEM CLOCKS OFFSET: {setmemoffset} MHz ", end='')
        oldmemoffset = nvmlDeviceGetMemClkVfOffset(handle)
        nvmlDeviceSetMemClkVfOffset(handle, setmemoffset)
        newmemoffset = nvmlDeviceGetMemClkVfOffset(handle)
        if setmemoffset != newmemoffset:
          print(f"({newmemoffset} Mhz) ", end='')
        if oldmemoffset == newmemoffset:
          print(f"was already set", end='')
        print()
    except NVMLError as error:
      print(f" [{error}]")
      
      
    
  except NVMLError as error:
    print(f" Error {error}")


try:
  nvmlInit()
except NVMLError as error:
  print(f"Error {error}")
  sys.exit(1)

try:
  if len(sys.argv) == 1:
    print(f"Driver Version: {nvmlSystemGetDriverVersion()}")
    all(-1)
    sys.exit(0)
  
  
  idx = -1
  setpl = -1
  setcore = -1
  setmem = -1
  setfan = -1
  setcoreoffset = -65535
  setmemoffset = -65535
  
  i = 1
  while i < len(sys.argv):
  
    if sys.argv[i] == "-i" or sys.argv[i] == "--index":
      i += 1
      idx = int(sys.argv[i])
      
    elif sys.argv[i] == "-a" or sys.argv[i] == "--all":
      all(idx)
    
    elif sys.argv[i] == "--setpl":
      i += 1
      setpl = int(sys.argv[i])
    elif sys.argv[i] == "--setcore":
      i += 1
      setcore = int(sys.argv[i])
    elif sys.argv[i] == "--setmem":
      i += 1
      setmem = int(sys.argv[i])
    elif sys.argv[i] == "--setfan":
      i += 1
      setfan = int(sys.argv[i])
    elif sys.argv[i] == "--setcoreoffset":
      i += 1
      setcoreoffset = int(sys.argv[i])
    elif sys.argv[i] == "--setmemoffset":
      i += 1
      setmemoffset = int(sys.argv[i])
    
    i += 1
  
  set(idx, setpl, setcore, setmem, setfan, setcoreoffset, setmemoffset)
  
  
except NVMLError as error:
  print(f"Error {error}")

finally:
  nvmlShutdown()
