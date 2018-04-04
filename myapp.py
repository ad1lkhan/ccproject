from flask import Flask
from flask import render_template, request
from flask_navigation import Navigation

from flask_wtf import FlaskForm
from wtforms import TextField, validators
import requests
import http.client, urllib.request, urllib.parse, urllib.error, base64
from pprint import pprint
import json


class MessageForm(FlaskForm):
    message = TextField(u'Enter team name', [validators.optional(), validators.length(max=200)])


app = Flask(__name__)
app.secret_key = '0e9490ae2c4e4915aa88fe0fc509d35b'


nav = Navigation(app)

nav.Bar('top', [
    nav.Item('Home!','index'),
    nav.Item('Premier League','team')
])

@app.route('/')
@app.route('/index/')
def index():
    return render_template("index.html")

@app.route('/team/', methods=['GET','POST'])
def team():    
    form = MessageForm(request.form)
    if request.method == 'POST': 
        msg = form.message.data
        connection = http.client.HTTPConnection('api.football-data.org')
        headers = { 'X-Auth-Token': app.secret_key, 'X-Response-Control': 'minified' }
        connection.request('GET', '/v1/competitions/398/leagueTable', None, headers )
        response = json.loads(connection.getresponse().read().decode())
        
        result = 'Not found'
        for x in response['standing']:
            if x['team'].lower() == msg.lower():
                result = x['rank']
        return render_template('result.html', result=str(result))
    return render_template('my_form.html', form=form)


if __name__ == "__main__":
	app.run(host='0.0.0.0')
