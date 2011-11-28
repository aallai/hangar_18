import smtplib
import imaplib
import poplib
from config import config

POP = 0
IMAP = 1
 
# base class for transmission medium 
# just a draft for now

class Medium(object) :

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

		
class MailboxServer(object) :

	'''
Encapsulates all the details of wether to use pop, imap, ssl bla bla
	'''

	def __init__(self, host, port, user, passwd) :
		
		self.host = host
		self.port = port
		self.user = user
		self.passwd = passwd

	def fetch_mail() : 
		
		'''
	Returns the body of every message in the inbox.
		'''	

class ImapServer(MailboxServer) :

	def __init__(self, host, user, passwd, port=0, use_ssl=True) :
		
		if port == 0 :
			if use_ssl :
				port = 993
			else :
				port = 143

		super().__init__(host, port, user, passwd)
		self.use_ssl = use_ssl


	def fetch_mail(self) :
		
		try :
			server = None

			if use_ssl :
				server = imaplib.IMAP4_SSL(self.host, self.port)
			else :
				server = imaplib.IMAP(self.host, self.port)
			
			server.login(self.user, self.passwd)
			# checks INBOX by default
			server.select()

			ls = []
			for index in server.search(None, 'ALL')[1][0].split() :			
				ls.append(server.fetch(index, '(UID BODY[TEXT])')[1][0][1])					
	
			return ls	

		except IMAP4.error e :
			raise EmailError(e.message)			


class EmailMedium(Medium) :

	'''
Represents an email account to which messages can be sent (and possbly received if we have the password for it).
	'''


	def __init__(self, address, mailbox_server=None) :

		# MTU depends on smtp settings of server... maybe we should connect here and figure it out
		self.address = address
		self.mtu = 2048          # temporary	
		self.mailbox_server = mailbox_server



	def send(self, data, mid, seq, key) :
			
		# not sure this works with every smtp server
	
		server = smtplib.SMTP(config['smtp_server'])
		server.starttls()
		server.login(config['smtp_user'], config['smtp_passwd'])		


		msg = '\n'.join([key, mid + ' ' + str(seq), data])
		
		server.sendmail(self.address, self.address, msg)
		server.quit()		

	
	def receive(self, key) :

		if not (self.mailbox_server) :
			raise EmailError("Tried to receive email account for which no IMAP/POP server was provided.") 

		'''
	Scan email account for messages
		'''

		messages = mailbox_server.fetch_mail()

	

