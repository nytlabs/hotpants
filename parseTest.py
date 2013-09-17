from Adafruit_Thermal import *

maxCol = 32
printer = Adafruit_Thermal("/dev/ttyO2", 19200, timeout=5)
printer.begin()
printer.upsideDownOn()

def parse(text):
    r = text.split(' ')
    # r.reverse()
    curLine = ''
    fin = []
    tally = 0
    for w in r:
    	if len(w)+tally > (maxCol-1):
    		fin.append(curLine)
    		curLine = []
    		tally = 0
    		curLine+=w
    	else:
    		curLine+=' '+w
    		tally += len(w)+1
    print curLine
    print fin
