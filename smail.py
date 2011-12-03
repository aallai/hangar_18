#!/usr/bin/python

import sys
import pickle
import os
from config import config
from core import *


users = None


def main(argv) :

	setup()
	
	while True :
		menu = '''
Welcome!

1 Retreive messages
2 Send a message
3 Exit

'''

		try : 
			action = int(raw_input(menu))
			print		
	
			if action == 1 :
				retreive_messages()
								

		except ValueError :
			bogus_input()	
 

def bogus_input() :
	sys.err.write('\nEnter a valid choice from the menu.\n')		

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

	d = receive(users.local_user)

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
