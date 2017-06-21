# -*- coding: utf-8 -*-
"""
Created on Mon Apr 03 15:57:34 2017

@author: luismilczarek
"""


import _thread as th
from time import time, sleep
from observer import *

import minimalmodbus as mb
from pyfirmata import Arduino, util
import paho.mqtt.client as ph
import opcua as op

from event import *



class Driver(object):
    u"""
    Driver - Classe matriz para os diversos protocolos de comunicação.
    ---------------------------------------------------------------------------
    Esta classe deve ser utilizada por classes derivadas que possuam diferentes
    protocolos de comunicação. Suas derivadas devem implementar o metodo de 
    escrita e de leitura.
    """
  
    def __init__(self, initScan=True):
        u"""
        Método construtor da classe base Driver.
        -----------------------------------------------------------------------
        Os argumentos minimos são 
        respectivamente o intevalo de tempo minimo entre um ciclo de 
        atualização e outra em milisegundos e se deve inicializar a varredura. 
        """
        self._Tags= []
        self._scan= initScan
        if(self._scan):
            self.startScan()
        
        
        
    def attach(self, *Tags):
        u"""
        Método attach - Método de subscrição de tags.
        -----------------------------------------------------------------------
        Como parametro este metodo deve receber as tags que deveram ser 
        atualizadas pelo driver;
        """
        
        for tag in Tags:
            if not tag in self._Tags:
                self._Tags.append(tag)
                
    
    def update(self):
            u"""
            Método update - Método de varredura.
            -----------------------------------------------------------------------
            Responsavel por realizar a atualização das tags inscritas no driver.
            """
    
            while self._scan:
                
                now= time()
#                print "oi"
                for x in self._Tags:
                    if x._timeLastUpdate+x._scanTime <= now:
                        aux = self.readValue(x)
                        if x.value != aux:
                            x._value = aux
                            x.notify(EventChanged(x))
                            x._timeLastUpdate = now
                        
                    if x._changeValue==True:
                       self.writeValue(x)
                       x._changeValue=False
                       
#    def update(self):
#        u"""
#        Método update - Método de varredura.
#        -----------------------------------------------------------------------
#        Responsavel por realizar a atualização das tags inscritas no driver.
#        """
##        print 'hello 2'
#        while self._scan:
##            print "Loop"
#            
#            for x in self._Tags:
#                if x._timeLastUpdate >= x._scanTime:
#                    aux = self.readValue(x)
#                    if x._value != aux:
#                        x._value = aux
#                        x.notify(EventChanged(x))
#                        x._timeLastUpdate = 0
##                        print 'ola evento'
#                else:
#                    x._timeLastUpdate += self._delay
#                    
#                if x._changeValue==True:
#                   self.writeValue(x)
#                   x._changeValue= False
#                        
#                
#            sleep(self._delay)
            
    def startScan(self):
        u"""
        Método startScan - Método inicializador do ciclo de varredura.
        -----------------------------------------------------------------------
        Este método inicializa o ciclo de varredura logo após fechar o atual, 
        caso o mesmo esteja ativo. Como parametro opcional pode-se definer um 
        novo intervalo de varredura.
        """
               
        self._scan= False
        sleep(0.5)
        self._scan= True
        sleep(3)
        th.start_new_thread(self.update, ())
        
    def stopScan(self):
        u"""
        Metodo que finaliza o ciclo de varredura.
        """
        self._scan=False
    
    def writeValue(self):
        u"""
        Método writeValue - Método de escrita de valores.
        -----------------------------------------------------------------------
        Este método é responsavel por escrever valores nas tags. Deve ser 
        definido em classes derivadas.
        """
        pass
    
    
    def readValue(self):
        u"""
        Método readValue - Método de leitura de valores.
        -----------------------------------------------------------------------
        Este método é responsavel por ler valores das tags. Deve ser 
        definido em classes derivadas.
        """
        pass
                   
           
class ModBusDriver(Driver):
    u"""
    Classe ModBusDriver - Classe responsavel pela atualização das tags atraves do protocolo modbus.
    ---------------------------------------------------------------------------
    Esta classe é derivada de Driver.
    """
    
    def __init__(self, initScan,**Args):
        u"""
        Método construtor
        -----------------------------------------------------------------------
        Como parametros devem ser passados o intervalo de tempo entre as 
        atualizações das tags,se deve iniciar o ciclo de varredura, a porta de 
        comunicação que deve ser especificada pelo parametro 'port', a 
        identificação do slave que deve ser especificado pelo parametro 'slave'
        , e o baudrate pelo parametro 'baud'.
        """
        super(ModBusDriver,self).__init__(initScan)
        self._instrument = mb.Instrument(Args["port"],Args["slave"])
        self._instrument.serial.baudrate= Args["baud"]
        
    def writeValue(self, Tag):
        u"""
        Método writeValue - Método de escrita da classe ModBusDriver.
        -----------------------------------------------------------------------
        Este método deve receber como parametro a tag a ser atualizada.
        """
        self._instrument.write_register(Tag._regnum, Tag._newValue)
        
    def readValue(self, Tag):
        u"""
        Método readValue - Método de leitura da classe ModBusDriver.
        -----------------------------------------------------------------------
        Este método deve receber como parametro a tag a ser lida.
        """
        return self._instrument.read_register(Tag._regnum, Tag._decimal)
        
        
    def __del__(self):
        u"""
        Método desconstrutor - fecha a comunicação e destroi o objeto.
        """
        self._instrument.serial.close()
        
        


class FirmataDriver(Driver):
     u"""
    Classe FirmataDriver - Classe responsavel pela atualização das tags atraves do protocolo firmata.
    ---------------------------------------------------------------------------
    Esta classe é derivada de Driver.
    """
   
     def __init__(self, initScan, **Args):
         u"""
         Método construtor
         -----------------------------------------------------------------------
         Como parametros devem ser passados o intervalo de tempo entre as 
         atualizações das tags,se deve iniciar o ciclo de varredura, a porta de 
         comunicação que deve ser especificada pelo parametro 'port'
         e o baudrate pelo parametro 'baud'.
         """
         super(FirmataDriver,self).__init__(scantTime,initScan)
         self._board= Arduino(Args["port"], baudrate=Args["baud"])
         self._it = util.Iterator(self._board)
         self._it.start()
        
    
     def writeValue(self, Tag):
         u"""
         Método writeValue - Método de escrita da classe FirmataDriver.
         -----------------------------------------------------------------------
         Este método deve receber como parametro a tag a ser atualizada.
         """
         if(Tag._analog):
             self._board.analog[Tag._regnum].write(Tag._newValue)
         else:
             self._board.digital[Tag._regnum].write(Tag._newValue)
    
     def readValue(self, Tag):
         u"""
         Método readValue - Método de leitura da classe FirmataDriver.
         -----------------------------------------------------------------------
         Este método deve receber como parametro a tag a ser lida.
         """
         if(Tag._analog):
             return self._board.analog[Tag._regnum].read(Tag._newValue)
         else:
             return self._board.digital[Tag._regnum].read(Tag._newValue)
    

class MqttDriver(Driver):
    
    u"""
    Classe MqttDriver - Classe responsavel pela atualização das tags atraves do protocolo Mqtt.
    ---------------------------------------------------------------------------
    Esta classe é derivada de Driver.
    """
    
    def __init__(self, initScan, **Args):
         u"""
         Método construtor
         -----------------------------------------------------------------------
         Como parametros devem ser passados o intervalo de tempo entre as 
         atualizações das tags,se deve iniciar o ciclo de varredura, o ip do 
         broker que deve ser especificada pelo parametro 'ip' e a porta
         pelo parametro 'port'.
         """
         super(MqttDriver, self).__init__( initScan)
         self._topics = {}
         self._Client = ph.Client()
         self._Client.on_connect= self.On_connect
         self._Client.on_message= self.On_message
         self._Client.connect(Args["ip"],Args["port"])
         self._Client.loop_start()
    
    
    def On_connect(self, mqttc, obj, flags, rc):
        u"""
        Método acionado no momento da conexão com o broker, que realiza a 
        subinscrição em todos os subtópicos de 'ESSA'. Não realizar chamada manualmente.
        
        """
        mqttc.subscribe(topic='ESSA/#', qos=0)
#        print type(self)

    
    
    def On_message(self,mqttc, userData, msg):
        u"""
        Método acionado quando há o recebimento da atualização de um tópico. Não realizar chamada manualmente.
        """
#        print topics
#        print msg.payload
        self._topics[msg.topic]= msg.payload
#        print type(msg.payload)
        
    def writeValue(self,Tag):
        u"""
        Método writeValue - Método de escrita da classe MqttDriver.
        -----------------------------------------------------------------------
        Este método deve receber como parametro a tag a ser atualizada.
        """
        self._Client.publish(Tag._regnum, Tag._newValue)
        
   
    def readValue(self, Tag):
        u"""
        Método readValue - Método de leitura da classe MqttDriver.
        -----------------------------------------------------------------------
        Este método deve receber como parametro a tag a ser lida.
        """
        try:
            return Tag._type(self._topics[Tag._regnum])
        except KeyError:
#            self._Client.subscribe(Tag._regnum)
            return -1
        
    
    def __del__(self):
        self._Client.loop_stop()
        
        
        
        
class OPCDriver(Driver):
    
    def __init__(self,initScan, **Args):
        
        super(OPCDriver, self).__init__(initScan)
        self._client= op.Client(Args["ip"])
        self._client.connect()
        self._root = self._client.get_root_node()
        
    def writeValue(self, Tag):
        self._root.get_child(Tag._regnum).set_value(Tag._newValue)
    
    def readValue(self, Tag):
        return self._root.get_child(Tag._regnum).get_value()
        