# -*- coding: utf-8 -*-
"""
Created on Tue May 23 13:58:47 2017

@author: luismilczarek
"""
from observer import Listener, Subject
#from event import EventChanged

class Adapter(Listener,Subject):
    def __init__(self, Tag, obj):
        super(Adapter,self).__init__()
        self._tag = Tag
        self._obj = obj
        
        
    
    @property        
    def value(self):
        return self.fromTag()
    
    @value.setter    
    def value(self, newValue):
        self._tag.value = self.toTag(newValue)
    
    def fromTag(self):
        pass
    
    def toTag(self):
        pass
    
    def process_event(self,event=None):
        event._subject = self
        self._obj.process_event(event)
        
    

class linearAdapter(Adapter):
    
    def __init__(self, Tag, obj,**Args):
        super(linearAdapter,self).__init__(Tag, obj)
        
        self._rangeObjMin = Args["rangeObjMin"]
        self._rangeTagMin = Args["rangeTagMin"]
        self._rangeObjMax = Args["rangeObjMax"]
        self._rangeTagMax = Args["rangeTagMax"]
        
        self._coef1 = (self._rangeObjMax -self._rangeObjMin)/(self._rangeTagMax - float(self._rangeTagMin))
        self._coef2 = (self._rangeTagMax - self._rangeTagMin)/(self._rangeObjMax - self._rangeObjMin)
        
    
    def fromTag(self):
        return float(self._tag.value) * (self._rangeObjMax -self._rangeObjMin)/(self._rangeTagMax - self._rangeTagMin)
        
    def toTag(self,newValue):
        return float(newValue ) * (self._rangeTagMax - self._rangeTagMin)/(self._rangeObjMax - self._rangeObjMin)
        
    
        