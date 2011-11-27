import smtplib
import imaplib
import poplib
from config import config

POP = 0
IMAP = 1
 
# base class for transmission medium 
# just a draft for now

class Medium :

	'''Base class for transmission medium.'''
 
	# mtu, useful for splitting up the message
	mtu = 0
	
	def send(self, data, mid, seq, key) :
		
		'''
	mid -> message id
	seq -> sequence number
	data -> string to send
	key -> key used to identify protocol messages remote user
		'''


	def receive(self, key) :
		
	 	'''
	key -> key to identify protocol messages for the local user

	Scan the email account for messages sent to this user, should return
	maybe a dictionary of lists of tuples, { mid : [(seq1, data1), ... (seqn, datan)] } ?
		'''

class EmailError(Exception) :

	'''
Base class for email errors
	'''

	def __init__(self, reason) :
		self.reason = reason


class EmailMedium(Medium) :

	'''
Represents an email account to which messages can be sent (and possbly received if we have the password for it).
	'''

	'''
CEST LE BORDEL ICITTE
	'''

	def __init__(self, address, recv_server=None, passwd=None, proto=None) :

		# MTU depends on smtp settings of server... maybe we should connect here and figure it out
		self.address = address
		self.mtu = 2048          # temporary	

		if recv_server and passwd and proto :

			if proto != IMAP and proto != POP :
				return None

			self.server = recv_server
			self.passwd = passwd
			self.proto = proto
		else :
			self.server = None
			self.passwd = None
			self.proto = None


	def send(self, data, mid, seq, key) :
			
		# not sure this works with every smtp server
	
		server = smtplib.SMTP(config['smtp_server'])
		server.starttls()
		server.login(config['smtp_user'], config['smtp_passwd'])		


		msg = '\n'.join([key, mid + ' ' + str(seq), data])
		
		server.sendmail(self.address, self.address, msg)
		

	
	def receive(self, key) :

		if not (self.passwd and self.proto) :
			raise EmailError("Tried to receive on another user's email account.") 

		'''
	Scan email account for messages
		'''

		if (self.recv_proto == POP) :
			recv_pop(self, key)
		else :
			recv_imap(self, key)


	def recv_pop(self, key) :

		'''
	TODO
		'''

	def recv_imap(self, key) :
 
		'''
	TODO
		'''


	

