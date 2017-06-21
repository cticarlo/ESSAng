# -*- coding: utf-8 -*-

import sys
sys.path.insert(0, "..")
import time


from opcua import ua, Server


if __name__ == "__main__":

    # setup our server
    server = Server()
    server.set_endpoint("opc.tcp://0.0.0.0:4840/freeopcua/server/")

    # setup our own namespace, not really necessary but should as spec
    uri = "http://examples.freeopcua.github.io"
    idx = server.register_namespace(uri)

    # get Objects node, this is where we should put our nodes
    objects = server.get_objects_node()

    # populating our address space
    myobj = objects.add_object(idx, "MyObject")
    myvar = myobj.add_variable(idx, "MyVariable", 6.7)
    myvar2 = myobj.add_variable(idx,"MyVariable2",2.3)
    myvar.set_writable()    # Set MyVariable to be writable by clients
    myvar2.set_writable()
    # starting!
    server.start()
    
    try:
        #count = 0
        myvar.set_value(0.0)
        myvar2.set_value(0.0)
        while True:
            time.sleep(0.1)
            #count += 0.1
            myvar.set_value(myvar.get_value()+0.1)
            myvar2.set_value(myvar2.get_value()+0.1)
            
    finally:
        #close connection, remove subcsriptions, etc
        server.stop()