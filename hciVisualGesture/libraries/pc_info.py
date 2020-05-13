#!/usr/bin/python3
"""
    This module contains the function to obtain the system information and store it in the file (pc_info.txt).
"""
import os
import psutil as ps
import platform
import win32api
from ssd import is_ssd

def getPC_Info():
    # Interpreter information:
    pythonVersion = "Python version: " + str(platform.python_version())
    pythonCompiler = "Python compiler: " + str(platform.python_compiler())

    # Platform information:
    systemTerse = "OS: " + str(platform.platform(terse = True))

    # Executable Architecture information
    arch = platform.architecture()
    architecture = "System architecture: " + str(arch[0])

    # Operating System and Hardware information
    version = "OS version: " + str(platform.version())
    machine= "Machine: " + str(platform.machine())
    processor= "Processor: " + str(platform.processor())
    numberCPUs = "CPUs number: " + str(ps.cpu_count(logical = False))

    cpufreq  = ps.cpu_freq()
    cpumaxfreq = "CPU Max Freq: " + str(cpufreq.max) + " MHz"
    cpuminfreq = "CPU Min Freq: " + str(cpufreq.min) + " MHz"
    cpucurrquency = "CPU Current Freq: " + str(cpufreq.current) + " MHz"

    svmem = ps.virtual_memory()
    totalMemory = "Total memory: " + str(get_size(svmem.total))
    availableMemory = "Available memory: " + str(get_size(svmem.available))
    usedMemory = "Used memory: " + str(get_size(svmem.used))
    percentMemory = "Percentaje memory: " + str((svmem.percent)) + ' %'

    # Display information
    displayDevice = win32api.EnumDisplayDevices()
    deviceName = 'Device: ' + displayDevice.DeviceString
    deviceSettings = win32api.EnumDisplaySettings(displayDevice.DeviceName, -1)
    deviceFreq = 'Refresh Rate (Hz): ' + str(deviceSettings.DisplayFrequency) + ' Hz'
    deviceColor = 'Color [bits per pixel]: ' + str(deviceSettings.BitsPerPel)
    deviceResolution = 'Display resolution: ' + str(deviceSettings.PelsWidth) + ' x ' + str(deviceSettings.PelsHeight)
    
    isSSD_Disk = is_ssd('./')
    if isSSD_Disk:
        diskType = 'Disk Type: SSD'
    else:
        diskType = 'Disk Type: HDD'

    data = ["Interpreter information:", "", pythonVersion, pythonCompiler, "", "Operating System and Hardware information:", "", 
            systemTerse, version, architecture, machine, processor, numberCPUs, cpumaxfreq, cpuminfreq, cpucurrquency, totalMemory, 
            availableMemory, usedMemory, percentMemory, "", "Display information:", "", deviceName, deviceFreq, deviceColor, 
            deviceResolution, "", "Disk information:", "", diskType]

    pc_info_file = open("./outputs/pc_info.txt", "w")
    for line in data:
        print(line, file = pc_info_file)
    pc_info_file.close()

def get_size(bytes, suffix="B"):
    """
        Scale bytes to its proper format
        example:
            1253656     => '1.20MB'
            1253656678  => '1.17GB'
    """
    factor = 1024
    for unit in ["", " K", " M", " G", " T", " P"]:
        if bytes < factor:
            return f"{bytes:.2f}{unit}{suffix}"
        bytes /= factor