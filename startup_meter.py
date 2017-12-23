import psutil
import time
import os
import sys
import subprocess


def startupMeter(progPath):
    # Config
    # progPath = "E:\\portable\\pro\\Altium\\AD17\\DXP.EXE"
    thresold = 10
    samplePeriod = 0.5
    frameSize = 10

    # Init
    frame = [thresold for x in range(frameSize)]
    write = sys.stdout.write
    write("Starting up ")
    markerFlag = True

    # Start timer
    initial_time = time.time()

    # Create process
    proc = subprocess.Popen(progPath)
    time.sleep(1)
    meter = psutil.Process(proc.pid)
    write(meter.name() + " -")

    while True:

        if markerFlag == True:
            write("\b|")
            markerFlag = False
        else:
            write("\b-")
            markerFlag = True
        sys.stdout.flush()

        try:
            frame.append(meter.cpu_percent(interval=samplePeriod))
        except Exception:
            print("\nAny processes killed")
            sys.exit()

        avg = 0
        for i in range(1, frameSize + 1):
            avg += frame[-i] / frameSize

        if avg < thresold:
            finish_time = time.time()
            overall = finish_time - initial_time - ((frameSize / 2) * samplePeriod)
            print("\nOverall startup time ", overall)
            proc.kill()
            # break
            return overall

# Usage
# xxx = startupMeter("E:\\portable\\pro\\Altium\\AD17\\DXP.EXE")
# print(xxx)