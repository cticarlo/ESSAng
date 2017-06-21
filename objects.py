# -*- coding: utf-8 -*-
"""
Created on Sat Nov 12 23:56:44 2016

@author: luismilczarek
"""

from observer import Listener
from event import *
from time import sleep
import _thread as th
from PyQt5.QtCore import pyqtSlot
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FC

class GraphUpdater(Listener):
    def __init__(self,graph,canvas,updatetime,update=True):
        super(GraphUpdater,self).__init__()
        
        self._x=[0]
        self._y=[0]
        self._tagvalue=0
        self._delay=updatetime
        self._scan=update
        
        self._canvas=canvas        
        self._graph=graph
        
        th.start_new_thread(self.graphLoop,())
        print("fiz o init do grafico")
    def process_event(self, event=None):
        
        self._tagvalue= event._subject._value
        print( "Evento recebido")
        
    def plotPoints(self):
        
        
        self._graph.clear()
        graph=self._graph.add_subplot(111)
        graph.plot(self._x,self._y)
        self._canvas.draw()
        
    def graphLoop(self):
        print( 'Vou entrar no while')
        self._scan=True
        while self._scan:
            
            self._x+=[self._delay+self._x[-1]]
            self._y+=[self._tagvalue]
            self.plotPoints()
            sleep(self._delay)
        
    def startScan(self,delay):
        
        self._scan=False
        sleep(self._delay+0.5)
        self._delay=delay
#        self._scan=True
        th.start_new_thread(self.graphLoop,())




class labelUpdater(Listener):
    def __init__(self,Label):
        super(labelUpdater,self).__init__()
        self._Label=Label
        
    def process_event(self,event=None):
        self._Label.setText(str(event._subject._value))
        


class kWHUpdater(Listener):
   
    def __init__(self,Label,scan,volt,delay,CostLabel,CostValue):
         self._x=[]
         self._time=0
         self._valueNow=0     
         self._Label=Label
         self._scan=scan
         self._volt=volt
         self._delay=delay
         self._costlabel=CostLabel
         self._costvalue= CostValue
         
         th.start_new_thread(self.kWHLoop,())
 
    def process_event(self,event=None):
         self._valueNow= event._subject._value
        
    
    def kWHLoop(self):
        while self._scan:
            self._x+=[self._valueNow]
            self._time+=self._delay
            aux=0.0
            for x in self._x:
               aux+=x
            aux =aux/len(self._x)*self._volt/3600000*self._time
#            self._Label.setText("%.2f"%(aux/len(self._x)*self._volt/3600000*self._time))
            self._Label.setText("%.2f"%aux)
            self._costlabel.setText("R$ %.2f"%(aux*self._costvalue.value()))
            sleep(self._delay)
            
    def startScan(self,delay):
        
        self._scan=False
        sleep(self._delay+0.5)
        self._delay=delay
        self._scan=True
        th.start_new_thread(self.kWHLoop,())
        
class kWHChanger(Listener):
    def __init__(self,scan,volt,delay,textMax,button,Tag,initValue):
        self._scan=scan
        self._volt=volt
        self._delay=delay
        self._textMax=textMax
        self._tag=Tag
        self._button=button
        button.clicked.connect(self.setValue)
        self._Max=initValue
        self._value=0
        self._time=0
        self._valueNow=0
        self._x=[0]
        self.setValue()
     
    @pyqtSlot()
    def setValue(self):
        print( self._textMax.value())
        self._Max= self._textMax.value()
    
    def process_event(self,event=None):
         self._valueNow= event._subject._value
         
    def kWHLoop(self):
        while self._scan:
            self._x+=[self._valueNow]
            self._time+=self._delay
            aux=0.0
            for x in self._x:
               aux+=x
            
            self._value=aux/len(self._x)*self._volt/3600000*self._time
            print (self._value)
            if self._value >= self._Max:
                print( self._Max)
                self._tag.writeValue(0)
            sleep(self._delay)
         
    def startScan(self,delay):
        
        self._scan=False
        sleep(self._delay+0.5)
        self._delay=delay
        self._scan=True
        th.start_new_thread(self.kWHLoop,())
        
    def stop(self):
        
        self._scan = False
    
        
class OnOffButton(object):
    
    def __init__(self,button,Tag):
        self._button=button
        self._button.setText('Desligado')
        self._state=False
        self._tag=Tag
        self._button.setStyleSheet('QPushButton {background-color: blue }')
        button.clicked.connect(self.writeValue)
    
    @pyqtSlot()
    def writeValue(self):
        self._state= not self._state
        self._tag.writeValue(int(self._state))
#        print self._state
        if self._state:
            self._button.setText("Ligado")
            self._button.setStyleSheet('QPushButton {background-color: red}')
        else:
            self._button.setText("Desligado")
            self._button.setStyleSheet('QPushButton {background-color: blue }')
            
            
class LuxUpdater(Listener):
   
   def __init__(self,Tag,Label,Value):
        self._tag=Tag
        self._value=Value
        self._label=Label
        self._luxValue=0
#        self._valueNow
        
   def process_event(self,event=None):
#        print event._subject.value
        aux = event._subject._value 
        self._luxValue = self.voltToLux(aux)
        if self._luxValue > self._value:
            self._tag.writeValue(0)
#        print self._luxValue*1000000000000
        self._label.setText(self._luxValue)
        
   def voltToLux(self,volt):
        
        if volt > 4.0:
            return (3.194375 * volt / 0.7600625)* 100
        elif volt > 3.0:
            return (3.194375 * volt / 0.9600625)* 100
        else:
            return (3.194375 * volt / 35.2600625)* 100
            

class ConsoleLogger(Listener):
    def __init__(self,identifier):
        self._identifier = identifier
        
    def process_event(self,event=None):
        print( self._identifier ,event._subject.value)
          