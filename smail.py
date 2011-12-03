#!/usr/bin/python

import sys
import pickle
import os
from config import config
import core


users = None


def main(argv) :

	setup()

	menu = '''
Welcome!

1 Retreive messages
2 Send a message
3 Exit
'''
	while True :

		try : 
			action = int(raw_input(menu))
			print		
	
			if action == 1 :
				retreive_messages()
			elif action == 2 :
				send()
			elif action == 3 :
				sys.exit(1)
			else :
				bogus_input()					

		except ValueError :
			bogus_input()	
 

def bogus_input() :
	sys.stderr.write('\nEnter a choice from the menu.\n')		


def send() :
	
	menu = '''
1 Specify a plaintext file
2 Type into prompt
3 Return to menu
'''	

	try :
		action = int(raw_input(menu))
                print

                if action == 1 :
			f = raw_input('file : ')
	
			try :
				data = open(f.strip(), 'r').read()
				get_dest_and_send(data)
			except IOError :
				print "Can't open file."
				send()	

		elif action == 2 :
			print 'Enter EOF when done.'

			data = ''			
			line = raw_input() 

			while line.strip() != 'EOF' :
				data += line + '\n'		
				line = raw_input()

			get_dest_and_send(data)

		elif action == 3 :
			return

		else :
			raise ValueError

	except ValueError :
		bogus_input()
		send()

def get_dest_and_send(data) :

	try :

		dest = raw_input('Enter the user you wish to send to : ')
		core.send(users.local_user, users.remote_users[dest.strip()], data)
		
		print 'Message sent'

	except KeyError, e :
		print  e.message + ' is not in your list of users'
		get_dest_and_send(data)	

# check for config files and inbox folder, do some sanity checks
def setup() :

	global users

	if not os.access(config['inbox'], os.W_OK) :
		if os.path.exists(config['inbox']) :
			sys.exit('Inbox directory exists but is inaccessible, exiting.')		
		else :
			print 'Creating inbox folder'
			os.mkdir(config['inbox'])
	
		

	if os.access(config['user_db'], os.R_OK) :

                try :
			users = pickle.load(open(config['user_db'], 'r'))
                except pickle.UnpicklingError, e :
                        sys.exit('Error reading contact list file : \n' + e.message)

        else :
                if os.path.exists(config['user.db']) :
                        sys.exit('User list file exists but is inaccessible, exiting.')

                # create new userlist object
		print 'Creating new user list'
                users = UserList()


def retreive_messages() :

	print 'Retreiving messages...'

	d = core.receive(users.local_user)

	# only display new messages
	new = { mid : data for mid, data in d.items() if mid not in os.listdir(config['inbox']) }

	# no new messages
	if not new :
		print 'No new messages.'
		return
		
	print 'Storing new messages in inbox'

	for mid, data in new.items() :
		f = open(os.path.join(config['inbox'], mid), 'w')
		f.write(data)
		f.close
	
	for mid, data in new.items() :
		print
		print 'Message ID -> ' + mid	
		print
		print data
		

if __name__ == '__main__' :
	main(sys.argv)
