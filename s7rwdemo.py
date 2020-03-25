#!/usr/bin/env python
# -*- coding:utf-8 -*- 

import time
from s7 import *

client = S7Client()
client.plc_connect('192.168.1.3', 2)
print("connected")


# 读取和设置当前模式 
# Handle：False
# Auto ：True
data = client.read_data("V1100.3")
print(data)


# client.write_data("V1100.3",False)

time.sleep(0.2)
data = client.read_data("V1100.3")
print(data)


#P/I/D
P = client.read_data("VD12", "float")
I = client.read_data("VD20", "float")
D = client.read_data("VD24", "float")

print P,I,D

# 阀位手动输出值HandOutput
# 阀位自动输出值AutoOutput
# 液位设定值 SP
HandOutput = client.read_data("VD1040", "float")
AutoOutput = client.read_data("VD1058", "float")
SP = client.read_data("VD1030", "float")

print HandOutput,AutoOutput,SP



# change and read PV（液位）值
while True:
    for x in range(1,27648,576):
        client.write_data("VW1000",x,ty="short")
        
        time.sleep(0.5)
        
        data = client.read_data("VW1000",ty="short")
        print(data)
        
    
    client.write_data("VW1000",27648,ty="short")
    
    for x in range(27648,1,-576):
        client.write_data("VW1000",x,ty="short")
        
        time.sleep(0.5)
        
        data = client.read_data("VW1000",ty="short")
        print(data)

time.sleep(2)



## change and read Steam Flow（蒸汽流量）值 
# for x in range(0,21,2):
    # client.write_data("VD1070",x,ty="float")
    
    # time.sleep(1)
     
    # data = client.read_data("VD1070",ty="float")
    # print(data)

# time.sleep(2)


# change and read Feed Flow（供液流量）值
# for x in range(0,11,1):
    # client.write_data("VD1074",x,ty="float")
    
    # time.sleep(1)
     
    # data = client.read_data("VD1074",ty="float")
    # print(data)

# time.sleep(2)



time.sleep(2)
client.plc_con_close()

