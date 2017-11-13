from flask import Flask, render_template,redirect,request
import json
import random
import requests
import requests_toolbelt.adapters.appengine

requests_toolbelt.adapters.appengine.monkeypatch()

app = Flask(__name__, template_folder="templates")

CLIENT_ID = '694111034037-uo4iqbripr3lvcckki8ul49503pmfe9h.apps.googleusercontent.com'
CLIENT_SECRET = '1zqhDCvzUKZth74HI-BHwiTU'
REDIRECT_URI = 'https://winged-octagon-173512.appspot.com/oauth'
REDIRECT_URI2 = 'https://winged-octagon-173512.appspot.com/oauth2'
state = random.randint(0,99999999)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login/')
def login():
	
	login_url = "https://accounts.google.com/o/oauth2/v2/auth?" + "response_type=code&client_id=" + CLIENT_ID + "&redirect_uri=" + REDIRECT_URI + "&scope=email&state=" + str(state)
	return redirect(login_url, code=302)
	
@app.route('/oauth')
def oauth():
	if str(state) == request.args.get('state'):
		url = 'https://www.googleapis.com/oauth2/v4/token'
		data = {'code': request.args.get('code'), 'client_id': CLIENT_ID, 'client_secret': CLIENT_SECRET, 'redirect_uri':REDIRECT_URI,'grant_type':"authorization_code"}
		r = requests.post(url, data)
		credentials = json.loads(r.text)
		token = 'Bearer ' + credentials["access_token"]
 	  	headers = {'Authorization': token}
    	req_uri = 'https://www.googleapis.com/plus/v1/people/me'
    	r = requests.get(req_uri, headers=headers)
    	content = json.loads(r.text)
    	name = content["displayName"]
    	google_plus_link = content["url"]
    	return render_template('oauth.html', name=name, google_plus_link=google_plus_link, state=state)
	
if __name__ == '__main__':
    app.run()
 