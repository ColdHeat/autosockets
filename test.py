from autosockets import *

print 'AUTOSOCKETS'

s = socket('128.238.66.230',12345)
print s.recv()
s.send('\n')
print s.recv()
s.send('\n')
print s.recv()
s.send('\n')
print s.recv()

listener(6969)