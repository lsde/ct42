#!/usr/bin/env python
from __future__ import print_function
import os
from flask import Flask, request
from flask import render_template
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

app = Flask(__name__)
app.debug = bool(int(os.getenv('APP_DEBUG', 0)))
listen_host = os.getenv('LISTEN_HOST', 'localhost')
listen_port = int(os.getenv('LISTEN_PORT', 5000))
endpoint_host = os.getenv('ENDPOINT_HOST', 'localhost')
endpoint_port = os.getenv('ENDPOINT_PORT', 8910)

@app.route('/')
def root():
    driver = webdriver.Remote(command_executor="http://{0}:{1}".format(endpoint_host, endpoint_port),
                              desired_capabilities=DesiredCapabilities.CHROME)
    driver.get('https://ct24.ceskatelevize.cz/#live')
    try:
        live_video = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "live-video")))
        url = live_video.find_element_by_tag_name('iframe').get_attribute('src')
    finally:
        driver.quit()
    return render_template('index.html', url=url)


if __name__ == '__main__':
    app.run(host=listen_host, port=listen_port, threaded=True)
