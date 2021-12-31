import time
import socket
import wx

from wx.lib.pubsub import Publisher
from knoten.models import Knoten

from threading import Thread

class NCoTThread(Thread):
    """ Thread für die Kommunikation mit einer ncot-node. """
    Knoten = None

    def __init__(self, Knoten):
        """Init NCoT Thread Class."""
        Thread.__init__(self)
        self.Knoten = Knoten
        self.start()    # start the thread
        
    def run(self):
        """NCoT Thread main loop."""
        # Als erstes initialisieren der Verbindungen
        if not self.Knoten.verbindung_set.count() == 1:
            # Hier eine Meldung an das GUI einfügen.
            return
        verbindung = knoten.verbindung_set.all()[0]
        tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_address = ('localhost', verbindung.port)
        tcp_socket.bind(server_address)
 
        # Listen on port 81
        tcp_socket.listen(1)

        while True:
            wx.CallAfter(Publisher().sendMessage, "update", "waiting for connection")
            connection, client = tcp_socket.accept()
            
            try:
                wx.CallAfter(Publisher().sendMessage, "update", "connection accepted. {}".format(client))
               
                # Receive and print data 32 bytes at a time, as long as the client is sending something
                while True:
                    data = connection.recv(32)
                    wx.CallAfter(Publisher().sendMessage, "update", "Received data: {}".format(data))
                    
                    if not data:
                        break
 
            finally:
                connection.close()
            wx.CallAfter(Publisher().sendMessage, "update", "connection finished.")
