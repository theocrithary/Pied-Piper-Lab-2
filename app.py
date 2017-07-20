import uuid
import time
import os, sys
import re
import redis
from flask import Flask, render_template, redirect, request, url_for
from werkzeug import secure_filename
from PIL import Image
import hashlib
import json

VCAP_SERVICES = json.loads(os.environ['VCAP_SERVICES'])
CREDENTIALS = VCAP_SERVICES["rediscloud"][0]["credentials"]
r = redis.Redis(host=CREDENTIALS["hostname"], port=CREDENTIALS["port"], password=CREDENTIALS["password"])
size = 150, 150
epoch_offset = 36000 #The offset in seconds with Sydney


app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads/'
app.config['ALLOWED_EXTENSIONS'] = set(['jpg', 'jpeg', 'JPG', 'JPEG'])

#Read the seed file and populate Redis. It could be part of an init script
f = open('sessions.txt') #Fields separated by ";" to allow for "," in description field
snames = []
stimes = []
session_list = f.readlines()
f.close()
i = 0

for each_session in session_list:
    i += 1
    newsession = "session" + str(i)
    (c, t, p, e, ro, d) = each_session.split(';')
    r.hmset(newsession,{'code':c.strip(),'title':t.strip(),'presenter':p.strip(),'epoch':e.strip(),'room':ro.strip(),'description':d.strip()})
    snames.append(t)
    stimes.append(e)

print stimes

@app.route('/')
def menu():
    global stimes
    current = int(time.time())
    anchor = 0
    for t in stimes:
        if current > int(t):
            anchor = t
       
    print "Anchor is " + str(anchor)
    return render_template('main_menu.html', anchor=anchor)

@app.route('/single.html')
def single():
    global r
    choices = ""
    i = 0
    while i < len (r.keys('session*')):
        n = snames[i]
        i +=1
        s = "session" + str(i)


        newchoice = """
                <option value="{}">{} - {}</option>""".format(n,n,r.hget(s,'presenter'))
        choices = choices + newchoice
		
##    print choices    
    return render_template('form_single.html',choices=choices)

@app.route('/sthankyou.html', methods=['POST'])
def sthankyou():
    global r
    s = request.form['session']
    c = request.form['content']
    p = request.form['presenter']    
    u = request.headers.get('User-Agent')

    Counter = r.incr('test')
    print "the counter is now: ", Counter
    newreview = 'review' + str(Counter)
    print "Lets create Redis hash: " , newreview
    hash_object = hashlib.md5(u.encode())
    MD5h = hash_object.hexdigest()
    print MD5h

##    localtime = time.strftime("%d-%b %H:%M",time.gmtime(time.time()-time.timezone))
##    time.timezone doesn't seem to work
    localtime = time.strftime("%d-%b %H:%M",time.gmtime(time.time()+epoch_offset))
    print "Sydney winter time is: ", localtime

    r.hmset(newreview,{'session':s,'content':c,'presenter':p, 'ltime':localtime, 'MD5h':MD5h})
    return render_template('form_action.html', session=s, content=c, presenter=p)

@app.route('/program.html')
def program():
    global r
    allsessions = ""

    i = 0
    while i < len (r.keys('session*')):
        i +=1
        each_session = "session" + str(i)
        epoch = r.hget(each_session,'epoch')
        room = r.hget(each_session,'room')
        title = r.hget(each_session,'title')
        presenter = r.hget(each_session,'presenter')
        description = r.hget(each_session,'description')

        human_time = time.strftime("%d-%b %H:%M",time.gmtime(int(epoch)+epoch_offset))

        thissession = '''
            <a name="{}"></a>
            <div class="container">
              <div class="content">
                    <table class="program">
                    <tr><td>{} in {}
                    <tr><td><b>{}
                    <tr><td><i>by {}
                    <tr><td>{}
                    </table>
              </div>
            </div>
            '''.format(epoch,human_time,room,title,presenter,description)

        allsessions = allsessions + thissession

    beginning = """
        <html>
        <head>
            <link rel=stylesheet type=text/css href="/static/style.css">
			<meta name="viewport" content="width=410, initial-scale=0.90">
        </head>
        <body>
            <div class="container">
              <div class="content">
                <h1>Event Program</h1>
              </div>
            </div>
        """
    theend = '''
        </body>
        </html>
        '''
    return beginning + allsessions + theend

@app.route('/rdump')
def rdump():
    global r
    output = ""
    output = output + "session, content, presenter<br>"
    for each_review in r.keys('review*'):
       output = output + "%s, %s, %s, %s, %s<br>" % (r.hget(each_review,'session'), \
                                              r.hget(each_review,'content'), \
                                              r.hget(each_review,'presenter'), \
                                              r.hget(each_review,'ltime'), \
                                              r.hget(each_review,'MD5h'))
    return output


if __name__ == "__main__":
	app.run(debug=False, host='0.0.0.0', port=int(os.getenv('PORT', '5000')))
