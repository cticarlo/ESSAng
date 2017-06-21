# -*- coding: utf-8 -*-
"""
attribute.py - Classes que representam dados e metodos auxiliares
--------------------------------------------------------------------------------
Contem as classes Attribute, Attributes, AttributeList, Identity
"""

from event import Subject, Listener, EventChanged, EventUpdated
from exception import KastError, KastListError

__author__  = "Carlos R. Rocha"
__email__   = "cticarlo@gmail.com"
__version__ = "20110411-1200"
__status__ = "stable"
__license__ = "GPL"

#-------------------------------------------------------------------------------

class Attribute(Subject):
    """
    Attribute - Armazena dado observavel - preferencialmente numerico
    Descende de Subject para ser data-aware
    """
    changed = EventChanged()
    
    def __init__(self, value=0.0, readonly=False):
        """
        Inicializador - Define um valor inicial para o atributo e se ele eh
        somente leitura. O valor default eh 0.0. O atributo eh rw por default
        """
        self._v = value
        self._ro = readonly
        Subject.__init__(self)

    def __repr__(self):
        return self._v.__repr__()

    @property
    def value(self):
        """
        Retorna o valor armazenado no attribute
        """
        return self._v
        
    @value.setter
    def value(self, value=0.0):
        """
        Modifica o valor armazenado no attribute
        se este nao for somente leitura
        """
        if (self._ro):
            raise KastError(u"Atributo é somente leitura.")
        else:
            self._v = value
            self.notify(Attribute.changed)

    @property
    def readonly(self):
        """
        Retorna o verdadeiro se o attribute for somente leitura
        """
        return self._ro
        
    @readonly.setter
    def readonly(self, status):
        """
        Define se o attribute eh somente leitura (True) ou não
        """
        self._ro = status

    # Metodos para compatibilidade com tipos numericos
    def __float__(self):
        return float(self._v)

    def __int__(self):
        return int(self._v)
        
    def __long__(self):
        return long(self._v)
        
    def __index__(self):
        return int(self._v)

    def __add__(self, other):
        return self._v + other
        
    def __sub__(self, other):
        return self._v - other

    def __mul__(self, other):
        return self._v * other

    def __div__(self, other):
        return self._v / other

    def __neg__(self):
        return -self._v

    def __radd__(self, other):
        return self._v + other
        
    def __rsub__(self, other):
        return self._v - other

    def __rmul__(self, other):
        return self._v * other

    def __rdiv__(self, other):
        return self._v / other

#-------------------------------------------------------------------------------

class Attributes(Subject):
    """
    Attributes - Armazena dados em um dicionario observavel
    Descende de Subject para ser data-aware
    """
    changed = EventChanged()
    
    def __init__(self, readonly=False, **values):
        """
        Inicializador - Define um valor inicial para o dicionario e se ele eh
        somente leitura. O valor default eh um dicionario vazio.
        O atributo eh rw por default
        """
        self._v = {} if values is None else values
        self._ro = readonly
        Subject.__init__(self)

    def __repr__(self):
        return self._v.__repr__()
        
    @property
    def readonly(self):
        """
        Retorna o verdadeiro se o attribute for somente leitura
        """
        return self._ro
        
    @readonly.setter
    def readonly(self, status):
        """
        Define se o attribute eh somente leitura (True) ou não
        """
        self._ro = status

    def __getitem__(self, key):
        """
        Retorna o valor do elemento key do dicionario se existir
        """
        try:
            return self._v[key]
        except:
            raise KastError (u"{0} não é um atributo da lista".format(key))
        
    def __setitem__(self, key, value=0.0):
        """
        Modifica o valor armazenado no elemento key do dicionario
        Se nao existir, o adiciona, se a instancia nao for somente leitura
        """
        if (self._ro):
            raise KastError(u"Lista de atributos é somente leitura.")
        else:
            self._v[key] = value
            self.notify(Attributes.changed)

    def __delitem__(self, key):
        """
        Remove o elemento key do dicionario
        se a instancia nao for somente leitura
        """
        if (self._ro):
            raise KastError(u"Lista de atributos é somente leitura.")
        else:
            try:
                del self._v[key]
                self.notify(Attributes.changed)
            except:
                raise KastError (u"{0} não é um atributo da lista".format(key))

    def __contains__(self, key):
        """
        Verifica se a atributo key esta na lista
        """
        return key in self._v

    def __len__(self):
        """
        Retorna o tamanho da lista de atributos
        """
        return len(self._v)
        
    def setdefault(self, key, value=0.0):
        """
        Define o valor default de um atributo, se ele nao existir no dicionario
        """
        if key not in self._v:
            self._v[key] = value
            self.notify(Attributes.changed)
        return self._v[key]

    def __iter__(self):
        """
        Necessario para definir a classe como generator
        """
        return self._v.iteritems()

#-------------------------------------------------------------------------------

class AttributeList(Listener, Subject):
    """
    AttributeList - Armazena instancias de Attribute em um dicionario
    Descende de Subject para ser data-aware
    """
    changed = EventChanged()
    
    def __init__(self, readonly=False, **values):
        """
        Inicializador - Define um valor inicial para o dicionario e se ele eh
        somente leitura. O valor default eh um dicionario vazio.
        O atributo eh rw por default
        """
        self._v = {}
        if values is not None:
            for k, v in values.iteritems():
                self._v[k] = Attribute(v)
                self._v[k].attach(self)
        self._ro = readonly
        Subject.__init__(self)
        Listener.__init__(self)

    def processEvent(self, event=None, subject=None):
        """
        Implementar esse metodo para resolver o processamento de notificacoes
        de eventos. Ele recebe o evento que disparou o processamento e pode
        receber opcionalmente o subject que foi usado
        """
        self.notify(AttributeList.changed)

    @property
    def readonly(self):
        """
        Retorna o verdadeiro se o attribute for somente leitura
        """
        return self._ro
        
    @readonly.setter
    def readonly(self, status):
        """
        Define se o attribute eh somente leitura (True) ou não
        """
        self._ro = status

    def __repr__(self):
        return self._v.__repr__()

    def __getitem__(self, key):
        """
        Retorna o valor do elemento key do dicionario se existir
        """
        try:
            return self._v[key].value
        except:
            raise KastError (u"{0} não é um atributo da lista".format(key))
        
    def __setitem__(self, key, value=0.0):
        """
        Modifica o valor armazenado no elemento key do dicionario
        Se nao existir, o adiciona, se a instancia nao for somente leitura
        """
        if (self._ro):
            raise KastError(u"Lista de atributos é somente leitura.")
        else:
            if key in self._v:
                self._v[key].value = value
            else:
                self._v[key] = Attribute(value)
                self._v[key].attach(self)
                self.notify(AttributeList.changed)

    def __delitem__(self, key):
        """
        Remove o elemento key do dicionario
        se a instancia nao for somente leitura
        """
        if (self._ro):
            raise KastError(u"Lista de atributos é somente leitura.")
        else:
            try:
                self._v[key].detach(self)
                del self._v[key]
                self.notify(AttributeList.changed)
            except:
                raise KastError (u"{0} não é um atributo da lista".format(key))

    def __contains__(self, key):
        """
        Verifica se a atributo key esta na lista
        """
        return key in self._v

    def __len__(self):
        """
        Retorna o tamanho da lista de atributos
        """
        return len(self._v)
        
    def setdefault(self, key, value=0.0):
        """
        Define o valor default de um atributo, se ele nao existir no dicionario
        """
        if key not in self._v:
            self._v[key] = Attribute(value)
            self._v[key].attach(self)
            self.notify(AttributeList.changed)
        return self._v[key].value

    def __iter__(self):
        """
        Necessario para definir a classe como generator
        """
        return self._v.iteritems()

    def createView(self, *names):
        """
        Retorna uma visao que nada mais eh que uma instancia de AttributeList
        onde os atributos originais sao referenciados com nomes diferentes
        passados em tuplas (original, novo). Se a lista de nomes nao for
        fornecida, faz-se uma copia completa do dicionario.
        Do contrario, copiam-se apenas os atributos com nome original presente
        na lista
        """
        list=[]
        try:
            view = AttributeList()
            if len(names) == 0:
                for k, v in self._v.iteritems():
                    view._v[k]=v
                    view._v[k].attach(view)                
            else:
                if isinstance(names[0], (tuple, list)):
                    for o, n in names:
                        try:
                            view._v[n] = self._v[o]
                            view._v[n].attach(view)
                        except:
                            list.append(o)
                else:
                    for o in names:
                        try:
                            view._v[o] = self._v[o]
                            view._v[o].attach(view)
                        except:
                            list.append(o)
        finally:
            if len(list) > 0:
                raise KastListError(u"Atributos inexistentes", list)
            else:
                return view

#-------------------------------------------------------------------------------

class Identity(Subject):
    """
    Identity - Define uma identidade para um objeto
    Descende de Subject para ser data-aware
    
    Os atributos essenciais de uma instancia de Identity sao:
      - id          : inteiro unico para referenciar a entidade
      - name        : nome da entidade
      - description : descricao mais detalhada da entidade
    """
    changed = EventChanged()
    obrigatorios = ('id', 'name', 'description')
    
    def __init__(self, id = None, name = None, description = None, 
                 readonly=False, **other):
        """
        Inicializador - Define os atributos da identidade e se eles sao
            somente leitura. O valor default eh um dicionario vazio.
        A instancia aceita modificacoes por default
        id - inteiro que referencia a entidade. Default eh None
        name - nome da entidade. Default eh None
        description - descricao detalhada da entidade. Default eh None
        readonly - define se a identidade eh somente leitura. Default eh False
        other - dicionario de outros identificadores opcionais
        """
        self._id = dict(id=id, name=name, description=description, **other)
        self._ro = readonly
        Subject.__init__(self)

    @property
    def readonly(self):
        """
        Retorna verdadeiro se a instancia for somente leitura
        """
        return self._ro
        
    @readonly.setter
    def readonly(self, status):
        """
        Define se a instancia eh somente leitura (True)
        """
        self._ro = status

    def __repr__(self):
        """
        Retorna atributo name da identidade
        """
        return self._id['name']

    def __getitem__(self, key):
        """
        Retorna o valor do elemento key do dicionario se existir
        """
        try:
            return self._id[key]
        except:
            raise KastError (u"{0} não é identificador".format(key))

    def __setitem__(self, key, value=0.0):
        """
        Modifica o valor armazenado no elemento key do dicionario
        Se nao existir, o adiciona, se a instancia nao for somente leitura
        """
        if (self._ro):
            raise KastError(u"Identidade é somente leitura.")
        else:
            self._id[key] = value
            self.notify(Identity.changed)

    def __delitem__(self, key):
        """
        Remove o elemento key do dicionario
        se a instancia nao for somente leitura ou key nao for obrigatorio
        """
        if self._ro:
            raise KastError(u"Identidade é somente leitura.")
        elif key in Identity.obrigatorios:
            raise KastError(u"Atributo obrigatório.")
        else:
            try:
                del self._id[key]
                self.notify(Identity.changed)
            except:
                raise KastError(u"{0} não é identificador".format(key))

    def __contains__(self, key):
        """
        Verifica se a chave key esta contida no dicionario
        """
        return key in self._id

    def __len__(self):
        """
        Retorna o tamanho do dicionario
        """
        return len(self._id)
        
    def setdefault(self, key, value=None):
        """
        Define o valor default de um atributo, se ele nao existir no dicionario
        """
        if key not in self._id:
            self._id[key] = value
            self.notify(Identity.changed)
        return self._id[key]

    @property
    def id(self):
        """
        Retorna o identificador numerico
        """
        return self._id['id']
        
    @id.setter    
    def id(self, value):
        """
        Modifica o id se a instancia nao for somente leitura
        """
        if (self._ro):
            raise KastError(u"Identidade é somente leitura.")
        else:
            self._id['id'] = value
            self.notify(Identity.changed)

    @property
    def name(self):
        """
        Retorna o nome
        """
        return self._id['name']
        
    @name.setter    
    def name(self, value):
        """
        Modifica o nome se a instancia nao for somente leitura
        """
        if (self._ro):
            raise KastError(u"Identidade é somente leitura.")
        else:
            self._id['name'] = value
            self.notify(Identity.changed)

    @property
    def description(self):
        """
        Retorna a descricao
        """
        return self._id['description']
        
    @description.setter    
    def description(self, value):
        """
        Modifica a descricao se a instancia nao for somente leitura
        """
        if (self._ro):
            raise KastError(u"Identidade é somente leitura.")
        else:
            self._id['description'] = value
            self.notify(Identity.changed)

    def __iter__(self):
        """
        Necessario para definir a classe como generator
        """
        return self._id.iteritems()

#-------------------------------------------------------------------------------

if __name__ == "__main__":
    print u"Módulo attribute"
    print u"Criado por {0} ({1})".format(__author__, __email__)
    print u"Versão {0} - {1}".format(__version__, __status__)
