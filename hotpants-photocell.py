# oh boy oh boy!
# It's project HOT_PANTS
from __future__ import print_function
import Adafruit_BBIO.UART as uart
import Adafruit_BBIO.ADC as adc
from Adafruit_Thermal import *
# import TMP102 as tmp
# import VCNL4000 as vcnl
import time
from serial import Serial
import random
import atexit
import sentence_generator as sg

theObj = 'APPLE'
sensor_pin = 'P9_40'
readings = []
fake = 0

def parseLen(text):
    L = []
    # add newlines to cause text to print properly
    # we need this because we're printing upside-down text
    # "call the police, it is faint-hearted" should be printed as
    # "rted" then linebreak then "Call the police, it is faint-hea"
    # which is "rted\nCall the police, it is faint-hea"
    # "faint-hearted\nCall the police, it is"

    if len(text) > Adafruit_Thermal.maxColumn: # 32 is defined by the printer; max chars per line
        r = len(text)%32
        L.append(text[-r:]+'\n')
        for i in reversed(range(len(text)/32)):
            L.append(text[i*32:(i+1)*32]+'\n')
    else:
        L.append(text)
    return ''.join(L)

def parse(text):
    r = text.split(' ')
    curLine = ''
    fin = []
    tally = 0
    for w in r:
        if len(w)+len(curLine) > (Adafruit_Thermal.maxColumn-1):
            fin.append(curLine)
            curLine = ''
            curLine+=w
        else:
            curLine+=' '+w
    # print curLine
    fin.append(curLine)
    fin[0] = fin[0].lstrip()
    fin.reverse()
    rt = '\n'.join(fin)
    return rt+'\n'

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
    r = adc.read(sensor_pin)
    readings.append(r)
    if len(readings)>WINDOW_SIZE:
        del readings[:-WINDOW_SIZE]
    
    avg = 0
    for i in readings:
        avg += (i/float(len(readings)))

    delta = r-rPast
    # delta = r-avg
    
    if r > rMax:
        rMax = r
        # does this merit an emission? Or should delta have to be > threshold?
    if r < rMin:
        rMin = r
        # does this merit an emission? Or should delta have to be > threshold?
    
    # print('%0.3f\t%0.3f\t%0.3f\t%0.3f\t%0.3f'%(r, delta, avg, rMin, rMax))

    if abs(delta) > emission_threshold:
        if len(readings)==WINDOW_SIZE: # this test prevents emissions before WINDOW_SIZE samples have been taken
            # print('emitting remark')
            noop = 0
            emit_remark(r, delta, avg)
        else:
            pass
    else:
        noop += 1
        if noop > noop_threshold:
            noop = 0
            # print('emitting dream')
            emit_dream(r, delta, avg)
    rPast = r

def emit_dream(r, delta, avg):
    global fake
    if fake == 5:
        fake = 0
        # norm = mapVals(r, rMin, rMax, 0.0, 0.999)
        # sen = sg.generate(theObj, (1.0-norm), delta, True) # reverse the range so 1=no light, 0=full light
        sen = sg.generate(theObj, r, delta, True) # reverse the range so 1=no light, 0=full light
        
        # printer.flush()
        printer.feed(1)
        printer.print('            . . .             ')
        printer.feed(1)

        slowPrint(parse(sen))
        
        # printer.flush()
        printer.feed(1)
        printer.print('            . . .             ')
        printer.feed(2)
    else:
        fake += 1
        # norm = mapVals(r, rMin, rMax, 0.0, 0.999)
        sen = sg.generate(theObj, r, delta, False) # reverse the range so 1=no light, 0=full light
        slowPrint(parse(sen))
        printer.feed(2)

def emit_remark(r, delta, avg):
    # norm = mapVals(r, rMin, rMax, 1.0, 0.0)
    # sen = sg.generate(theObj, (1.0-norm), delta, False) # reverse the range so 1=no light, 0=full light
    sen = sg.generate(theObj, r, delta, False) # reverse the range so 1=no light, 0=full light
    slowPrint(parse(sen))
    # slowPrint(str(norm))
    printer.feed(2)

def exit_handler():
    print('exiting')
    # adc.cleanup()
    # uart.cleanup() # not yet supported?

def mapVals(val, inMin, inMax, outMin, outMax):
        toRet = float(outMin + (float(outMax - outMin) * (float(val - inMin) / float(inMax - inMin))))
        print('turned %s into %s'%(val,toRet))
        toRet = clamp(toRet, outMin, outMax)
        return toRet

def clamp(val, tmin, tmax):
    if val > tmax:
        val = tmax
    if val < tmin:
        val = tmin
    return val


uart.setup("UART2")
adc.setup()
atexit.register(exit_handler)
printer = Adafruit_Thermal("/dev/ttyO2", 19200, timeout=5)
printer.begin()
printer.upsideDownOn()
printer.feed(3)
printer.print(parse('i am awake and I am APPLE (light)'))
printer.feed(1)
rPast = 0
rMax = 0 # all-time max sensor reading
rMin = 100000 # all-time min sensor reading
WINDOW_SIZE = 30 # size of moving-window avg
noop = 0 # number of intervals passed without a trigger
noop_threshold = 480
emission_threshold = 0.1 # changed this for vcnl4000, used to be 0.7

while True:
    checkSensor()
    time.sleep(0.5)