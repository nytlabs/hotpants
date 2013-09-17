from Adafruit_Thermal import *

maxCol = 32
printer = Adafruit_Thermal("/dev/ttyO2", 19200, timeout=5)
printer.begin()
printer.upsideDownOn()

def parse(text):
    r = text.split(' ')
    # r.reverse()
    curLine = []
    fin = []
    for w in r:
    	if len(w)+len(curLine) > maxCol:
    		fin.append(curLine)
    		curLine = []
    		curLine.append(w)
    	else:
    		curLine.join(w)
    print curLine
    print fin
