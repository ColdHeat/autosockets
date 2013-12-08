import re

def wildcard(addr):
	'''
	Return a generator for ip addresses with wildcards in them
	Ex: wildcard('1.1.1.*')

	'''
	addr = [[int(x)] if x != "*" else "*" for x in addr.split('.')]

	for x in xrange(len(addr)):
		if addr[x] == '*':
			addr[x] = range(256)

	for a in addr[0]:
		for b in addr[1]:
			for c in addr[2]:
				for d in addr[3]:
					yield "{}.{}.{}.{}".format(a,b,c,d)

def ip_range(range):
	'''
	http://cmikavac.net/2011/09/11/how-to-generate-an-ip-range-list-in-python/
	Return a generator for ip addresses in the range 
	Ex: ip_range('1.1.1.1 - 1.1.1.255')

	'''
	addr = range.split('-')
	start = list(map( int, addr[0].strip().split('.') ) )
	end = list(map( int, addr[1].strip().split('.') ) )

	start[3] = start[3]-1

	temp = start
	ip_range = []
	
	ip_range.append(".".join(map(str, start)))
	while temp != end:
		temp[3] += 1
		for i in (3, 2, 1):
			if temp[i] == 256:
				temp[i] = 0
				temp[i-1] += 1
		yield ".".join(map(str, temp))


def _ipWildcardMask(addr, mask):
	'''Return a list of IP Addresses based on a starting address and a wildcard mask'''
	_addr = list(map(int, addr.split('.')))
	_mask = list(map(int, mask.split('.')))

	if _mask[1] > 127:
		return [] 

	start = []
	end = []

	for quad in range(4):
		start.append(_addr[quad] & (_mask[quad] ^ 0xFF))
		end.append(_addr[quad] | _mask[quad])

	return ip_range('.'.join(map(str, start))+'-'+'.'.join(map(str, end)))

def cidr(addr):
	'''
	http://boubakr92.wordpress.com/2012/12/20/convert-cidr-into-ip-range-with-python/
	Return a list of IP Addresses from CIDR notation
	'''
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

	return _ipWildcardMask(_addr, '.'.join(map(str, _mask)))

def gen_addrs(addr):
	if '*' in addr:
		return wildcard(addr)
	elif '-' in addr:
		return ip_range(addr)
	elif '/' in addr:
		return cidr(addr)

def regex(reg = ''):
	'''Return a known regular expression, or validate a custom regular expression'''
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

if __name__ == '__main__':
	print list(gen_addrs('*.1.1.1'))
	print list(gen_addrs('1.1.1.1 - 1.1.1.80'))
	print list(gen_addrs('1.1.1.1/24'))
