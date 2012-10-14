import os
import sys
import csv
import urllib2
import html5lib
from html5lib import treebuilder

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
				# Find the link to the players page
				if l.count('<a href') > 0 and l.count('/profile"'):
				# Search the returned HTML for the hyper-link data for the specific player
				# This is mostly string clean up stuff to make the URL string read for the next step
					split1 = l.split('=')
					first_piece = split1[0].lstrip('"')
					second_piece=split1[1].split('"')[1]
					player_profile_urls[n]="http://www.nfl.com/"+second_piece
					print "\n \n This is the url:" 
					print player_profile_urls[n]
			except UnicodeDecodeError:
				print "Ignoring UnicodeDecodeError"
		results.close()
	return player_profile_urls

def parse_data(player_urls):
# Returns a dict of player data parse trees indexed by player name
	# Create a dict indexed by player names
	player_data = dict.fromkeys(player_urls.keys())
	for name in player_urls.keys():
	# Use par treebuilders library to parse the html
		parser = html5lib.HTMLParser(tree=treebuilders.getTreeBuilder("beautifulsoup"))
		tree = parser.parse(urllib2.urlopen(player_urls[name]).read())
		# The data we are looking for is contained in a <p></p> tag, so we search for these tags
		data = tree.findAll("p")
		stats = data[2:5]
		data_temp = []
		for i in stats:
		# All important data comes after a colon, so we split before and after the colon.
			decoded = i.decode("utf-8")
			pieces=decoded.split(':')
			data_temp.append(pieces)
		# Create a dict
		player_dict=dict.fromkeys(['heigth','weight','dob','college'])
		# Once split and stored in data_temp, extract the useful data
		# Extract height
		height = string_cleaner_hw(data_temp[0][1])
		player_dict['height']=height
		# Extract wieght
		weight = int(string_cleaner_hw(data_temp[0][2]))
		player_dict['weight']=weight
		# Extract DOB
		dob = string_cleaner_dob(data_temp[1][1])
		player_dict['dob']=dob
		# Extract college
		college = string_cleaner_college(data_temp[2][1])
		player_dict['college']=college
		player_data[name]=player_dict
	return player_data

def string_cleaner_hw(data_string):
	# This function cleans the strings for height and weight
	data_string = data_string.strip()
	data_string=data_string.split('\n')[0]
	return data_string.split(' ')[0].encode()

def string_cleaner_dob(data_string):
	# This function cleans the strings for DOB
	data_string = data_string.strip()
	data_string=data_string.split('\t')[0]
	return data_string.split('\n')[0].encode()

def string_cleaner_college(data_string):
	# This function cleans the strings for college data
	data_string = data_string.strip()
	return data_string.split('\n')[0].encode()


player_file_path = 'playerData.csv'
players = get_players(player_file_path)
player_urls = get_player_profiles(players)
parsed_player_data=parse_data(player_urls)
print parsed_player_data



