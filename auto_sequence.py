import sys
import time
from datetime import datetime
import psutil
from startup_meter import *

def progressMarker(flag):
    if flag[0] == True:
        sys.stdout.write("\b|")
        flag[0] = False
    else:
        sys.stdout.write("\b-")
        flag[0] = True
    sys.stdout.flush()


def ConditionLog():

    logsDir = "Condition logs"
    if not os.path.exists(logsDir):
        os.makedirs(logsDir)

    nowTimeStamp = datetime.now().strftime("%Y-%m-%d %H.%M.%S")

    try:
        logFile = open(logsDir + "/condition from " + nowTimeStamp + ".log", "w")
    except Exception as e:
        print("ERROR opening log file: {}".format(e))
    else:
        print("{} log file opened successfully".format(logFile.name))

    logFile.write("Automated test sequence from " + nowTimeStamp + ". Initial system conditions.\n")

    initialTime = time.time()
    print("Processing condition log -", end="")
    markerFlag = [True]
    cpuUsage = 0

    for i in range(10):
        cpuUsage += psutil.cpu_percent(interval=0.5) / 10
        progressMarker(markerFlag)

    logFile.write("CPU Usage average: {}%\n".format(cpuUsage))
    logFile.write("CPU Usage: {}\n".format(psutil.cpu_times()))
    logFile.write("MEM Usage: {}\n".format(psutil.virtual_memory()))

    for proc in psutil.process_iter():
        logFile.write("PID {:>5d} | {:>40} | Created {} | CPU {:5.1f}% | MEM {:5.1f}%\n".format(
            proc.pid,
            proc.name(),
            time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime(proc.create_time())),
            proc.cpu_percent(interval=0.5),
            proc.memory_percent()
            ))
        progressMarker(markerFlag)

    logFile.write("Logging successfully finished in: {}\n".format(time.strftime("%M minutes %S seconds", time.gmtime(time.time() - initialTime))))

    try:
        logFile.close()
    except Exception as e:
        print("\nERROR closing log file {}\n Log hasn't been recorded".format(logFile.name))
    else:
        print("\n{} has been recorded successfully".format(logFile.name))

ConditionLog()

progsList = {\
"AD17":["E:\\portable\\pro\\Altium\\AD17\\DXP.EXE", 0],\
"AD18":["E:\\portable\\pro\\Altium\\AD18\\X2.EXE", 0],\
"GIMP 2.9":["E:\\portable\\media\\GIMP 2.9\\bin\\gimp-2.9.exe", 0],\
"Firefox 56":["E:\\portable\\usr\\Mozilla Firefox\\firefox.exe", 0],\
"iTunes":["C:\\Program Files\\iTunes\\iTunes.exe", 0],\
}

for key in progsList.keys():
    progsList[key][1] = startupMeter(progsList[key][0])
    print("Waiting 10 seconds")
    time.sleep(10)

for key in progsList.keys():
    print("{} Startup time: {} seconds".format(key, progsList[key][1]))
