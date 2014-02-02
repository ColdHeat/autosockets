from isis import *
from autosockets import *

s=socket('128.238.66.230',12345)
s.settimeout(5)

shell(s)
