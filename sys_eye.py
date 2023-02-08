import psutil
from time import sleep
import os

import clr # the pythonnet module.

import wmi
w = wmi.WMI()
probe = w.Win32_TemperatureProbe()
for item in probe:
    print(item.CurrentReading)

# print(gpu.temperature)

# cwd = os.getcwd()
path = r"C:\Users\Patrick\Documents\UpWork\practice\OpenHardwareMonitorLib"
# path = r"C:\Users\Patrick\Downloads\openhardwaremonitor-v0.9.6.zip\OpenHardwareMonitor"
# path = r"C:\Users\Patrick\Downloads\openhardwaremonitor-v0.9.6\OpenHardwareMonitor\OpenHardwareMonitorLib.dll"
# # path = cwd + "\OpenHardwareMonitorLib"
clr.AddReference(path) 
# # e.g. clr.AddReference(r'OpenHardwareMonitor/OpenHardwareMonitorLib'), without .dll

from OpenHardwareMonitor.Hardware import Computer

c = Computer()
c.CPUEnabled = True # get the Info about CPU
c.FanControllerEnabled = True
# c.MainboardEnabled = True
c.Open()

cpu_temps = list()
gpu_temps = list()

for h in c.Hardware:
    print(h.Name)

print("")
for a in range(0, len(c.Hardware[0].Sensors)):
    s = c.Hardware[0].Sensors[a]
    print("{}: {}".format(s.Identifier, s.get_Value()))
    if "/temperature" in str(c.Hardware[0].Sensors[a].Identifier):
        print("{}: {}".format(c.Hardware[0].Sensors[a].Name, c.Hardware[0].Sensors[a].get_Value()))
        cpu_temps.append((c.Hardware[0].Sensors[a].Name, c.Hardware[0].Sensors[a].get_Value()))
        c.Hardware[0].Update()

c.CPUEnabled = False
c.MainboardEnabled = True
for sub in c.Hardware[0].SubHardware:
    sub.Update()
    if len(sub.Sensors) > 0:
        for sensor in sub.Sensors:
            print("{}".format(sensor.Name))


# for a in range(0, len(c.Hardware[1].Sensors)):
#     if "/temperature" in str(c.Hardware[1].Sensors[a].Identifier):
#         gpu_temps.append(c.Hardware[1].Sensors[a].get_Value())
#         c.Hardware[1].Update()



# gpu_temp = 0
# cpu_temp = 0

f = open("stats.txt", "w")

f.write("CPU%\t\t--\t{:f}%".format(psutil.cpu_percent(1)))
f.write("\n")
f.write("CPU Count\t--\t{}".format(psutil.cpu_count()))
f.write("\n")
f.write("CPU Frequency\t--\t{}".format(psutil.cpu_freq()[0]))
f.write("\n")
# f.write("Load average:\n\t1 min: {}\n\t5 min: {}\n\t15 min: {}".format(*psutil.getloadavg()))
# f.write("\n")
for i in range(len(cpu_temps)):
    f.write("{} temp\t--\t{}".format(*cpu_temps[i]))
    f.write("\n")
for i in range(len(gpu_temps)):
    f.write("GPU {} temp\t--\t{}".format(i, gpu_temps[i]))
    f.write("\n")
percent, secs, plugged = psutil.sensors_battery()
secs = secs / 60 if secs == psutil.POWER_TIME_UNKNOWN else "?"
f.write("Battery Information:\n\t{}% Left\n\t{} minutes left before empty\n\tCharger is{} plugged in.".format(percent, secs, "" if plugged else " not"))
f.write("\n")
f.write("Memory Used\t--\t{}".format(psutil.virtual_memory()[3]))
f.write("\n")
f.write("Memory Free\t--\t{}".format(psutil.virtual_memory()[4]))
f.write("\n")
f.close()