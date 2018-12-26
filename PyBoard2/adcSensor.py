import pyb
class adcSensor:
    def __init__(self, SCK, DT):
        self.pin_sck=pyb.Pin(SCK,  pyb.Pin.OUT)
        self.pin_dt=pyb.Pin(DT,  pyb.Pin.IN)
        self.pin_sck.high()
        pyb.udelay(100)
        self.pin_sck.low()
        self.m=2
        self.getValue()
        
        print("finished1")
    
    def setMode(self, s):
        self.m=s
        self.pin_sck.low()
        self.getValue()
    def averageValue(self, times):
        sum=0
        for i in range(0, times):
            sum=sum+self.getValue()
        
        return sum/times
            
    def getValue(self):
        #data=bytearray(3)
        temp=0
        while self.pin_dt.value(): None;
        #print("**")
        for i1 in range(0, 24):
            self.pin_sck.high()
#         
            temp=(temp<<1)
 #           print(self.pin_dt.value())
            temp=(temp)|self.pin_dt.value()
            self.pin_sck.low()
 #       print("**")
        for i in range(0, self.m):
            self.pin_sck.high()
            self.pin_sck.low()
        temp=temp^0x00800000
   #    print(data[2]<<16 | data[1] <<8 | data[0]  )
        return (temp)  
    
