import os
import sys
import csv
import urllib2
from bottle import route, run, get, post, request
import HTML


# The prompt page where it asks for a players name
@route('/prompt')
def hello():
    # Read in the html file from the local directory
    f = open('prompt.htm')
    return f.read()
    f.close()


# The page where it displays the data
@post('/data')
def login_submit():
    # Get the names from the prompt and split them on commas
    names = request.forms.get('name').split(',')
    player_data = []
    # Loop through the list of names and fetch the corresponding url and player data
    for i in range(len(names)):
	    player_url = get_player_urls(names[i])
	    player_data.append(get_player_data(player_url))
	    player_data[i].insert(0,names[i])
    # Add the titles to the table
    player_data.insert(0,['Name', 'Height', 'Weight', 'Age', 'Birthdate/Birthplace'])
    # Turn the python list into an html text table
    htmlTable = HTML.table(player_data)
    outFile1 = open('output1.htm')
    outFile2 = open('output2.htm')
    return outFile1.read() + htmlTable + outFile2.read()
    outFile1.close()
    outFile2.close()

# This function takes a string of player names and returns their corresponding urls
def get_player_urls(player_list):
	# Turn the string into a list 
	player_list = [player_list]
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
	# Find all the items in the dictionary
	items = player_urls.items()
	# Loop through and extract the url in each item
	for i in range(len(items)):
		search_url = items[i]
		name, url = search_url
		results=urllib2.urlopen(url)
		l = results.readlines()
		# Look through each line for the data I want
		for index in range(len(l)):
			line = l[index]
			# Check for height data
			if line.count('Height</strong>') > 0:
				height = getData(line)
			# Check for weight data
			if line.count('Weight</strong>') > 0:
				weight = getData(line)
			# Check for age data
			if line.count('Age</strong>') > 0:
				age = getData(line)
			# Check for birthplace
			if line.count('Born</strong>') > 0:
				born = getFrom(line)
		# Package the data
		data = [height, weight, age, born]
	results.close()
	return data
	
def getData(line):
	# This function gets height weight and age data 
	data = line.split(' ')[1]
	data = data.strip()
	return data 
def getFrom(line):
	# This function gets where the player is from
	fromLine = line.split(' ', 1)[1]
	fromLine = fromLine.strip()
	return fromLine

# Setup the local server
run(host='localhost', port=8080, debug=True)

