# -*- coding: utf-8 -*-
"""
Created on Sun Sep 04 14:09:47 2016

@author: luismilczarek
"""
#import thread as th
#from time import sleep
#import minimalmodbusmaster.minimalmodbus as mb
#mb.CLOSE_PORT_AFTER_EACH_CALL = True
from observer import *

        
class Tag(Subject):
    u"""
    Classe Tag - classe destinada ao armazenamento de informações.
    ---------------------------------------------------------------------------
    Esta classe armazena os dados necessarios para a comunicação com o 
    dispositivo controlador. Como parametros devem ser passados: O 
    identificador do endereço de origem/destino, o valor inicial da tag,
    intervalo de tempo entre atualizações da tag (default 0), se é um valor
    analogico (default true), casas decimais (default 0), é o tipo de variavel 
    (default int) geralmente usado quando o dado recebido esta em formato de 
    string (ex. Mqtt).
    """

    
    def __init__(self,reg_num,initValue,scanTime=0,analog=True,decimalNum=0,vartype=int):
        
        super(Tag,self).__init__()
#        self._values={"valor1":None,"valor2":None,"valor3":None}
        
#        mb.CLOSE_PORT_AFTER_EACH_CALL = True
        self._value=initValue
#        self._controler=controler
#        self._scan=scan       
#        self._delay = delay
        self._regnum= reg_num
        self._decimal=decimalNum
#        self._port=port
#        self._addres=addres
#        self._instrument=mb.Instrument(port,addres)
        
#        self._instrument=mb.Instrument()
#        self._baud=baud
        self._changeValue=False
        self._newValue=0
        self._scanTime=scanTime / 1000.0
        self._timeLastUpdate=0
        self._analog = analog
        self._type=vartype 
    
    @property
    def value(self):
        return self._value
    
    
    @value.setter
    def value(self,value):
        u"""
        Método writeValue - Método que prepara a tag para a escrita de um novo
        valor.
        """
        self._newValue=value
        self._changeValue=True

    @property
    def scanTime(self):
        return self.scanTime*1000
        
    @scanTime.setter
    def scanTime(self,newTime):
        self._scanTime= newTime/1000
        
        





#class Tag(Subject):
#    u"""
#    Objeto destinado a capturar dados do controlador, e notificar seus Listeners.
#   
#    
#    """
#    
#    def __init__(self,port,baud,addres,reg_num,delay=1,scan=True):
#        
#        super(Tag,self).__init__()
##        self._values={"valor1":None,"valor2":None,"valor3":None}
#        
##        mb.CLOSE_PORT_AFTER_EACH_CALL = True
#        self._value=0
##        self._controler=controler
#        self._scan=scan       
#        self._delay = delay
#        self._regnum= reg_num
#        self._port=port
#        self._addres=addres
##        self._instrument=mb.Instrument(port,addres)
#        
##        self._instrument=mb.Instrument()
#        self._baud=baud
#        self._changeValue=False
#        self._newValue=0
##        self._instrument.serial.baudrate=baud
##        self._time=0
#        
#        
#
#   
##    def update(self,delay):
##        while True:
##            if self._values["valor1"] != self._plc.var[0] or self._values["valor2"] != self._plc.var[1] or self._values["valor3"] != self._plc.var[2]:
##                self._values["valor1"] = self._plc.var[0]
##                self._values["valor2"] = self._plc.var[1]
##                self._values["valor3"] = self._plc.var[2]
##                self.notify(EventChanged(self))
##            sleep(delay)
#            
#    def update(self):
#        u"""
#        Metodo que realiza o scaneamneto das vairiaveis, sendo interrompido somente quando o metodo stopScan e
#        startScan, tem como argumentos de entrada os nomes das variaveis.
#        """
#        instrument=mb.Instrument(self._port,self._addres)
#        instrument.serial.baudrate=self._baud
#       
#        while self._scan:
#            if self._value != instrument.read_register(self._regnum):
#                self._value = instrument.read_register(self._regnum)
#                print self._value
#                self.notify(EventChanged(self))
#                sleep(self._delay)
#                print 'ola'
#            if self._changeValue==True:
#                instrument.write_register(self._regnum+1,self._newValue)
#                self._changeValue=False
#                print 'oi'
#   
#    def startScan(self,delay):
#        u"""
#        Metodo que inicializa a varredura pelas variaveis do controlador,
#        como argumentos de entrada devem ser passados o intervalo entre as varreduras em segundos
#        e os nomes das variaveis.
#        """
#        
#        self._scan=False
#        sleep(self._delay+0.5)
#        self._delay=delay
#        self._scan=True
#        th.start_new_thread(self.update,())
#        
#    def stopScan(self):
#        u"""
#        Metodo que finaliza o ciclo de varredura.
#        """
#        self._scan=False
#    
#    def writeValue(self,value):
#        self._newValue=value
#        self._changeValue=True
#        

        

