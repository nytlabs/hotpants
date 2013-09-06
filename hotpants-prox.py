# oh boy oh boy!
# It's project HOT_PANTS
from __future__ import print_function
import Adafruit_BBIO.UART as uart
from Adafruit_Thermal import *
import Adafruit_BBIO.ADC as adc
import Adafruit_BBIO.GPIO as gpio
import time
from serial import Serial
import random
import atexit
import VCNL4000 as vcnl

########### static
sensor_pin = 'P9_40'
extreme_lo = ['dark','inky','shadowed','midnight''black','sinister','dour','glowering','glum','moody','morose','saturnine','sour','sullen','benighted','obscure','blue','dingy','disconsolate','dismal','gloomy','grim','sorry','drab','drear','dreary','colored','coloured','dark-skinned','non-white','depressing','dispiriting']
mid_lo = ['shady','dim','grey','faint','weak','dim','shadowy','vague','wispy','feeble','light','swooning','light-headed','lightheaded','fainthearted','timid','faint-hearted','cloudy','muddy','murky','turbid']
mid_hi = ['light','shiny','clear','lustrous','diaphanous','filmy','gauze-like','gossamer','see-through','sheer','transparent','vaporous','vapourous','cobwebby']
extreme_hi = ['blinding','superbright','brilliant','vivid','brilliant','vivid','smart','burnished','lustrous','shining','shiny','undimmed','promising','sunny','sunshiny']

preamble = ['Now it is hella ','Oh, just a bit ','It is quite ','Gosh it is ','Well looky here, it is ','Suddenly: ','Call the police, it is ','After awhile: ','Things have changed; now it\'s more ']

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

def checkSensor():
    global rPast
    # r = adc.read(sensor_pin)
    r = v.readProximity()
    delta = r-rPast
    if abs(delta) > emission_threshold:
        if delta < 0:
            printer.print(parseLen(random.choice(preamble) + random.choice(extreme_hi)))
            printer.feed(1)
        else:
            printer.print(parseLen(random.choice(preamble) + random.choice(extreme_lo)))
            printer.feed(1)
        printer.print(str(r)+', delta: '+str(delta)) # debug - prints sensor val that elicited the text
        printer.feed(2)
    rPast = r

def exit_handler():
    pass
    # print 'exiting'
    # adc.cleanup()
    # uart.cleanup() # not yet supported?


v = vcnl.VCNL4000()
uart.setup("UART2")
# atexit.register(exit_handler)
printer = Adafruit_Thermal("/dev/ttyO2", 19200, timeout=5)
printer.begin()
printer.upsideDownOn()
printer.feed(1)
printer.print('i am awake and i am dreaming')
printer.feed(1)
printer.print(parseLen(str(time.ctime())))
printer.feed(1)
rPast = 0
emission_threshold = 100

while True:
    checkSensor()
    time.sleep(0.5)


# if __name__ == '__main__':
#     # adc.setup()
#     uart.setup("UART2")
#     atexit.register(exit_handler)
#     while True:
#         checkSensor()
#         time.sleep(0.5)