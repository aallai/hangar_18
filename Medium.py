
# base class for transmission medium 
# just a draft for now

Class Medium :

	'''Base class for transmission medium.'''
	
	def send(user, data, mid, seq) :
		
		'''
	I am thinking of this sending one message (i.e a single email or tweet or whatever),
	I am not sure what user will be yet, maybe just an adress (this might limit the mediums
	we can use), maybe an object of some sort containing medium specific info about the user.

	user -> ???
	mid -> message id
	seq -> sequence number
	data -> string to send
		'''


	def receive(user, mid) :

		'''
	Again, not sure what user will be, mid is the message id.
		'''


	def mtu() :

		'''
	Something to get the medium's mtu, for example you can only send a limited amount of
	characters in a tweet.
		'''
	
