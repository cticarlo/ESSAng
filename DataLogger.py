# -*- coding: utf-8 -*-
"""
Created on Thu Jul  6 13:54:57 2017

@author: luismilczarek
"""
from observer import Listener

class DataLogger(Listener):
    
    def __init__(self,fileName,*tags):
        super(DataLogger,self).__init__()
        self._filename = fileName
        self._tags= tags
        self._isOpen = False
        
                
    def process_event(self,event=None):
        if not event.subject in self._tags:
            raise ValueError("The tag {} is not listed on the data logger".format(event.subject))
        else:
            while(self._isOpen):
                pass
            self._isOpen = True
            file = open(self._filename,'a')
            for tag in range(len(self._tags)-1):
                file.write("{},".format(self._tags[tag].value))
            file.write("{}\n".format(self._tags[-1].value))
            file.close()
            self._isOpen = False
            
    def read(self):
        while(self._isOpen):
            pass
        self._isOpen = True
        file = open(self._filename)
        data = file.read()
        file.close()
        self._isOpen = False
        data = data.splitlines()

        aux = []
        for linha in data:
            auxl=[]
            x = linha.split(',')
            for dado in x:
                auxl.append(self.getTypedValue(dado))
            aux.append(auxl)
        del data
        return aux


        #size = range(len(data))
        #for x in size:
        #    data[x] = data[x].split(',')
            
            
        #types = []
        #columms = range(len(data[0]))
        #for x in data[0]:
        #    types.append(self.getType(x))
            
            
#        global teste
#        teste = data
#        
        #dados = np.zeros((size,len(data[0])))
        #n = 0
        #for linha in data:
        #    dados[n,:]=linha[:]
        #    n=n+1
        
#        aux = []*len(data)
#        for x in columms:
#            for y in data:
#                aux[x].append(types[x](y[x]))                
#        return aux
            
            
    def getTypedValue(self,value):
        try:            
            return int(value)
        except ValueError:
            try:                
                return float(value)
            except ValueError:
                pass
        return str(value)
            