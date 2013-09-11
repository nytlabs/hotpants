# oh boy oh boy!
# It's project HOT_PANTS
from __future__ import print_function
import Adafruit_BBIO.UART as uart
from Adafruit_Thermal import *
# import TMP102 as tmp
import VCNL4000 as vcnl
import time
from serial import Serial
import random
import atexit
import sentence_generator as sg

theObj = 'BLOCKS'

v = vcnl.VCNL4000()
v.continuousConversionOn()
readings = []
# sensor_pin = 'P9_40'
# extreme_lo = ['dark','inky','shadowed','midnight''black','sinister','dour','glowering','glum','moody','morose','saturnine','sour','sullen','benighted','obscure','blue','dingy','disconsolate','dismal','gloomy','grim','sorry','drab','drear','dreary','colored','coloured','dark-skinned','non-white','depressing','dispiriting']
# extreme_lo = ['stale','cold','dusty','moth-eaten','frigid','arctic','gelid','glacial','icy','polar','frosty','frozen','wintry','cold-blooded','inhuman','insensate','insentient']
# mid_lo = ['shady','dim','grey','faint','weak','dim','shadowy','vague','wispy','feeble','light','swooning','light-headed','lightheaded','fainthearted','timid','faint-hearted','cloudy','muddy','murky','turbid']
# mid_hi = ['light','shiny','clear','lustrous','diaphanous','filmy','gauze-like','gossamer','see-through','sheer','transparent','vaporous','vapourous','cobwebby']
# extreme_hi = ['blinding','superbright','brilliant','vivid','brilliant','vivid','smart','burnished','lustrous','shining','shiny','undimmed','promising','sunny','sunshiny']
# extreme_hi = ['raging','hot','angry','furious','tempestuous','wild','blistering','acerbic','acid','acrid','bitter','caustic','sulfurous','sulphurous','virulent','vitriolic','blistery','red-hot','scalding','scathing','venomous','vituperative','juicy','luscious','toothsome','voluptuous','sizzling','live','unrecorded','bouncy','lively','resilient','springy','alive']
# preamble = ['Now it is hella ','Oh, just a bit ','It is quite ','Gosh it is ','Well looky here, it is ','Suddenly: ','Call the police, it is ','After awhile: ','Things have changed; now it\'s more ','Hey now! It is very ']
# dream = ['i am falling', 'i am walking and falling', 'i had to take a test', 'i have eaten an embarrassing amount of gum']

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
    r = v.readProximity()
    readings.append(r)
    if len(readings)>WINDOW_SIZE:
        del readings[:-WINDOW_SIZE]
    
    avg = 0
    for i in readings:
        avg += (i/float(len(readings)))

    delta = r-rPast
    # delta = r-avg

    print(r, delta, avg)
    
    if r > rMax:
        rMax = r
        # does this merit an emission? Or should delta have to be > threshold?
    if r < rMin:
        rMin = r
        # does this merit an emission? Or should delta have to be > threshold?

    if abs(delta) > emission_threshold:
        if len(readings)==WINDOW_SIZE: # this test prevents emissions before WINDOW_SIZE samples have been taken
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
    norm = mapVals(r,rMin, rMax, 0.999, 0.0) # reversed this because for vcnl4000, hi means close
    sen = sg.generate(theObj, norm, delta, True)
    slowPrint(parseLen(sen))
    printer.feed(1)
    slowPrint(parseLen('DREAM: '+str(time.ctime())))
    printer.feed(1)

def emit_remark(r, delta, avg):
    norm = mapVals(r,rMin, rMax, 0.999, 0.0)
    sen = sg.generate(theObj, norm, delta, False)
    slowPrint(parseLen(sen))
    printer.feed(1)

def exit_handler():
    pass
    # print 'exiting'
    # adc.cleanup()
    # uart.cleanup() # not yet supported?

def mapVals(val, inMin, inMax, outMin, outMax):
        toRet = outMin + (outMax - outMin) * ((val - inMin) / (inMax - inMin))
        return toRet

uart.setup("UART2")
printer = Adafruit_Thermal("/dev/ttyO2", 19200, timeout=5)
printer.begin()
printer.upsideDownOn()
printer.feed(3)
printer.print('i am awake and I have a VCNL4000')
printer.feed(1)
rPast = 0
rMax = 0 # all-time max sensor reading
rMin = 0 # all-time min sensor reading
WINDOW_SIZE = 30 # size of moving-window avg
noop = 0 # number of intervals passed without a trigger
noop_threshold = 480
emission_threshold = 5 # changed this for vcnl4000, used to be 0.7

while True:
    checkSensor()
    time.sleep(0.5)