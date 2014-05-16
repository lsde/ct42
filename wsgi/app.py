import requests
import bs4
from flask import Flask
from flask import request
from flask import url_for
from flask import render_template
from flask import Response

app = Flask(__name__)
src = 'http://www.ceskatelevize.cz/ct24/zive-vysilani/'

@app.route('/')
def root():
	r = requests.get(src)
	soup = bs4.BeautifulSoup(r.text)
	for link in soup.find_all('iframe'):
		iframe_link = link.get('src')
		if 'iFramePlayerCT24' in iframe_link:
			url = 'http://www.ceskatelevize.cz' +  iframe_link
        return render_template('index.tpl', url=url)

@app.route('/static')
def foo():
        url_for('static', filename='.*')

if __name__ == '__main__':
	app.debug = True
        app.run()
