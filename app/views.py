import datetime

from flask import render_template
from app import app


@app.route('/test')
@app.route('/test/<data>')
def test(data=None):
    server_gmt_time  = datetime.datetime.now()
    result = server_gmt_time.strftime("%d-%m-%Y %H:%M")
    
    if data is not None:
        result = data
    
    return result

@app.route('/')
@app.route('/index/')
@app.route('/index')
def index():
    posts = [{'author': {'username': 'Vlad'},
              'body': 'Beautiful day in Portland!'},

             {'author': {'username': 'Tony'},
              'body': 'Nice mother'},

             {'author': {'username': 'Mark'},
              'body': 'Bullshit!'}]

    return render_template('index.html', title='INDEX', posts=posts)