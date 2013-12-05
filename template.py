#! /usr/bin/python

from autosockets import *
from socketutils import *

import sys
import time

## Payload Specific Imports Start

## Payload Specific Imports End

## Options Start
# Regex to retrieve the key; can be either a known CTF regex (iCTF, CSAW, MITLL, 
# Pico) or a custom regex
KEY_REGEX = regex('')

# String, List, or use one of the functions in `socketutils.py`
SERVICE_IP = ''
SERVICE_PORT = 0

# IP Address of Key Submission Server; Leave blank if no submission server
KEY_IP = ''
KEY_PORT = 0

SEND_KEY = False

TIMEOUT = 3.0
SLEEP   = 0.3

# All of the retrieved keys will be accumulated here; you can perform additional
# processing on them in `process()`
KEYS = []

# Show all parameters before running
DEBUG = False
## Options End

## Payload Start
# All send/receive calls to trigger the exploit belong here. Leave the final 
# receive to get they flag out; it will be handled below
def payload(s):
	pass
## Payload End

## Process Key Start
# Clean up the KEYS list and perform and post-processing if necessary. If not,
# make sure the function has a `pass`
def process():
	global KEYS

	pass
## Process Key End

# === DO NOT EDIT BELOW THIS LINE ==============================================
@thread
def _exploit(SERVER):
	global SERVICE_PORT, TIMEOUT, KEY_REGEX

	s = socket(SERVER,SERVICE_PORT,TIMEOUT)
	payload(s)
	return s.recv(KEY_REGEX)

def exploit():
	global SERVICE_IP, SERVICE_PORT, TIMEOUT

	if isinstance(SERVICE_IP, str):
		SERVICE_IP = [SERVICE_IP]
	for _SERVER in SERVICE_IP:
		_key = _exploit(_SERVER).get()
		if isinstance(_key, list):
			KEYS.extend(_key)
		else:
			KEYS.append(_key)

def submit():
	global KEY_IP, KEY_PORT, TIMEOUT, KEYS

	s = socket(KEY_IP,KEY_PORT,TIMEOUT)
	for key in KEYS:
		s.send('{key}\n'.format(key=key))
		print s.recv()
		time.sleep(SLEEP)

def parameters():
	global SERVICE_IP, SERVICE_PORT, KEY_REGEX, KEY_PORT, KEY_IP, TIMEOUT, SLEEP, SEND_KEY

	print 'Running with the following parameters:'
	print '  SERVICE'
	print '   > IP(s): {}'.format(SERVICE_IP)
	print '   > PORT: {}'.format(SERVICE_PORT)
	if KEY_REGEX:
		print '   > REGEX: {}'.format(KEY_REGEX)
	if SEND_KEY == True and not (KEY_IP == '' or KEY_PORT == 0):
		print ''
		print '  KEY SUBMISSION'
		print '   > IP: {}'.format(KEY_IP)
		print '   > PORT: {}'.format(KEY_PORT)

def main():
	global SERVICE_IP, SERVICE_PORT, KEY_IP, KEY_PORT, SEND_KEY, DEBUG

	if DEBUG:
		parameters()

	if not SERVICE_IP or SERVICE_PORT == 0:
		print 'Service IP/Service Port not set. Please set them and run again.'
		sys.exit()

	if SEND_KEY == True and (KEY_IP == '' or KEY_PORT == 0):
		print 'Key IP/Key Port not set. Keys will NOT be submitted'
		SEND_KEY = False

	exploit()
	process()
	if SEND_KEY:
		submit()
	else:
		print KEYS

if __name__ == '__main__':
	main()