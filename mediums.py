import email
import smtplib
import imaplib
import poplib
import re
from config import config
 
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

		super(ImapServer, self).__init__(host, port, user, passwd)
		self.use_ssl = use_ssl


	def fetch_mail(self) :
		
		try :
			server = None

			if self.use_ssl :
				server = imaplib.IMAP4_SSL(self.host, self.port)
			else :
				server = imaplib.IMAP4(self.host, self.port)
			
			server.login(self.user, self.passwd)
			# checks INBOX by default
			server.select()

			# poplib version returns string with \r\n scrubbed out, do the same here
			ls = []
			for index in server.search(None, 'ALL')[1][0].split() :			
				ls.append(re.sub('\r\n', '\n', server.fetch(index, '(UID BODY[TEXT])')[1][0][1]).strip('\n'))					

			server.logout()
	
			return ls

		except imaplib.IMAP4.error, e :
			raise EmailError(e.message)			

class PopServer(MailboxServer) :

        def __init__(self, host, user, passwd, port=0, use_ssl=True) :

                if port == 0 :
                        if use_ssl :
                                port = 995
                        else :
                                port = 110

                super(PopServer, self).__init__(host, port, user, passwd)
                self.use_ssl = use_ssl

	def fetch_mail(self) :

		try :
		
			server = None
	
			if self.use_ssl :
                                server = poplib.POP3_SSL(self.host, self.port)
                        else :
                                server = poplib.POP3(self.host, self.port)

			messages = []

			server.user(self.user)
			server.pass_(self.passwd)

			# a bit convoluted, poplib gets rid of the newline separating header and body, 
			# not sure how to tell where the body starts, email can do it
			for i in xrange(len(server.list()[1])) :
				messages.append( email.message_from_string( '\n'.join(server.retr(i+1)[1]) ).get_payload() )	

			server.quit()
	
			return messages			
	
		except poplib.error_proto, e :
			raise EmailError(e.message)



class EmailMedium(Medium) :

	'''
Represents an email account to which messages can be sent (and possbly received if we have the password for it).
	''' 

	def __init__(self, address, mailbox_server=None) :


		# the default MTU is pretty arbitrary... should discuss it
		self.address = address
		self.mtu = 1024
		self.mailbox_server = mailbox_server



	def send(self, data, mid, seq, key) :
		
		'''
	Send off a segment in an email
		'''
	
		# not sure this works with every smtp server
	
		server = smtplib.SMTP(config['smtp_server'])
		server.starttls()
		server.login(config['smtp_user'], config['smtp_passwd'])		


		msg = '\n'.join([key, mid + ' ' + str(seq), data])
		
		server.sendmail(self.address, self.address, msg)
		server.quit()		

	
	def receive(self, key) :

		'''
        Scan email account for messages
                '''

		if not (self.mailbox_server) :
			raise EmailError('Tried to receive email account for which no IMAP/POP server was provided.') 

		messages = self.mailbox_server.fetch_mail()

		d = {}

		for m in messages :

			# \r gets thrown in everywhere
			lines = m.split('\n')
	
			if lines[0] == key :   # protocol message for us, otherwise regular email

				try :
					mid, seq = lines[1].split()
					seq = int(seq)	
					data = '\n'.join(lines[2:])
				
					try :
						d[mid] += [(seq, data)]
					except KeyError :						
						d[mid] = [(seq, data)]	
					
				except ValueErrror : # bogus header, ignore
					pass

		return d

