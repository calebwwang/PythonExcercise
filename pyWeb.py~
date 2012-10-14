from bottle import route, run, get, post, request

f = open('example.htm')

@route('/prompt')
def hello():
    return f.read()


@post('/data') # or @route('/login', method='POST')
def login_submit():
    name = request.forms.get('name')
    print name
    return "<p>Your login was correct</p>"
run(host='localhost', port=8080, debug=True)
