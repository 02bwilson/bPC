import platform
import subprocess
import threading
from collections import OrderedDict

from cpuinfo import get_cpu_info


class bPC_DF:

    def __init__(self):
        self.c = None
        self.data = None


        self.data = OrderedDict()

    def get_data(self, hw):
        threading.Timer(1.0, lambda: self.get_data(hw))
        if hw == "CPU":
            self.data = OrderedDict(get_cpu_info())
            return
        elif hw == "GPU":
            self.data = OrderedDict(get_cpu_info())
            return

        else:
            raise Exception("Invalid entry")



    def get_cpu_freq(self):
        if platform.system() == "Windows":
            max_clock_speed = int(
                subprocess.check_output(["powershell", "(Get-CimInstance CIM_Processor).MaxClockSpeed"]).strip())
            processor_performance = float(subprocess.check_output(["powershell",
                                                                   "(Get-Counter -Counter '\\Processor Information(_Total)\\% Processor Performance').CounterSamples.CookedValue"]).strip())
            current_clock_speed = max_clock_speed * (processor_performance / 100000)
            print("Current Processor Speed: ", current_clock_speed)
            self.data['current_freq'] = current_clock_speed

        elif platform.system() == "Linux":
            with open("/proc/cpuinfo", "r") as f:
                for line in f:
                    if "cpu MHz" in line:
                        frequency = float(line.split(":")[1])
                        self.data['current_freq'] = frequency
        else:
            return None

