import requests
import bs4
from flask import Flask, request
from flask import render_template
from flask.ext import restful

app = Flask(__name__)
api = restful.Api(app)

ct_domain = 'http://www.ceskatelevize.cz'
video_src =  '{0}/ct24/zive-vysilani/'.format(ct_domain)
iframe_name = 'iFramePlayerCT24'
iframe_working = True

@app.route('/')
def root():
	r = requests.get(video_src)
	soup = bs4.BeautifulSoup(r.text)
	global iframe_working
	for link in soup.find_all('iframe'):
		iframe_link = link.get('src')
		if iframe_name in iframe_link:
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
	url = ct_domain + link
	r = requests.get(url)
	return r.text

class monitoring(restful.Resource):
	def get(self):
		if iframe_working:
			return {'status': 'OK'}
		else:
			return {'status' : 'ERROR'}

api.add_resource(monitoring, '/monitoring')

if __name__ == '__main__':
	app.run(debug=True)
