from autosockets import *

print 'AUTOSOCKETS'

s = socket('128.238.66.230',12345)
print s.recv()
s.send(raw_input() + '\n')
print s.recv()
s.send(raw_input() + '\n')
print s.recv()
s.send(raw_input() + '\n')
print s.recv(r'I am\.')