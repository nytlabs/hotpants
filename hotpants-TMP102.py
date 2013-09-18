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
humanHot = 32.5

t = tmp.TMP102()
readings = []
fake = 0
recent = False
crescent = 10 # this counter gets incremented everytime we sample; it gets reset when we emit a remark
choke = 10 # this is a threshold level - until we've ignored choke number of emissions, we don't emit

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
    global crescent
    # change this to whatever get-readings call we need
    r = t.getTemp()
    readings.append(r)
    if len(readings)>WINDOW_SIZE:
        recent = False
        del readings[:-WINDOW_SIZE]
    
    avg = 0
    for i in readings[-WINDOW_SIZE:]:
        avg += (i/float(WINDOW_SIZE))

    delta = r-avg
    
    if r > rMax:
        rMax = r
        # does this merit an emission? Or should delta have to be > threshold?
    if r < rMin:
        rMin = r
        # does this merit an emission? Or should delta have to be > threshold?

    if abs(delta) > emission_threshold:
        crescent += 1
        if len(readings)==WINDOW_SIZE:
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
        norm = mapVals(r,humanCold, humanHot, 0.0, 0.999)
        sen = sg.generate(theObj, norm, delta, True)
        
        printer.flush()
        printer.feed(1)
        # for i in xrange(Adafruit_Thermal.maxColumn):
        #     printer.writeBytes(0xB0)
        # printer.flush()
        printer.print('            . . .             ')

        slowPrint(parse(sen))
        
        printer.flush()
        printer.feed(1)
        # for i in xrange(Adafruit_Thermal.maxColumn):
        #     printer.writeBytes(0xB0)
        # printer.flush()
        printer.print('            . . .             ')
        printer.feed(2)
    else:
        fake += 1
        norm = mapVals(r,humanCold, humanHot, 0.0, 0.999)
        sen = sg.generate(theObj, norm, delta, False)
        slowPrint(parse(sen))
        printer.feed(2)

def emit_remark(r, delta, avg):
    global crescent
    global choke
    global rPast
    print('crescent is ', crescent)
    print(r-rPast)
    if r-rPast <= 0:
        if crescent > choke:
            crescent = 0
            norm = mapVals(r,humanCold, humanHot, 0.0, 0.999)
            sen = sg.generate(theObj, norm, delta, False)
            slowPrint(parse(sen))
            printer.feed(2)
        else:
            print('we are throttling now; readings to follow')
            print(r, delta, avg)
    else:
        norm = mapVals(r,humanCold, humanHot, 0.0, 0.999)
        sen = sg.generate(theObj, norm, delta, False)
        slowPrint(parse(sen))
        printer.feed(2)

def exit_handler():
    pass
    # print 'exiting'
    # adc.cleanup()
    # uart.cleanup() # not yet supported?

def mapVals(val, inMin, inMax, outMin, outMax):
        toRet = float(outMin + float(outMax - outMin) * float(float(val - inMin) / float(inMax - inMin)))
        return clamp(toRet, outMin, outMax)

def clamp(val, tmin, tmax):
    if val > tmax:
        val = tmax
    if val < tmin:
        val = tmin
    return val

uart.setup("UART2")
printer = Adafruit_Thermal("/dev/ttyO2", 19200, timeout=5)
printer.begin()
printer.upsideDownOn()
printer.feed(3)
printer.print(parse('i am awake and I am MUG (thermal)'))
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
