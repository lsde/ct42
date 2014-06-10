import requests
import bs4
from flask import Flask
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
			url = 'http://www.ceskatelevize.cz' + iframe_link
			iframe_working = True
		else:
			url = 'about:blank'
			iframe_working = False
		return render_template('index.html', url=url)

@app.route('/monitoring', methods=['GET'])
def monitoring():
	if iframe_working:
		return 'blebleble OK'
	else:
		return 'blebleble CRITICAL'

if __name__ == '__main__':
	app.debug = True
	app.run('0.0.0.0')
