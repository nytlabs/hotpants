# oh boy oh boy!
# It's project HOT_PANTS
from __future__ import print_function
import Adafruit_BBIO.UART as uart
from Adafruit_Thermal import *
import Adafruit_BBIO.ADC as adc
import Adafruit_BBIO.GPIO as gpio
import TMP102 as tmp
import time
from serial import Serial
import random
import atexit

t = tmp.TMP102()
sensor_pin = 'P9_40'
# extreme_lo = ['dark','inky','shadowed','midnight''black','sinister','dour','glowering','glum','moody','morose','saturnine','sour','sullen','benighted','obscure','blue','dingy','disconsolate','dismal','gloomy','grim','sorry','drab','drear','dreary','colored','coloured','dark-skinned','non-white','depressing','dispiriting']
extreme_lo = ['stale','cold','dusty','moth-eaten','frigid','arctic','gelid','glacial','icy','polar','frosty','frozen','wintry','cold-blooded','inhuman','insensate','insentient']
# mid_lo = ['shady','dim','grey','faint','weak','dim','shadowy','vague','wispy','feeble','light','swooning','light-headed','lightheaded','fainthearted','timid','faint-hearted','cloudy','muddy','murky','turbid']
# mid_hi = ['light','shiny','clear','lustrous','diaphanous','filmy','gauze-like','gossamer','see-through','sheer','transparent','vaporous','vapourous','cobwebby']
# extreme_hi = ['blinding','superbright','brilliant','vivid','brilliant','vivid','smart','burnished','lustrous','shining','shiny','undimmed','promising','sunny','sunshiny']
extreme_hi = ['raging','hot','angry','furious','tempestuous','wild','blistering','acerb','acerbic','acid','acrid','bitter','caustic','sulfurous','sulphurous','virulent','vitriolic','blistery','red-hot','scalding','scathing','venomous','vituperative','juicy','luscious','toothsome','voluptuous','sizzling','live','unrecorded','bouncy','lively','resilient','springy','alive']
preamble = ['Now it is hella ','Oh, just a bit ','It is quite ','Gosh it is ','Well looky here, it is ','Suddenly: ','Call the police, it is ','After awhile: ','Things have changed; now it\'s more ','Hey now! It is very ']

printer = Adafruit_Thermal("/dev/ttyO2", 19200, timeout=5)
printer.begin()
printer.upsideDownOn()
printer.feed(3)
printer.print("o hai")
printer.feed(1)
rPast = 0
emission_threshold = 0.7

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
	r = t.getTemp()

	if abs(r-rPast) > emission_threshold:
		# if r < 0.25:
		# 	printer.print(parseLen(random.choice(preamble) + random.choice(extreme_lo)))
		# 	printer.feed(1)
		# elif r < 0.5:
		# 	printer.print(parseLen(random.choice(preamble) + random.choice(mid_lo)))
		# 	printer.feed(1)
		# elif r < 0.75:
		# 	printer.print(parseLen(random.choice(preamble) + random.choice(mid_hi)))
		# 	printer.feed(1)
		# else:
		# 	printer.print(parseLen(random.choice(preamble) + random.choice(extreme_hi)))
		# 	printer.feed(1)
		if r < rPast:
			printer.print(parseLen(random.choice(preamble) + random.choice(extreme_lo)))
			printer.feed(1)
		else:
			printer.print(parseLen(random.choice(preamble) + random.choice(extreme_hi)))
			printer.feed(1)
		printer.print(r)
		printer.feed(2)
	rPast = r

def exit_handler():
    pass
    # print 'exiting'
    # adc.cleanup()
    # uart.cleanup() # not yet supported?

if __name__ == '__main__':
	adc.setup()
	uart.setup("UART2")
	atexit.register(exit_handler)
	while True:
		checkSensor()
		time.sleep(0.5)