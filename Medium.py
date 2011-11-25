
# base class for transmission medium 
# just a draft for now

Class Medium :

	'''Base class for transmission medium.'''

	# key to identify the user, will need to be unique among users, maybe an RSA public key? 
	user_key = ''

	
	def send(self, data, mid, seq) :
		
		'''
	mid -> message id
	seq -> sequence number
	data -> string to send
		'''


	def receive(self, user, mid) :


	def mtu(self) :

		'''
	Something to get the medium's mtu, for example you can only send a limited amount of
	characters in a tweet.
		'''
	
