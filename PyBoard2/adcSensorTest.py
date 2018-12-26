import pyb
from adcSensor import adcSensor

class adcobj:
    def __init__(self):
        self.adc=adcSensor('Y3', 'Y4')
        self.tare1=0
        self.tare2=0
        pyb.delay(200)
        self.adc.setMode(3)
        pyb.delay(200)
        self.tare1=self.adc.averageValue(40)
        self.adc.setMode(2)
        pyb.delay(200)
        self.tare2 = self.adc.averageValue(40)
        print("tare1 = "+str(self.tare1))
        print("tare2 = "+str(self.tare2))
        #print(tare2)

    def getData(self):
        self.adc.setMode(3)
        print("--")
        print((self.adc.averageValue(20)- self.tare1)/973.3)
            
        self.adc.setMode(2)
        print((self.adc.averageValue(20)- self.tare2)/973.3)
        print("--")
    def repGet(self):
        while True:
            pyb.delay(100)
            self.getData()
