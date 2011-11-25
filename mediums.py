import smtplib
import imaplib
import poplib

POP = 0
IMAP = 1

# base class for transmission medium 
# just a draft for now

class Medium :

	'''Base class for transmission medium.'''

	# key to identify the user, will need to be unique among users, maybe an RSA key? 
	user_key = ''

	
	def send(self, data, mid, seq) :
		
		'''
	mid -> message id
	seq -> sequence number
	data -> string to send
		'''


	def receive(self) :
		
		'''
	Scan the email account for messages sent to this user, should return
	maybe a dictionary of tuples, { mid : (seq, data) } ?
		'''
	

	def mtu(self) :

		'''
	Something to get the medium's mtu, for example you can only send a limited amount of
	characters in a tweet.
		'''

class EmailMedium(Medium) :

	# use POP as default, some webmail services don't offer IMAP	

	def __init__(self, key, address, proto=POP) :

		if proto != POP and proto != IMAP :
			return None 

		self.user_key = key
		self.addr = address
		self.recv_proto = proto	


	def send(self, data, mid, seq) :
		
		'''
	Make a header and use smtp to send the data
		'''

	
	def receive(self) :

		'''
	Scan email account for messages
		'''

		if (self.recv_proto == POP) :
			recv_pop(self)
		else :
			recv_imap(self)


	def recv_pop(self) :

		'''
	TODO
		'''

	def recv_imap(self) :
 
		'''
	TODO
		'''
