import psutil
from datetime import datetime
import matplotlib.pyplot as plt
import time
import os
import sys

def ProcSearch(procName):
    write = sys.stdout.write
    write("Waiting " + procName + " -")
    markerFlag = True
    while True:
        if markerFlag == True:
            write("\b|")
            markerFlag = False
        else:
            write("\b-")
            markerFlag = True
        sys.stdout.flush()
        try:
            for proc in psutil.process_iter():
                if proc.name() == procName:
                    print("\nStart: ", proc)
                    return proc
        except Exception: 
            pass

        time.sleep(0.2)

# Config

# processName = "DXP.EXE"
processName = "X2.EXE"
# processName = "firefox.exe"
# processName = "iTunes.exe"
# processName = "gimp-2.9.exe"

width = 30 # Samples to dislpay
xcount = width # Seconds counter
thresold = 10
frameSize = 10

# Search process
dxp_pid = ProcSearch(processName)
initial_time = time.time()

### Initialize plots ###

# Initialize data capture buffer
xdata = [x for x in range(width)]
ydata = [thresold for x in range(width)]

# Create plots window
plt.ion()
axes = plt.gca()
line, = plt.plot(xdata, ydata)

axes.set_title(processName)
axes.autoscale(axis='x')
axes.set_xlabel("Seconds")
axes.grid()
axes.set_ylim(0, 110)
axes.set_ylabel("CPU %")
axes.legend()

# Open plot window
plt.show()

### Create log file ###
logsDir = "logs"
if not os.path.exists(logsDir):
    os.makedirs(logsDir)

nowTimeStamp = datetime.now().strftime("%Y-%m-%d %H.%M.%S")

try:
    logFile = open(logsDir + "/log " + processName + " " + nowTimeStamp + ".csv", "w")
except Exception as e:
    print("ERROR opening log file: {}".format(e))
else:
    print("{} log file opened successfully".format(logFile.name))

title = "timeStamp," + processName
logFile.write(title + "\n")


### Infinite loop of data processing and displaying ###

while plt.fignum_exists(1):

    try:
        ydata.append(dxp_pid.cpu_percent(interval=0.5))
    except Exception:
        print("Any processes killed")
        break
    
    avg = 0
    for i in range(1, frameSize + 1):
        avg += ydata[-i] / frameSize

    if avg < thresold:
        finish_time = time.time()
        print("Startup finished on ", xdata[-(frameSize // 2)])
        print("Overall startup time ", finish_time - initial_time - ((frameSize / 2) * 0.5))
        x = input("Press ENTER to exit")
        break

    for i in ydata:
        while len(ydata) > width:
            del ydata[0]

    xcount += 0.5
    del xdata[0]
    xdata.append(xcount)

    line.set_xdata(xdata)
    line.set_ydata(ydata)

    axes.relim()
    axes.autoscale_view(True,True,True)

    plt.draw()
    plt.pause(0.01)

    # Write log record
    dataStr = datetime.now().strftime("%Y-%m-%dT%H:%M:%S.%f")
    dataStr += ","
    dataStr += str(ydata[width - 1])
    
    logFile.write(dataStr + "\n")
    print("Recorded log: " + dataStr)

try:
    logFile.close()
except Exception as e:
    print("ERROR closing log file {}\n Log hasn't been recorded".format(logFile.name))
else:
    print("{} has been recorded successfully".format(logFile.name))