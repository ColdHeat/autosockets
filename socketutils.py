import re

def __valid(addr):
	return (len(addr) == 4 and all(quad <= 255 and quad >= 0 for quad in addr))

def __confirm():
	tmp = 'n'
	while True:
		inp = raw_input('Generating large amount of IP Addresses. Are you sure you want to continue? [y/N] ')
		if inp != '':
			tmp = inp.lower()

		if tmp not in ['y', 'n']:
			print 'Invalid option'
			continue

		return False if tmp == 'n' else True

## http://cmikavac.net/2011/09/11/how-to-generate-an-ip-range-list-in-python/
# Return a list of IP Addresses from start_ip until end_ip
def ipRange(start_ip, end_ip):
	start = list(map(int, start_ip.split(".")))
	end = list(map(int, end_ip.split(".")))

	if not __valid(start):
		raise Exception('Invalid Start IP Address')

	if not __valid(end):
		raise Exception('Invalid End IP Address')

	for i in range(4):
		if start[i] > end[i]:
			start, end = end, start
			break

	temp = start
	ip_range = []
	
	ip_range.append(".".join(map(str, start)))
	while temp != end:
		temp[3] += 1
		for i in (3, 2, 1):
			if temp[i] == 256:
				temp[i] = 0
				temp[i-1] += 1
		ip_range.append(".".join(map(str, temp)))
	  
	return ip_range

# Return a list of IP Addresses based on a starting address and a wildcard mask
def ipWildcardMask(addr, mask):
	_addr = list(map(int, addr.split('.')))
	_mask = list(map(int, mask.split('.')))

	if not __valid(_addr):
		raise Exception('Invalid IP Address')

	if not __valid(_mask):
		raise Exception('Invalid IP Mask')

	if _mask[1] > 127 and not __confirm():
		return [] 

	start = []
	end = []

	for quad in range(4):
		start.append(_addr[quad] & (_mask[quad] ^ 0xFF))
		end.append(_addr[quad] | _mask[quad])

	return ipRange('.'.join(map(str, start)), '.'.join(map(str, end)))

## http://boubakr92.wordpress.com/2012/12/20/convert-cidr-into-ip-range-with-python/
# Return a list of IP Addresses from CIDR notation
def ipCidr(addr):
	_addr, _cidr = addr.split('/')

	_cidr = int(_cidr)

	if _cidr > 32 or _cidr < 0:
		raise Exception('Invalid CIDR')

	if _cidr < 16 and not __confirm():
		return []

	_mask = [0, 0, 0, 0]
	for i in range(_cidr):
		_mask[i/8] = _mask[i/8] + (1 << (7 - i % 8))

	_mask = [quad ^ 0xFF for quad in _mask]

	return ipWildcardMask(_addr, '.'.join(map(str, _mask)))

# Return a known regular expression, or validate a custom regular expression
def regex(reg = ''):
	if reg.lower() == 'ictf':
		return '(FLG\w+)'
	elif reg.lower() == 'csaw':
		return 'key{(.*)}'
	elif reg.lower() == 'mitll':
		return 'flag_(.*)'
	elif reg.lower() == 'pico':
		return 'key:(.*)'
	else:
		try:
			re.compile(reg)
		except re.error:
			return ''
		else:
			return reg
		