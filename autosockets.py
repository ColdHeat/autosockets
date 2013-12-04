import sys
import os
import re

import socket as _socket
from socket import AF_INET, AF_INET6, AF_UNIX, SOCK_STREAM, SOCK_DGRAM

try: 
    from pebble import thread
except ImportError:
    print "Threading decorator unavailable. Install pebble with sudo pip install pebble"

class print_hook:
    """ Dirty hack for overriding default print behavior """
    def __init__(self, *writers) :
    	self.writers = writers
    	
    def write(self, text):
        for w in self.writers :
            if text != '\n':
                if len(text) > 0 and text[-1] == '\n':
                     w.write("[DEBUG] " + text)
                     return
                w.write("[DEBUG] " + text + "\n")

class error_hook:
    def __init__(self, *writers) :
    	self.writers = writers
    	
    def write(self, text):
        for w in self.writers :
            if text != '\n': 
                w.write("[ERROR] " + text + "\n")

sys.stdout = print_hook(sys.stdout)
##sys.stderr = error_hook(sys.stderr)


class socket:
    def __init__(self, addr, port, timeout=1, stype=AF_INET, sproto=SOCK_STREAM):
        self.s = _socket.socket(stype, sproto)
        self.s.connect((addr, port))
        self.s.settimeout(timeout)

    def recv(self, end='\n', regex = False):
        total=[]
        data='\n'
        while data != "":
            try: 
                data = self.s.recv(8192)
                if end in data:
                    total.append(data)
                    data = ""
                    break
                total.append(data)
                data = ""
            except _socket.error:
                break

        if regex:
           return re.findall(regex, ''.join(total))
        return ''.join(total)

    def send(self, text):
        self.s.sendall(text)
    
