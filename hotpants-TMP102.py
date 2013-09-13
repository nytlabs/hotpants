# oh boy oh boy!
# It's project HOT_PANTS
from __future__ import print_function
import Adafruit_BBIO.UART as uart
from Adafruit_Thermal import *
import TMP102 as tmp
import time
from serial import Serial
import random
import atexit
import sentence_generator as sg

# emit something every minute
# map degC to human scale of hot, cold, and temperate

theObj = 'MUG'

humanCold = 20
humanHot = 30

t = tmp.TMP102()
readings = []

def parseLen(text):
    L = []
    # add newlines to cause text to print properly
    # we need this because we're printing upside-down text
    # "call the police, it is faint-hearted" should be printed as
    # "rted" then linebreak then "Call the police, it is faint-hea"
    # which is "rted\nCall the police, it is faint-hea"

    if len(text) > Adafruit_Thermal.maxColumn: # 32 is defined by the printer; max chars per line
        r = len(text)%32
        L.append(text[-r:]+'\n')
        for i in reversed(range(len(text)/32)):
            L.append(text[i*32:(i+1)*32]+'\n')
    else:
        L.append(text)
    return ''.join(L)

def slowPrint(text):
    for i in text.splitlines():
        printer.print(i+'\n')
        time.sleep(0.1)

def checkSensor():
    global rPast
    global rMin
    global rMax
    global noop
    # change this to whatever get-readings call we need
    r = t.getTemp()
    readings.append(r)
    if len(readings)>WINDOW_SIZE:
        del readings[:-WINDOW_SIZE]
    
    avg = 0
    for i in readings[-WINDOW_SIZE:]:
        avg += (i/float(WINDOW_SIZE))

    delta = r-avg
    
    print(r, delta, avg)
    
    if r > rMax:
        rMax = r
        # does this merit an emission? Or should delta have to be > threshold?
    if r < rMin:
        rMin = r
        # does this merit an emission? Or should delta have to be > threshold?

    if abs(delta) > emission_threshold:
        if len(readings)==WINDOW_SIZE:
            print('emitting remark')
            noop = 0
            emit_remark(r, delta, avg)
        else:
            pass
    else:
        noop += 1
        if noop > noop_threshold:
            noop = 0
            print('emitting dream')
            emit_dream(r, delta, avg)
    rPast = r

def emit_dream(r, delta, avg):
    r = random.randint(0,5)
    if r==1:
        emit_remark(r, delta, avg)
    else:
        norm = mapVals(r,humanCold, humanHot, 0.0, 0.999)
        sen = sg.generate(theObj, norm, delta, True)
        slowPrint(parseLen(sen))
        printer.feed(2)
        slowPrint(parseLen(str(time.ctime()))+'\n')

def emit_remark(r, delta, avg):
    norm = mapVals(r,humanCold, humanHot, 0.0, 0.999)
    sen = sg.generate(theObj, norm, delta, False)
    slowPrint(parseLen(sen))
    printer.feed(2)

def exit_handler():
    pass
    # print 'exiting'
    # adc.cleanup()
    # uart.cleanup() # not yet supported?

def mapVals(val, inMin, inMax, outMin, outMax):
        toRet = float(outMin + float(outMax - outMin) * float(float(val - inMin) / float(inMax - inMin)))
        return toRet

uart.setup("UART2")
printer = Adafruit_Thermal("/dev/ttyO2", 19200, timeout=5)
printer.begin()
printer.upsideDownOn()
printer.feed(3)
printer.print(parseLen('i am awake and I am MUG (thermal)'))
printer.feed(1)
rPast = 0
rMax = 0 # all-time max sensor reading
rMin = 0 # all-time min sensor reading
WINDOW_SIZE = 30 # size of moving-window avg
noop = 0 # number of intervals passed without a trigger
noop_threshold = 480
emission_threshold = 0.7

while True:
    checkSensor()
    time.sleep(0.5)