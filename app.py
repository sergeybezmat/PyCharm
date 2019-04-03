from flask import Flask
from flask import render_template, request, redirect, url_for
from sqlalchemy import create_engine
from flask import render_template

app = Flask(__name__)
engine = create_engine("postgresql://naucrm:naucrm@172.16.200.199:5432/naumendb")
connection = engine.connect()

s = connection.execute('SELECT * FROM naumb_file_type').fetchall()
s1 = connection.execute('SELECT login, status, sub_status, sum(duration) FROM ns_agent_sub_status_duration GROUP BY login, status, sub_status').fetchall()


@app.route('/')
def index():
     return render_template('add_user.html', s=s, s1=s1)

