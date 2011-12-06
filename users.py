import re

class User(object) :

	def __init__(self, name, key, mlist=None) :

                self.name = name
                self.key = key
                self.mlist = mlist

	def tostring(self) :

		s = '\n\t'.join(['%s\n{', 'key -> %s'] + [re.sub('\n', '\n\t', m.tostring()) for m in self.mlist])
		s +='\n}'
		return s % (self.name, self.key)

class UserList(object) :

	'''
Object which will hold users of the system and their medium lists.
We pickle this and store as a file.	
	'''

	def __init__(self) :

		'''
	{ user.name : user_object }
		'''

		self.local_user = None
		self.remote_users = {}
