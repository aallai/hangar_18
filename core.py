import sys
import random
import hashlib
import time


'''
Functions to send and receive messages using the protocol
'''

def send(medium_list, data, sender_key, receiver_key) :

	# unique message id
	mid = hashlib.md5(sender_key + receiver_key + str(time.time())).hexdigest()
	
	data_len = len(data)
	med_len = len(medium_list)

	min_mtu = 5	

	for medium in medium_list :		
		if medium.mtu < min_mtu :
			min_mtu = medium.mtu

	'''
	split up the data in (data_len / min_mtu) chunks of size min_mtu  
	the smaller our chunks the more obfuscated the data is, will have to
	revisit this
	''' 

	segments = []

	for i in xrange(data_len / min_mtu) :			
		segments += [ (i, data[i*min_mtu : i*min_mtu + min_mtu]) ]

	seq_len = len(segments)

	if (data_len % min_mtu != 0) :
		segments += [ (seq_len, data[seq_len * min_mtu :]) ]
		seq_len += 1
	
	messages_per_medium = len(segments) / med_len	
	
	# permute segments 
	random.shuffle(segments)

	for i in xrange(med_len) :
		send_range(medium_list[i], segments[i * messages_per_medium : i*messages_per_medium + messages_per_medium], receiver_key, mid)
		
	if (med_len * messages_per_medium % seq_len != 0) :
		send_range(medium_list[0], segments[med_len * messages_per_medium :], receiver_key, mid)		
			


def send_range(medium, segments, key, mid) :

	print segments

	for seq, segment in segments :
                        medium.send(segment, mid, seq, key)

def receive(medium_list, receiver_key) :
	
	'''
Returns a dictionary {mid : data} for every message found by scanning medium_list.
	'''

	# assumes that medium.receive returns a dictionary in the form {mid : [ (seq, data), ...]}
	messages = {}
	for medium in medium_list :
		d = medium.receive(receiver_key)

		for mid, segments in d.items() :
			try :
				messages[mid] += segments
			except KeyError :
				messages[mid] = segments
	
	# python guesses how to sort this correctly 		
	return {mid : ''.join([seg[1] for seg in sorted(segments)]) for mid, segments in messages.items()}	
	
		
