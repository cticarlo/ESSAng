# -*- coding: utf-8 -*-
"""
Created on Wed Jun 28 16:46:49 2017

@author: luismilczarek
"""

class Data(object):
    
    def __init__(self,fileName):
        self._file = "{}.csv".format(fileName)
        self._data =[]
        self._index = {}
    
    def update(self):
        file = open(self._file,'r')
        self._data = file.read().split('\n')
        types = []
        for x in range(len(self._data)):
            self._data[x]= self._data[x].split(',')
        size = range(len(self._data[0]))
        
        for x in size:
            try:
                self._data[1][x]=int(self._data[1][x])
                
            except ValueError:
                try:
                    self._data[1][x]=float(self._data[1][x])
                except ValueError:
                    pass
        
        for x in size:
            self._index[self._data[0][x]] = x
            types.append(type(self._data[1][x]))
            
        self._data.pop(0)
            
        for x in range(len(self._data)):
            for i in size:
                self._data[x][i]= types[i](self._data[x][i])
        
    def searchByIndex(self,index, value, target=None):
        for x in self._data:
            if x[self._index[index]] == value:
                if target == None:
                    return x
                else:
                    return x[self._index[target]]
        raise ValueError("Was impossible to find the value for this index")