import tkinter as tk
import time
import serial
import subprocess


class app1:
    def __init__(self, master):
        self.master = master
        self.skipcount = 0
        self.frame = tk.Frame(self.master)
        self.label = tk.Label(self.master, text=" You're working since long! Take a break maybe.")
        self.button1 = tk.Button(self.frame, text="Yes", command=self.close_window)
        self.button2 = tk.Button(self.frame, text="No", command=self.wait)
        self.label.pack()
        self.button1.pack(side="left")
        self.button2.pack(side="right")
        self.frame.pack()

    def wait(self):
        if (self.skipcount < 2):
            self.master.iconify()
            time.sleep(1)
            self.master.deiconify()
            self.skipcount = self.skipcount + 1
        else:
            self.button1.pack_forget()
            self.button2.pack_forget()
            self.label.config(text="The code is running now :)")
            time.sleep(2)
            self.newwindow = tk.Toplevel(self.master)
            self.app = app2(self.newwindow)
            self.master.iconify()

    def close_window(self):
        self.newwindow = tk.Toplevel(self.master)
        self.app = app2(self.newwindow)
        self.button1.pack_forget()
        self.button2.pack_forget()
        self.label.config(text="The code is running now :)")
        self.master.iconify()


class app2:
    def __init__(self, master):
        self.master = master
        self.label = tk.Label(self.master, text="How long a break do you think you need?")
        self.E1 = tk.Entry(self.master, bd=5)
        self.button = tk.Button(self.master, text="OK", command=self.call_code)
        self.label.pack()
        self.E1.pack()
        self.button.pack()

    def call_code(self):
        timeout = int(self.E1.get())
        self.master.destroy()
        execute_code(timeout)


def execute_code(timeout):
    print("code started with timeout " + str(timeout))
    time.sleep(5)
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
                brightness = brightness - 0.2
                delta = 0
                s = subprocess.check_call("brightness " + str(brightness), shell=True)

        else:
            brightness = 1
            delta = 0
            s = subprocess.check_call("brightness " + str(brightness), shell=True)
        time.sleep(1)


def main():
    root = tk.Tk()
    app = app1(root)
    root.mainloop()


if __name__ == '__main__':
    main()