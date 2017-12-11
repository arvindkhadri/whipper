from flask import Flask, render_template, request, session, url_for, redirect
from clarifai import rest
from clarifai.rest import ClarifaiApp, Image
from uuid import uuid4
from config import *
import requests


app = Flask(__name__)
SECRET_KEY = uuid4().hex

def whip(item):
    d = {}
    url = item.get('input').get('data').get('image').get('url')
    names = [el.get('name') for el in item.get('data').get('concepts')]
    d[url] = names
    return d

@app.route('/')
def index():
    return render_template("index.html", url=URL)

@app.route('/redirect')
def redirector():
    """ Get the code and then make a request to get the auth token.
    Set the auth token in session.
    After successful login, navigate the user to the app page."""
    url = "https://api.instagram.com/oauth/access_token"
    params = {"client_id": INSTA_APP_ID,
              "client_secret": INSTA_APP_SECRET,
              "grant_type": "authorization_code",
              "redirect_uri": REDIRECT_URI,
              "code": request.args.get("code")}
    response = requests.post(url, data=params)
    response_json = response.json()
    session['insta_auth'] = response_json.get('access_token')
    return redirect(url_for('main_app'))

@app.route('/main_app')
def main_app():
    """Get images of the logged in user."""
    response = requests.get(MEDIA_URL.format(session.get('insta_auth')))
    images = [image.get('images') for image in response.json().get('data')]
    urls = map(lambda x: x.get('standard_resolution').get('url'), images)
    base_64_contents = map(lambda url: Image(url=url), urls)
    capp = ClarifaiApp(api_key=CLARIFAI_APP_ID)
    model = capp.models.get('general-v1.3')
    output = model.predict(base_64_contents)
    results = map(whip, output.get('outputs'))
    return render_template('app.html', response=results)

if __name__ == '__main__':
    app.secret_key = SECRET_KEY
    app.run(debug=True)
