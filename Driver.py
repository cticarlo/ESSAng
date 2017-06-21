# -*- coding: utf-8 -*-
"""
Created on Fri Nov 25 13:29:10 2016

@author: luismilczarek
"""
import thread as th
from time import sleep
from observer import *
import minimalmodbus as mb
from pyfirmata import Arduino, util
import paho.mqtt.client as ph
from event import *



class Driver(object):
  
    def __init__(self, port, baud, delay, scan, flag, **Args):
        self._port= port
        self._baud= baud
#        self._addres= addres
        self._Tags= []
        self._scan= scan
        self._delay= delay/1000
        self._args= Args
        self._flag = flag
        self._controler= self.chooseComm()
        
    def attach(self, *Tags):
        
        for tag in Tags:
            if not tag in self._Tags:
                self._Tags.append(tag)
                
    
    def update(self):
#        print 'hello 2'
        while self._scan:
#            print "Loop"
            
            for x in self._Tags:
                if x._timeLastUpdate >= x._scanTime:
                    if x._value != self._controler.readValue(x):
                        x._value = self._controler.readValue(x)
                        x.notify(EventChanged(x))
                        x._timeLastUpdate = 0
#                        print 'ola evento'
                    if x._changeValue==True:
                        self._controler.writeValue(x)
                        
                else:
                    x._timeLastUpdate += self._delay
            sleep(self._delay)
            
    def startScan(self, delay):
               
        self._scan= False
        sleep(self._delay+0.5)
        self._delay= delay
        self._scan= True
        sleep(3)
        th.start_new_thread(self.update, ())
        
    def stopScan(self):
        u"""
        Metodo que finaliza o ciclo de varredura.
        """
        self._scan=False
        
    def chooseComm(self):
        
       if(self._flag=='m'or self._flag=='M'):
           return ModBusComm(self._port, self._baud, self._args)
       
       elif(self._flag=='f' or self._flag=='F'):
           return FirmataComm(self._port, self._baud, self._args)
       elif(self._flag=='p' or self._flag=='P'):
           return MqttComm(self._port,self._baud,self._args)

           
           
class ModBusComm(object):
    
    def __init__(self, port , baud, Args):
#        print "Teste"
#        print Args["Slave"]
        self._instrument = mb.Instrument(port,Args["Slave"])
        self._instrument.serial.baudrate= baud
        
    def writeValue(self, Tag, newValue):
        self._instrument.write_register(Tag._regnum, Tag._newValue)
        
    def readValue(self,Tag):
        return self._instrument.read_register(Tag._regnum, Tag._decimal)
        


class FirmataComm(object):
   
    def __init__(self, port, baud=9600, **Args):
        self._board= Arduino(port, baudrate=baud)
        self._it = util.Iterator(self._board)
        self._it.start()
        
    
    def writeValue(self, Tag, newValue):
        if(Tag._analog):
            self._board.analog[Tag._regnum].write(Tag._newValue)
        else:
            self._board.digital[Tag._regnum].write(Tag._newValue)
    
    def readValue(self, Tag):
        if(Tag._analog):
            return self._board.analog[Tag._regnum].read(Tag._newValue)
        else:
            return self._board.digital[Tag._regnum].read(Tag._newValue)
    

class MqttComm(object):
    
    def __init__(self,ip,port,Args):
        self._topics = {}
        self._ip= ip
        self._port =port
        self._Client = ph.Client()
        self._Client.on_connect= self.On_connect
        self._Client.on_message= self.On_message
        self._Client.connect(ip,port)
        self._Client.loop_start()
    
    def On_connect(self, mqttc, obj, flags, rc):
        mqttc.subscribe(topic='ESSA/#', qos=0)
        print type(self)

    
    
    def On_message(self,mqttc, userData, msg):
#        print topics
#        print msg.payload
        self._topics[msg.topic]= msg.payload
#        print type(msg.payload)
        
    def writeValue(self,Tag):
        self._Client.publish(Tag._regnum,Tag._newValue)
        
    def readValue(self,Tag):
        try:
            return Tag._type(self._topics[Tag._regnum])
        except KeyError:
#            self._Client.subscribe(Tag._regnum)
            return -1
        
    
    def __del__(self):
        self._Client.loop_stop()
        
        
    
        