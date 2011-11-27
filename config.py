config = {}

def read_configuration(file) :
	
	global config
	file = open(file, 'r')
	
	# ignores blank lines and lines starting with a #
	config = {line.split('=')[0].strip() : line.split('=')[1].strip() for line in filter(lambda x : x.split()[0].strip() != '#', filter(lambda x : x.strip(), file.read().split('\n')))}

	

