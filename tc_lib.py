import sys
import time
import numpy as np
try:
    import serial
except:
    import pip
    pip.main(['install','pyserial'])
    import serial

class tc_lib(object):

    def __init__(self, port=None, baud=115200):
        #port = self.findPort()
        self.port = serial.Serial(port, baud, timeout=2)
        self.port.flushInput()
        self.port.flushOutput()
        time.sleep(2)
        print('Device connected throught on port ' + port)
        
    def build_cmd_str(seft,cmd, value=None):
        if value:
            value = ' '.join(map(str, value))
        else:
            value = ''
        return ("{cmd} {value}\r\n".format(cmd=cmd, value=value))
        #return ("{cmd} {value}\n".format(cmd=cmd, value=value))
   
    def write(self,cmd,pwm):       
        cmd_ = self.build_cmd_str(cmd,(pwm,))
        try:
            self.port.write(cmd_.encode())
            self.port.flush()
        except:
            return None
        return self.port.readline().decode('UTF-8').replace("\r\n", "")
    
    def read(self,cmd):
        cmd_ = self.build_cmd_str(cmd,'') # create string of command
        try:
            self.port.write(cmd_.encode())
            self.port.flush()
        except Exception:
            return None
        return self.port.readline().decode('UTF-8').replace("\r\n", "")
    
    def Q1(self,current):
        current = max(0.0,min(100.0,current)) 
        self.write('Q1',current)
        return current

    def set_I2(self,current):
        current = max(0.0,min(100.0,current)) 
        self.write('I2',current)
        return current

    def close(seft):
        try:
            seft.port.close()
            print('Device disconnected successfully')
        except:
            print('Problems disconnecting from Device.')          
        return True
