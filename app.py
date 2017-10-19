#!/usr/bin/env python
import os
from flask import Flask, request
from flask import render_template
from selenium import webdriver

app = Flask(__name__)
app.debug = bool(int(os.getenv('APP_DEBUG', 0)))
listen_host = os.getenv('LISTEN_HOST', 'localhost')
listen_port = int(os.getenv('LISTEN_PORT', 5000))
endpoint_host = os.getenv('ENDPOINT_HOST', 'localhost')
endpoint_port = os.getenv('ENDPOINT_PORT', 8910)

@app.route('/')
def root():
    driver = webdriver.Remote(command_executor="http://{0}:{1}".format(endpoint_host, endpoint_port),
                              desired_capabilities={'javascriptEnabled' : True,
                                                    'loadImages' : False}
                              )
    driver.get('http://www.ceskatelevize.cz/ct24#live')
    iframe = driver.find_element_by_class_name('live-video').find_element_by_tag_name('iframe')
    url = iframe.get_attribute('src')
    return render_template('index.html', url=url)


if __name__ == '__main__':
    app.run(host=listen_host, port=listen_port, threaded=True)
