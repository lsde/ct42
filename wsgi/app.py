import requests
import bs4
from flask import Flask, request
from flask import render_template

app = Flask(__name__)
src = 'http://www.ceskatelevize.cz/ct24/zive-vysilani/'

iframe_working = True

@app.route('/')
def root():
	r = requests.get(src)
	soup = bs4.BeautifulSoup(r.text)
	global iframe_working
	for link in soup.find_all('iframe'):
		iframe_link = link.get('src')
		if 'iFramePlayerCT24' in iframe_link:
			url = iframe_link
			iframe_working = True
		else:
			url = 'about:blank'
			iframe_working = False
		return render_template('index.html', url=url)

@app.route('/ivysilani/<path:link>')
def ivysilani(link):
	full_link = request.url
	link = full_link.replace(request.url_root, '/')
	url = 'http://www.ceskatelevize.cz' + link
	r = requests.get(url)
	return r.text

@app.route('/monitoring', methods=['GET'])
def monitoring():
	if iframe_working:
		return 'blebleble OK'
	else:
		return 'blebleble CRITICAL'

if __name__ == '__main__':
	app.debug = True
	app.run('0.0.0.0')
