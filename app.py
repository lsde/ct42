#!/usr/bin/env python
from flask import Flask, request
from flask import render_template
from selenium import webdriver

app = Flask(__name__)


@app.route('/')
def root():
    if 'Firefox' in str(request.user_agent):
        return render_template('unsupported.html')

    driver = webdriver.Remote(command_executor="http://127.0.0.1:8910",
                              desired_capabilities={'javascriptEnabled' : True,
                                                    'loadImages' : False}
                              )
    driver.get('http://www.ceskatelevize.cz/ct24#live')
    iframe = driver.find_element_by_class_name('live-video').find_element_by_tag_name('iframe')
    url = iframe.get_attribute('src')
    return render_template('index.html', url=url)


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, threaded=True)
