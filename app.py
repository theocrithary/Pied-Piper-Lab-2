#!/usr/bin/env python3
import os
import redis
import json
from flask import Flask, render_template, redirect, request, url_for, make_response

if 'VCAP_SERVICES' in os.environ:
    VCAP_SERVICES = json.loads(os.environ['VCAP_SERVICES'])
    CREDENTIALS = VCAP_SERVICES["rediscloud"][0]["credentials"]
    r = redis.Redis(host=CREDENTIALS["hostname"], port=CREDENTIALS["port"], password=CREDENTIALS["password"])
else:
    r = redis.Redis(host='127.0.0.1', port='6379')

app = Flask(__name__)

@app.route('/')
def mainpage():

	response = """
	<HTML><head>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <link rel="apple-touch-icon" href="/static/apple-touch-icon.png">
    <title>Pied Piper - Sprint 2 - Survey</title>
    <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css" integrity="sha384-BVYiiSIFeK1dGmJRAkycuHAHRg32OmUcww7on3RYdg4Va+PmSTsz/K68vbdEjh4u" crossorigin="anonymous">
    <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap-theme.min.css" integrity="sha384-rHyoN1iRsVXV4nD0JutlnGaslCJuC7uwjduW9SVrLvRYooPp2bWYgmgJQIXwl/Sp" crossorigin="anonymous">
    </head>
    <BODY><h2>
	<a href="/survey">Take Survey</a><br>
	<a href="/dumpsurveys">Survey Results</a><br>
	</h2>
	</BODY>
	"""
	return response

@app.route('/survey')
def survey():
    resp = make_response(render_template('survey.html'))
    return resp

@app.route('/suthankyou.html', methods=['POST'])
def suthankyou():

    global r
    b = request.form['business']
    l = request.form['location']
    f = request.form['feedback']

    print ("Business Unit is " + b)
    print ("Location is " + l)
    print ("Feedback: " + f)

    Counter = r.incr('new_counter')
    print ("the counter is now: ", Counter)
    ## Create a new key that includes the counter
    newsurvey = 'new_survey' + str(Counter)

    print ("Storing the survey now")
    ## Now the key name is the content of the variable newsurvey
    r.hmset(newsurvey,{'business':b,'location':l,'feedback':f})
	
    resp = """
    <h3> - THANKS FOR TAKING THE SURVEY - </h3>
    <a href="/">back</a><br>
    """
    return resp

@app.route('/dumpsurveys')
def dumpsurveys():

    global r
    response = "Dump of all reviews so far<br>"
    response += "--------------------------<br>"
    print ("Reading back from Redis")
    for eachsurvey in r.keys('new_survey*'):
        response += "Business Unit : " + str(r.hget(eachsurvey,'business'),'utf-8') + "<br>"
        response += "Location    : " + str(r.hget(eachsurvey,'location'),'utf-8') + "<br>"
        response += "Feedback : " + str(r.hget(eachsurvey,'feedback'),'utf-8') + "<br>"
        response += " ----------------------<br>"

    return response

if __name__ == "__main__":
	app.run(debug=False, host='0.0.0.0', \
                port=int(os.getenv('PORT', '5000')), threaded=True)
