import struct
import hashlib
import math
from PyBoard.adcSensorTest import adcobj
from PyBoard.i2cmod import Accel
from PyBoard.CRC import getCRC32
from pyb import UART
import uasyncio as asyncio
import pyb
from math import ceil
import os
from uasyncio import queues
from i2cmod import Accel
COMM=1
CONFI=2
    
    
REQT_WEIGHT=1
REQT_ACCELE=2
REQT_M_ACCELE=3
SET_TIME=4
CONN_REQT=5
    
START_ACCELE_REC=6
STOP_ACCELE_REC=7
START_WEIGHT_REC=8
TRANS=9

TRANS_ACCEL=10
class Message:
    def __init__(self,msg=None, com=None,val=None, buf=None):
        if buf!=None:
            self.mssg_type=struct.unpack('i', buf[0:4])[0]
            self.comm_type=struct.unpack('i', buf[4:8])[0]
            self.value=struct.unpack('f', buf[8:12])[0]
            self.CRC=struct.unpack('I', buf[12:16])[0]
            self.buff=buf
        elif msg!=None and com!=None and val!=None:
            self.mssg_type=msg
            self.comm_type=com
            self.value=val
            temp=struct.pack("i", msg)+struct.pack("i", com)+struct.pack("f", val)
            self.CRC=getCRC32(temp) & 0xFFFFFFFF
            temp2=struct.pack("I", self.CRC)
            self.buff=temp+temp2
    def isOkay(self):
        temp=getCRC32(self.buff[0:12])
        if temp==self.CRC:
            return True
        else:
            return False

    
def message(msg_type, com_type, val=0):
    return struct.pack('i',msg_type)+struct.pack('i',com_type)+struct.pack('f',com_type)
    
class Packet:
    def __init__(self, dat=None, p=None):
        if p==None:
            l=len(dat)
            self.__dat=dat
            res=[]
            self.dat_size=l
            nmb=math.ceil(l/4056)
            print("nmb"+ str(nmb))
            for ctr in range(0, nmb):
                pck_temp=self.dat[ctr*4056:(ctr+1)*4056]
                tdat=pck_temp
                l=len(tdat)
                print("4060-l="+str(4056-l))
                temp=bytes([0]*(4056-l))
                temp2=struct.pack('i',ctr)+struct.pack('i',l)+tdat+temp
                s=md5(temp2)
                s2=str.encode(s)
                temp2=temp2+s2
                print(len(temp2))
                res=res+[temp2]
            
            self.__pck=res
        else:
            self.dat_size=0
            self.__dat=[]
            print('')
            for tmp in p:
                l=int(struct.unpack('i', tmp[4:8] )[0])
                print("l="+str(l))
                self.__dat=self.__dat+[tmp[8 :(8+l)]]
                self.dat_size=self.dat_size+l
                
            self.__pck=p
    @property
    def dat(self):
        return self.__dat
      #  print(fin)

    @property
    def pck(self):
        return self.__pck
    
    def isOkay(self):
        
        temp=self.__dat
        s=md5(temp)
        s2=str.encode(s)
def count2():
        print("start")

class commUART:
    def __init__(self):
        self.uart6=UART(6, 115200)
        self.acc=Accel()
        self.queue=queues.Queue(100)
        #self.uart6.init(115200)
        
#    async def sender(self):
#        swriter = asyncio.StreamWriter(self.uart6, {})
#        while True:
#            await swriter.awrite('Hello uart\n')
#            await asyncio.sleep(2)
    def count3(self):
        for i in range(0, 10):
            
            print("str="+str(i))
            pyb.delay(1000)
    
    def captureAccel(self):
        
        print("capture")
    async def receiver(self):
        sreader = asyncio.StreamReader(self.uart6)
        swriter = asyncio.StreamWriter(self.uart6, {})
        while True:

            res=await sreader.read(16)
            print("recievd")
            m=Message(buf=res)
            print(m.buff)
            print(m.CRC)
            print(m.isOkay())
            if m.isOkay():
                print("is Okay")
                if m.comm_type==REQT_ACCELE:
                    fsize=os.stat('PyBoard/record.dat')[6]
                    print("reqt_accel")
                    print(fsize)
                    tm=Message(CONFI,REQT_ACCELE,fsize)
                    await swriter.awrite(tm.buff)
                    f=open('PyBoard/record.dat', 'rb')
                    s=int(ceil(fsize/4096))
                    
                    for i in range(0, s):
                        print(i)
                     #   pyb.delay(200)
                        m=f.read(4096)
                        await swriter.awrite(m)
                    f.close()
                    print("done")

                elif m.comm_type==REQT_WEIGHT:
                    print("REQT_WEIGHT")
                    weight=1.0
                    self.queue.put_nowait(self.count3)
                    print("s="+str(self.queue.qsize()))
                    tm=Message(CONFI, REQT_WEIGHT, weight)
                elif m.comm_type==START_ACCELE_REC:
                    print("START_ACCEL_REC")
                    rcd=open("PyBoard/record.dat", "w")
                    lp=True
                    while lp:
                        tup=self.acc.readAccel()
                        print(tup)
                        rcd.write(str(tup[0])+","+str(tup[1])+","+str(tup[2])+"\n")
                        if self.uart6.any()!=0:
                            res=await sreader.read(16)
                            m=Message(buf=res)
                            if m.isOkay() and m.mssg_type==COMM and m.comm_type==STOP_ACCELE_REC:
                                lp=False
                                tm=Message(CONFI, STOP_ACCELE_REC, 0)
                                await swriter.awrite(tm.buff)
                                print("stoped")
                                rcd.close()
#            
            
    async def commCycle(self):
        i=0
        while True:
            i=i+1
            await asyncio.sleep(0.1)
            if not self.queue.empty():
                print("here3")
               # await asyncio.sleep(1)
                item=self.queue.get_nowait()
                print(item)
                item()
                print("funct")
            
#            print(a.isOkay)
    def start(self):
        loop = asyncio.get_event_loop()
#        loop.create_task(self.sender())
        loop.create_task(self.receiver())
#        loop.create_task(self.count())
        loop.create_task(self.commCycle())
        loop.run_forever()
        print("start")
        
        
