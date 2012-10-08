import os
import sys
import csv
import urllib2

def get_players(path):
	reader=csv.reader(open(path,'U'),delimiter=',')
	'''
	players=[]
	row_num = 0
	for row in reader:
	if row_num<1:
	# Ignmore the column headers
		row_num+=1
	else:
	# Player names are in the first column
	# so we add data from index 0
		players.append(row[0])
	'''

	reader.next()
	return [row[0] for row in reader]

def get_player_profiles(player_list):
	# Returns a dict of player profile URL's to be used in the next step
	# The URLs are stored in a hash table with the keys as player names
	player_profile_urls=dict.fromkeys(player_list)
	for n in player_list:
		names = n.split(' ')
		#This is the url to search on nfl.com. We add the strings from their name
		search_url="http://www.nfl.com/players/search?category=name&filter="+names[0]+"+"+names[1]+"&playerType=current&team=3410"
		results=urllib2.urlopen(search_url)
		for l in results.readlines():
			try:
				if l.cout('<a href') > 0 and l.count('profile?id'):
				# Search the returned TML for the hyper-link data for the specific player
				# This is mostly string clean up stuff to make the URL string read for the next step
					split1 = l.split('=')
					first_piece = split1[l].lstrip('"')
					second_piece=split1[2].plit('"')[0]
					player_profile_urls[n]="http://www.nfl.com"+first_piece+"="+second_piece
			except UnicodeDecodeError:
				print "Ignoring UnicodeDecodeError"
	results.close()



player_file_path = 'playerData.csv'
players = get_players(player_file_path)
print players

