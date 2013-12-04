autosockets
===========
autosockets is a python module meant to lessen the amount of work and intimidation of writing socket code. This is 
to aid those who are newcomers to scripting during a CTF. It also includes some prepackaged functionality that will
aid a CTF veteran. 

Optional Dependencies: 
https://pypi.python.org/pypi/Pebble

autosockets.socket(addr, port, timeout=1, stype=AF_INET, sproto=SOCK_STREAM)
 * Returns the socket connected to addr at port
 * The socket will have a timeout of 1 second by default 
 * The addr should be IPv4 as specified by stype and the protocol TCP as specified by sproto. 

autosockets.recv(regex=False, end='\n'))
 * Returns either a list or a string depending on the value of regex.
 * The regex parameter is a string parameter specifying a regex to match the recieved string against. Useful for parsing out keys.
 * The end parameter specifies the terminating character or characters as a string. 
 
autosockets.send(text)
 * Sends text to server. You must add your own newline.
