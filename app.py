#!/usr/bin/env python
from __future__ import print_function
import os
import time
import traceback
from flask import Flask, request, redirect
from flask import render_template
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support import expected_conditions as expected
from selenium.webdriver.support.wait import WebDriverWait

app = Flask(__name__)
app.debug = bool(int(os.getenv('APP_DEBUG', 0)))
listen_host = os.getenv('LISTEN_HOST', 'localhost')
listen_port = int(os.getenv('LISTEN_PORT', 5000))
endpoint_host = os.getenv('ENDPOINT_HOST', 'localhost')
endpoint_port = os.getenv('ENDPOINT_PORT', 4444)


@app.route('/favicon.ico')
def favicon():
    return redirect('/static/favicon.ico')


@app.route('/mon')
def mon():
    return 'OK'


@app.route('/<path:subpath>')
def ivysilani(subpath):
    return root(subpath)


@app.route('/')
def root(subpath=None):
    options = Options()
    options.add_argument('-headless')
    driver = webdriver.Remote(command_executor="http://{0}:{1}".format(endpoint_host, endpoint_port), options=options)
    wait = WebDriverWait(driver, timeout=10)
    try:
        if subpath:
            div_class = 'mainPanel'
            driver.get('https://www.ceskatelevize.cz/' + subpath)
        else:
            div_class = 'live-video'
            driver.get('https://ct24.ceskatelevize.cz/#live')
        video = wait.until(expected.visibility_of_element_located((By.CLASS_NAME, div_class)))
        element = video.find_element_by_tag_name('iframe').get_attribute('outerHTML')
    except Exception as e:
        traceback.print_exc()
        if app.debug:
            driver.save_screenshot('static/screenshot.png')
        element = '<img src="/static/tv_static.gif">'
    finally:
        driver.quit()
    return render_template('index.html', element=element)


if __name__ == '__main__':
    app.run(host=listen_host, port=listen_port, threaded=True)
