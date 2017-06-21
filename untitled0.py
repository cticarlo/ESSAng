# -*- coding: utf-8 -*-
"""
Created on Thu Feb 16 00:34:26 2017

@author: luismilczarek
"""

#import minimalmodbus as mb
from Driver2 import *
#from time import sleep
from objects import ConsoleLogger
from adapter import linearAdapter

#x = mb.Instrument("COM4",1)
#x.serial.baudrate=9600
#sleep(3)
from tag import Tag



tag1 = Tag(["0:Objects", "2:MyObject", "2:MyVariable"],0.0,10000)
tag2 = Tag(["0:Objects", "2:MyObject", "2:MyVariable2"],3.0,10000,vartype=float)

list1= ConsoleLogger("1:")
list2= ConsoleLogger("2:")
adapt1 = linearAdapter(tag1,list1,rangeTagMax=1023.0,rangeTagMin=0.0,rangeObjMax=5.0,rangeObjMin=0.0)
adapt2 = linearAdapter(tag2,list2,rangeTagMax=1023.0,rangeTagMin=0.0,rangeObjMax=24.0,rangeObjMin=0.0)

tag1.attach(adapt1)
tag2.attach(adapt2)

   
x = OPCDriver(True,ip="opc.tcp://localhost:4840/freeopcua/server/")
x.attach(tag1,tag2)

