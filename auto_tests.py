import psutil
import time
import os
import sys
import subprocess
from datetime import datetime
import ffmpeg
import wmi


def progressMarker(flag):
    if flag[0] == True:
        sys.stdout.write("\b|")
        flag[0] = False
    else:
        sys.stdout.write("\b-")
        flag[0] = True
    sys.stdout.flush()


def waitingIdle(idleSec):
    print("Waiting", idleSec, "seconds idle -", end="")
    markerFlag = [True]
    for i in range(idleSec * 2):
        progressMarker(markerFlag)
        time.sleep(0.5)
    print()


def sensorsCapture():
    # OpenHardwareMonitor must been started
    capture = dict()
    w = wmi.WMI(namespace="root\OpenHardwareMonitor")
    for sensor in w.Sensor():
        if sensor.SensorType in capture:
            capture[sensor.SensorType][sensor.Name] = round(sensor.Value, 2)
        else:
            capture[sensor.SensorType] = {sensor.Name:round(sensor.Value, 2)}
    return capture


def hardwareCapture():
    # OpenHardwareMonitor must been started

    units = {"Voltage":"V", "Temperature":"°C", "Fan":"RPM", "Clock":"MHz", "Load":"%", "Power":"W", "Data":"GB", "Level":"%"}    
    w = wmi.WMI(namespace="root\OpenHardwareMonitor")

    hard = dict()
    for i in w.Hardware():
        hard[i.Identifier] = i.Name

    capture = dict()
    for sensor in w.Sensor():
        if sensor.SensorType not in units:
            units[sensor.SensorType] = "?"
        hardName = hard[sensor.Parent]
        if hardName in capture:
            if sensor.SensorType in capture[hardName]:
                capture[hardName][sensor.SensorType][sensor.Name] = (round(sensor.Value, 2), units[sensor.SensorType])
            else:
                capture[hardName][sensor.SensorType] = {sensor.Name:(round(sensor.Value, 2), units[sensor.SensorType])}
        else:
            capture[hardName] = {sensor.SensorType:{sensor.Name:(round(sensor.Value, 2), units[sensor.SensorType])}}

    return capture


def conditionLog():
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

    # Write Open Hardware Monitor capture
    logFile.write("\nOpen Hardware Monitor capture\n")
    cap = hardwareCapture()
    for n in cap.keys():
        logFile.write("{}\n".format(n))
        for i in cap[n].keys():
            logFile.write("                   {}\n".format(i))
            for k in sorted(cap[n][i]):
                logFile.write("                                 {:<18} = {} {}\n".format(k, cap[n][i][k][0], cap[n][i][k][1]))

    # Write psutil metrics
    logFile.write("\npsutil metrics\n")

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

    # Finish logging
    logFile.write("\nLogging successfully finished in: {}\n".format(time.strftime("%M minutes %S seconds", time.gmtime(time.time() - initialTime))))

    try:
        logFile.close()
    except Exception as e:
        print("\nERROR closing log file {}\n Log hasn't been recorded".format(logFile.name))
    else:
        print("\n{} has been recorded successfully".format(logFile.name))


def startupMeter(progPath, threshold = 10, samplePeriod = 0.5, frameSize = 10):
    # Init
    frame = [threshold for x in range(frameSize)]
    print("Starting up ", end="")
    markerFlag = [True]

    # Start timer
    initial_time = time.time()

    # Create process
    proc = subprocess.Popen(progPath)
    time.sleep(1)
    meter = psutil.Process(proc.pid)
    print(meter.name(), " -", end="")    

    while True:
        progressMarker(markerFlag)

        try:
            frame.append(meter.cpu_percent(interval=samplePeriod))
        except Exception:
            print("\nAny processes killed")
            sys.exit()

        avg = 0
        for i in range(1, frameSize + 1):
            avg += frame[-i] / frameSize

        if avg < threshold:
            finish_time = time.time()
            overall = finish_time - initial_time - ((frameSize / 2) * samplePeriod)
            print("\nOverall startup time", overall)
            proc.kill()
            return overall


def videoConvert(inputFile, outputFile):
    stream = ffmpeg.input(inputFile, loglevel="error", stats="")
    stream = ffmpeg.output(stream, outputFile)
    stream = ffmpeg.overwrite_output(stream)

    print("Converting {}:".format(inputFile))
    initial_time = time.time()
    ffmpeg.run(stream)
    overall = time.time() - initial_time
    print("Overall convert time", overall)
    return overall



### Usage

# conditionLog()

# xxx = startupMeter("E:\\portable\\pro\\Altium\\AD17\\DXP.EXE")
# print(xxx)

# xxx = videoConvert("test_video.mp4", "test_video.avi")
# print(xxx)

# cap = sensorsCapture()
# for i in cap.keys():
#     print(i)
#     for k in sorted(cap[i]):
#         print("{:>18} = {}".format(k, cap[i][k]))

# cap = hardwareCapture()
# for n in cap.keys():
#     print(n)
#     # print('{str:{filler1}<{len1}}\n{down:{filler2}>{len2}}'.format(str=n, len1=22, len2=23, filler1='-', filler2=' ', down='|'))
#     for i in cap[n].keys():
#         print("                   ", i)
#         for k in sorted(cap[n][i]):
#             print("                                 {:<18} = {} {}".format(k, cap[n][i][k][0], cap[n][i][k][1]))
