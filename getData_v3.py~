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

def get_player_urls(player_list):
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
			except UnicodeDecodeError:
				print "Ignoring UnicodeDecodeError"
		results.close()
	return player_profile_urls

# This function takes a dictionary of player names and urls and returns height, weight, age, and birthplace for the player
def get_player_data(player_urls):
	items = player_urls.items()
	for i in range(len(items)):
		search_url = items[i]
		name, url = search_url
		results=urllib2.urlopen(url)
		l = results.readlines()
		for index in range(len(l)):
			line = l[index]
			# Check for height data
			if line.count('Height</strong>') > 0:
				height = getData(line)
				
				#print height
			# Check for weight data
			if line.count('Weight</strong>') > 0:
				weight = getData(line)
				#print weight
			# Check for age data
			if line.count('Age</strong>') > 0:
				age = getData(line)
				#print age

			# Check for birthplace
			if line.count('Born</strong>') > 0:
				born = getFrom(line)
				#print born
		data = [height, weight, age, born]
	results.close()
	
def getData(line):
	# This function gets height weight and age data 
	data = line.split(' ')[1]
	data = data.strip()
	return data 
def getFrom(line):
	# This function gets where the player is from
	fromLine = line.split(' ', 1)[1]
	return fromLine
player_file_path = 'playerData.csv'
players = get_players(player_file_path)
player_urls = get_player_urls(players)
get_player_data(player_urls)
#items = player_urls.items()
#print items
#search_url = items[0]
#name, url = search_url
#print url 
