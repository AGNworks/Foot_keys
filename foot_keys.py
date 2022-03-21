import sys
import glob
from tkinter import *
from tkinter import messagebox
from pynput.keyboard import Controller, Key
from scipy.fftpack import shift
import serial
#import time

root = Tk()
keyboard = Controller()
ser = serial.Serial()

#global variables
button_ind = [1, 2, 3]
on_off = False
stringy = StringVar()
shift_on = False

""" Lists serial port names

    :raises EnvironmentError:
        On unsupported or unknown platforms
    :returns:
        A list of the serial ports available on the system
"""
if sys.platform.startswith('win'):
    ports = ['COM%s' % (i + 1) for i in range(256)]
elif sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):
    # this excludes your current terminal "/dev/tty"
    ports = glob.glob('/dev/tty[A-Za-z]*')
elif sys.platform.startswith('darwin'):
    ports = glob.glob('/dev/tty.*')
else:
    raise EnvironmentError('Unsupported platform')

serial_names = []
for port in ports:
    try:
        s = serial.Serial(port)
        s.close()
        serial_names.append(port)
    except (OSError, serial.SerialException):
        pass
print(serial_names)

#functions
def connect_ser():
    #print(ser_variable.get())
    btn1.configure(bg="#42f563")
    porto = str(ser_variable.get())
    ser.baudrate = 115200
    ser.port = porto
    ser.open()

def btn_click():
    global on_off
    global button_ind
    button_order = ['esc','esc','esc']
    button_order[0] = str(value_inside1.get())
    button_order[1] = str(value_inside2.get())
    button_order[2] = str(value_inside3.get())
    for i in range(len(button_order)):
        if button_order[i] == 'Shift':
            button_ind[0] = i+1
        elif button_order[i] == 'Esc':
            button_ind[1] = i+1
        elif button_order[i] == 'Enter':
            button_ind[2] = i+1
    print(button_order)
    
    if on_off == True:
        on_off = False
        btn.configure(bg="#428df5")
        stringy.set('Off')

    else:
        on_off = True
        btn.configure(bg="#42f563")
        stringy.set('On')

def on_func():
    global on_off
    global shift_on
    ard_input = "0"
    if on_off == True:
        if (ser.inWaiting() > 0):
            ard_input = str(ser.read())
            #print(len(ard_input))

        if (str(button_ind[0]) in ard_input and shift_on == False):     #Shift
            keyboard.press(Key.shift_l)
            shift_on = True
            #print('shift_on')
         
        if (str(button_ind[0]) not in ard_input and shift_on == True):   #Shift
            keyboard.release(Key.shift_l)
            shift_on = False
            #print('shift_off')
        
        if (str(button_ind[1]) in ard_input):                          #Esc 
            keyboard.press(Key.esc)
            keyboard.release(Key.esc)
            #print('ESC')

        if (str(button_ind[2]) in ard_input):                      #Enter
            keyboard.press(Key.enter)
            keyboard.release(Key.enter)
            #print('enter')

    status.after(200,on_func)

def on_closing():
    if messagebox.askokcancel("Quit", "Really?"):
        #print("bye-bye")
        ser.close()
        root.destroy()

def change_shift():
    print(" change_shift")

def change_esc():
    print(" change_esc")

def change_enter():
    print(" change_enter")

root.geometry('300x250')
root.resizable(width=False, height=False)
root.title("Foot keys")

ser_variable = StringVar(root)
ser_variable.set('Select')

options_list = ["Shift", "Esc", "Enter"]
value_inside1 = StringVar(root)
value_inside1.set(options_list[0])

value_inside2 = StringVar(root)
value_inside2.set(options_list[1])

value_inside3 = StringVar(root)
value_inside3.set(options_list[2])

label1 = Label(root, text='Choose the COM port and press Connect button!')
label1.place(x=10, y=10)

w = OptionMenu(root, ser_variable, *serial_names)
w.place(x=10,y=40)

btn1 = Button(root, text = 'Connect', bg = '#428df5', command = connect_ser)
btn1.place(x=100, y=42)

label2 = Label(root, text='Choose order of buttons!')
label2.place(x=10, y=80)

w1 = OptionMenu(root, value_inside1, *options_list)
w1.place(x=10,y=120)

w2 = OptionMenu(root, value_inside2, *options_list)
w2.place(x=100,y=120)

w3 = OptionMenu(root, value_inside3, *options_list)
w3.place(x=190,y=120)

btn = Button(root, text = 'START', bg = '#428df5', command = btn_click)
btn.place(x=10, y=180)

status = Label(root, textvariable= stringy)
stringy.set('None')
status.place(x=100, y=180)


root.protocol("WM_DELETE_WINDOW", on_closing)
on_func()
root.mainloop()