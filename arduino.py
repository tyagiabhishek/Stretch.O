import time
import serial
import subprocess
count = 0
while (count < 2):
    proceed = input("You are sitting since a long time. Its time to take a break? (Y/N)")
    if (proceed == "N"):
        time.sleep(100)
    else:
        break

timeout = int(input("Enter the value after which your computer should return to normal brightness in seconds: "))
ser = serial.Serial('/dev/cu.usbmodem14201', 9600, timeout=timeout)

brightness = 1
delta = 0
while True:
    message = ser.readline()
    if ('MOVEMENT' in str(message)):
        delta = delta + 1
        print("increased delta " + str(delta))
        if (brightness > 0.1 and delta > 3):
            print("reducing brightness")
            brightness = brightness - 0.1
            delta = 0
            s = subprocess.check_call("brightness " + str(brightness), shell=True)

    else:
        brightness = 1
        delta = 0
        s = subprocess.check_call("brightness " + str(brightness), shell=True)
    time.sleep(1)
