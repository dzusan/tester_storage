from auto_tests import *

# Write initial conditions
conditionLog()

# Measure programs startup time
progsList = {\
"AD17":["E:\\portable\\pro\\Altium\\AD17\\DXP.EXE", 0],\
"AD18":["E:\\portable\\pro\\Altium\\AD18\\X2.EXE", 0],\
"GIMP 2.9":["E:\\portable\\media\\GIMP 2.9\\bin\\gimp-2.9.exe", 0],\
"Firefox 56":["E:\\portable\\usr\\Mozilla Firefox\\firefox.exe", 0],\
"iTunes":["C:\\Program Files\\iTunes\\iTunes.exe", 0],\
}
for key in progsList.keys():
    progsList[key][1] = startupMeter(progsList[key][0])
    waitingIdle(10)

# Measure video convertion time
videosList = {\
"VID1":["videos\\test_video.mp4", "videos\\converted_video.avi", 0],\
"VID2":["videos\\test_video.mp4", "videos\\converted_video.mov", 0],\
}
for key in videosList.keys():
    videosList[key][2] = videoConvert(videosList[key][0], videosList[key][1])
    waitingIdle(10)
