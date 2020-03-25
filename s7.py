#!/usr/bin/env python
# -*- coding:utf-8 -*- 

import struct
import snap7
import sys

tag_type = {
"V":1,
"M":0
}

size_type = {
"B":1,
"W":2,
"D":4
}


class S7Client(object):
    
    
    def __init__(self):
        self.client = None

    def plc_connect(self, ip, type, rack=0, slot=1):
        self.client = snap7.client.Client()
        self.client.set_connection_type(type)
        self.client.connect(ip, rack, slot)

    def plc_con_close(self):
        self.client.disconnect()

    def read_VB(self, offset):
        vb_data = self.client.db_read(1, offset, 1)
        return vb_data[0]

    def write_VB(self, offset, data):
        data = int(data)
        temp = hex(int(data))[2:]
        if data < 0 or data > 255:
            print("0-255")
        else:
            if data < 16:
                temp = "0"+ temp
            self.client.db_write(1, offset, bytes.fromhex(temp))
            print("write to V "+str(offset)+"with "+str(data)+"successful")
    
    def _changetag2offsetandtype(self, tag="",ty= ""):
        ''''
        # tag 地址表示值：例如V1100.2、VW1000、VD1074等
        '''
        try:
            bit = 0
            if not tag:
                raise KeyError
            
            tag = tag.strip().upper()
            if tag[0] in tag_type:
                db = tag_type[tag[0]]
            else:
                raise KeyError
            
            if ord(tag[1]) < ord('A'):
                size = 1
                if '.' in tag:
                    ty = "bool"
                    addr = int(tag[1:tag.index(".")])
                    bit = int(tag[tag.index(".")+1:])
                    
                else:
                    ty = "byte"
                    addr = int(tag[1:])
            else:
                size = size_type[tag[1]]
                addr = int(tag[2:])
        except KeyError as e:
            print "Please check address!!!",str(e)
            sys.exit(-1)
        
        return [db, addr, size , ty , bit]
        
    def read_DB(self,db, addr, size ,ty ,bit):
        db_data = self.client.db_read(db, addr, size)
        
        if ty == "float":
            value = struct.unpack('!f', db_data)[0]
        elif ty == "short":
            value = struct.unpack('!h', db_data)[0]
        elif ty == "int":
            value = struct.unpack('!i', db_data)[0]
        elif ty == "byte":
            value = db_data[0]
        elif ty == "bool":
            bvalue = db_data[0] & (1<<bit) 
            if bvalue:
                return True
            else:
                return False
        
        return value
        
        
    def write_DB(self, value, db, addr, size ,ty ,bit):
        
        if ty == "float":
            vbytes = struct.pack('!f', value)
            
        elif ty == "short":
            vbytes = struct.pack('!h', value)
        elif ty == "int":
            vbytes = struct.pack('!i', value)
        elif ty == "byte":
            
            if type(value) == str:
                vbytes = value
            else:
                vbytes = chr(value)
            
        elif ty == "bool":
            db_data = self.client.db_read(db, addr, 1)
            bvalue = db_data[0] & (1<<bit) 
            if bvalue == value:
                return
            else:
                vbytes = chr(db_data[0] ^ (1<<bit)) 
        
        db_data = self.client.db_write(db, addr, vbytes)
    
    
    def read_data(self,tag,ty=""):
        params = self._changetag2offsetandtype(tag,ty)
        return self.read_DB(*params)
    
    def write_data(self,tag,value,ty=""):
        params = self._changetag2offsetandtype(tag,ty)
        self.write_DB(value,*params)

    
    

