# Example class for talking to the VCNL4000 i2c proximity/light sensor
# Very heavily based on an Arduino demo written by Adafruit - thanks!
# (Python class by AKA MEDIA SYSTEM, also public domain)
# To use: Connect VCC to 3.3-5V (5V is best if it is available), GND to
#         ground, SCL to i2c clock (on classic arduinos, Analog 5), SDA
#         to i2c data (on classic arduinos Analog 4). The 3.3v pin is
#         an ouptut if you need 3.3V
# This sensor is 5V compliant so you can use it with 3.3 or 5V micros

# You can pick one up at the Adafruit shop: www.adafruit.com/products/466

from Adafruit_I2C import Adafruit_I2C
import time

class VCNL4000():
  # the i2c address
  VCNL4000_ADDRESS = 0x13

  # commands and constants
  VCNL4000_COMMAND = 0x80
  VCNL4000_PRODUCTID = 0x81
  VCNL4000_IRLED = 0x83
  VCNL4000_AMBIENTPARAMETER = 0x84
  VCNL4000_AMBIENTDATA = 0x85
  VCNL4000_PROXIMITYDATA = 0x87
  VCNL4000_SIGNALFREQ = 0x89
  VCNL4000_PROXIMITYADJUST = 0x8A

  VCNL4000_3M125 = 0
  VCNL4000_1M5625 = 1
  VCNL4000_781K25 = 2
  VCNL4000_390K625 = 3

  VCNL4000_MEASUREAMBIENT = 0x10
  VCNL4000_MEASUREPROXIMITY = 0x08
  VCNL4000_AMBIENTREADY = 0x40
  VCNL4000_PROXIMITYREADY = 0x20

  def __init__(self, *args, **kwargs):
    self.i2c = Adafruit_I2C(self.VCNL4000_ADDRESS)
    rev = self.i2c.readU8(self.VCNL4000_PRODUCTID)
    if((rev & 0xF0) != 0x10):
      print 'Sensor not found wtf'
    self.i2c.write8(self.VCNL4000_IRLED, 10) # set to 10 * 10mA = 100mA
    current = self.i2c.readU8(self.VCNL4000_IRLED)
    print 'we think current is set to ', current
    sigFreq = self.i2c.readU8(self.VCNL4000_SIGNALFREQ)
    print 'we think sigFreq is ',sigFreq
    self.i2c.write8(self.VCNL4000_PROXIMITYADJUST, 0x81)
    proxAdj = self.i2c.readU8(self.VCNL4000_PROXIMITYADJUST)
    print 'we think proximityAdjust is ',proxAdj

  def setLEDcurrent(self, cur):
    if (cur > 20) or (cur < 0):
      cur = 10
    self.i2c.write8(self.VCNL4000_IRLED, cur)

  def continuousConversionOn(self):
    self.i2c.write8(self.VCNL4000_AMBIENTPARAMETER, 0x89)

  def continuousConversionOff(self):
    self.i2c.write8(self.VCNL4000_AMBIENTPARAMETER, 0x09) 

  def setSignalFreq(self, freq):
    # Setting the proximity IR test signal frequency. The proximity measurement is using a square IR 
    # signal as measurement signal. Four different values are possible: 
    # 00 = 3.125 MHz
    # 01 = 1.5625 MHz
    # 02 = 781.25 kHz (DEFAULT)
    # 03 = 390.625 kHz
    if freq not in [00, 01, 02, 03]:
      freq = 02
      print 'value must be an int between 0 and 3. Using 2 as default.'
    self.i2c.write8(self.VCNL4000_SIGNALFREQ, freq)

  def getSignalFreq(self):
    return self.i2c.readU8(self.VCNL4000_SIGNALFREQ)

  def setProximityAdjust(self, prox):
    pass
    # datasheet makes adjusting this look less wise than I thought. Ignoring for now.
    # Should basically be set to 0x81 = 129

  def getProximityAdjust(self):
    return self.i2c.readU8(self.VCNL4000_PROXIMITYADJUST)

  def readProximity(self):
    self.i2c.write8(self.VCNL4000_COMMAND, self.VCNL4000_MEASUREPROXIMITY)
    while True:
      result = self.i2c.readU8(self.VCNL4000_COMMAND)
      if(result & self.VCNL4000_PROXIMITYREADY):
        h = self.i2c.readList(self.VCNL4000_PROXIMITYDATA,2)
        result = ((h[0]<<8)|h[1])>>4
        return result
      time.sleep(0.001)

  def readAmbient(self):
    self.i2c.write8(self.VCNL4000_COMMAND, self.VCNL4000_MEASUREAMBIENT)
    while True:
      result = self.i2c.readU8(self.VCNL4000_COMMAND)
      if(result & self.VCNL4000_AMBIENTREADY):
        h = self.i2c.readList(self.VCNL4000_AMBIENTDATA,2)
        result = ((h[0]<<8)|h[1])>>4
        return result
      time.sleep(0.001)
