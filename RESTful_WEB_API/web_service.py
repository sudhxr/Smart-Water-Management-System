
# Importing Flask modules
from flask import Flask, url_for
from flask import request
from flask import json
from flask import Response
from flask.ext.cors import CORS, cross_origin

# Importing supporting modules
import os
from datetime import datetime

# Declaring the app object
app = Flask(__name__)
cors = CORS(app)

# GET /
@app.route('/')
def api_root():
	return 'Welcome'

# Get /articles
@app.route('/articles')
def api_articles():
	return 'List of ' + url_for('api_articles')

#Get particular article detail
@app.route('/articles/<articleid>')
def api_article(articleid):
	return 'You are reading ' + articleid

# Get request with arguments
# @app.route('/hello')
# def api_hello():
#     if 'name' in request.args:
#         return 'HI ' + request.args['name']
#     else:
#         return 'HI John Doe'

# Handling different types of request
@app.route('/echo', methods = ['GET', 'POST', 'PATCH', 'PUT', 'DELETE'])
def api_echo():
	if request.method == 'GET':
		return "ECHO: GET\n"

	elif request.method == 'POST':
		return "ECHO: POST\n"

	elif request.method == 'PATCH':
		return "ECHO: PACTH\n"

	elif request.method == 'PUT':
		return "ECHO: PUT\n"

	elif request.method == 'DELETE':
		return "ECHO: DELETE"

# POST Request header
@app.route('/messages', methods = ['POST'])
def api_message():

	if request.headers['Content-Type'] == 'text/plain':
		return "Text Message: " + request.data

	elif request.headers['Content-Type'] == 'application/json':
		return "JSON Message: " + json.dumps(request.json)

	elif request.headers['Content-Type'] == 'application/octet-stream':
		f = open('./binary', 'wb')
		f.write(request.data)
		f.close()
		return "Binary message written!"

	else:
		return "415 Unsupported Media Type ;)"

# GET for hello
@app.route('/hello', methods = ['GET'])
def api_hello():
	data = {
		'hello'  : 'world',
		'number' : 3
	}
	js = json.dumps(data)

	resp = Response(js, status=200, mimetype='application/json')
	resp.headers['Link'] = 'http://luisrei.com'

	return resp

# Turn on the LED4
def glow_4_on():
	os.system("sshpass -p raspberry ssh -o StrictHostKeyChecking=no pi@192.168.0.5 python /home/pi/Desktop/glow_Red_on.py &")

	processed_data = {}
	# Status of LED
	processed_data['status']=1
	# Time date
	dt = datetime.now()
	processed_data['time']=dt.strftime('%Y-%m-%d %H:%M:%S')

	return processed_data

# Turn off the LED4
def glow_4_off():
	print "Started command"
	os.system("sshpass -p raspberry ssh -o StrictHostKeyChecking=no pi@192.168.0.5 python /home/pi/Desktop/glow_Red_off.py")
	os.system("killall sshpass")
	processed_data = {}
	# Status of LED
	processed_data['status']=0
	# Time date
	dt = datetime.now()
	processed_data['time']=dt.strftime('%Y-%m-%d %H:%M:%S')

	print "Sent request"
	return processed_data

# POST request rpiglow
@app.route('/rpiglow', methods=['POST'])
# @cross_origin(origin='*',headers=['Content-Type','Authorization'])
def api_rpiglow():
	if request.headers['Content-Type'] == 'application/json':
		req = request.json
		command_details = req['command']
		if str(command_details) == "on":
			# on_status = True
			process_data = glow_4_on()
			return json.dumps(process_data)

		# elif str(command_details) == "off" and on_status == True:
		elif str(command_details) == "off":
			# on_status = False
			process_data = glow_4_off()
			return json.dumps(process_data)

		else:
			return "Command not found"

# Starting the flask server
if __name__ == '__main__':
	app.run(debug=True,host= '0.0.0.0')
