from pyb import I2C
import struct
class Accel:
    def __init__(self):
        print("start")
        self.i2c = I2C(2, I2C.MASTER)             # create and init as a master
        self.i2c.init(I2C.MASTER, baudrate=100000) # init as a master
            # init as a slave with given address
        print("initialized")
        self.i2c.is_ready(0x1D) 
        #i2c.send(0x00, addr=0x1D)
        a=self.i2c.mem_read(1, 0x1D, 0) 
        print(a)
        self.i2c.mem_write(0x31, 0x1D, 0x31)
#        self.i2c.send(0x31, 0x1D)
#        self.i2c.send(0x31, 0x1D)
        self.i2c.mem_write(0x08, 0x1D, 0x2D)

        #print(data)
    def readAccel(self):
        buf=self.i2c.mem_read(6, 0x1D, 0x32) 
        x=struct.unpack('h', buf[0:2])
        y=struct.unpack('h', buf[2:4])
        z=struct.unpack('h', buf[4:6])
        
#        x=a[1]<<8 | a[0]
#        y=a[3]<<8 | a[2]
#        z=a[5]<<8 | a[4]
        print(" x1 = "+str(x)+" y = "+str(y)+" z = "+str(z))
        return(x, y, z)
