import struct
import hashlib
import math
import pyb
from PyBoard2.CRC import getCRC32

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
DUTY=10

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
        s2=str.encode(s)