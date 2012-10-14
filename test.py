import os
import sys
import csv
import urllib2
from bottle import route, run, get, post, request

# Load an hmtl file template
f = open('example.htm')

# The prompt page where it asks for a players name
@route('/prompt')
def hello():
    return f.read()

# The page where it displays the data
@post('/data') # or @route('/login', method='POST')
def login_submit():
    name = request.forms.get('name')
    test(name)
    return "<p>Your login was correct</p>"

def test(name):
	print name

run(host='localhost', port=8080, debug=True)
