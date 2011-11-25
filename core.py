import sys
import random


'''
Functions to send and receive messages using the protocol
'''

def send(medium_list, data, sender_key) :

	

	min_mtu = sys.maxint 
	
	for medium in medium_list :		
		if medium.mtu < min_mtu :
			min_mtu = medium.mtu

	# split up the data in (len(data) / min_mtu) chunks of size min_mtu  
	segments = []

	for i in xrange(len(data) / min_mtu) :			
		segments.append( (i, data[i*min_mtu: i*min_mtu + min_mtu]) )

	messages_per_medium = len(segments) / len(medium_list)	

	# permute segments 
	random.shuffle(segments)
	
	for i in xrange(len(medium_list)) :

		for (seq, segment) in segments[i*messages_per_medium : i*messages_per_medium + messages_per_medium] :
			medium_list[i].send()
