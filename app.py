from flask import Flask
from flask import render_template, request, redirect, url_for
from sqlalchemy import create_engine
from flask import render_template
from flask_redis import Redis

app = Flask(__name__)
engine = create_engine("postgresql://naucrm:naucrm@172.16.200.199:5432/naumendb")
connection = engine.connect()

app.config['REDIS_URL'] = 'redis://172.16.200.199:6379/db0'
redis = Redis(app, 'REDIS')
r = redis.hgetall("agents:state:offline")

@app.route('/')
@app.route('/index')
def index():
     if request.args.get('username') == None:
          aq = 'Пользователь'
          sur = '!'
     else:
          if request.args.get('surname') == None:
               aq = request.args.get('username')
               sur = '!'
          else:
               aq = request.args.get('username')
               aw = request.args.get('surname')
               sur = {'surname': aw}
     user = {'username': aq}
     return render_template('index.html', title='Home', user=user, sur=sur)

@app.route('/add_user')
def add_user():
     s = connection.execute('SELECT * FROM naumb_file_type').fetchall()
     #s1 = connection.execute('SELECT login, status, sub_status, sum(duration) FROM ns_agent_sub_status_duration GROUP BY login, status, sub_status').fetchall()
     s1 = connection.execute('SELECT * FROM TEST')
     return render_template('add_user.html', title='DB', s=s, s1=s1)

@app.route('/redis')
def redis():

     return render_template('redis.html', title='Redis', r=r)

if __name__ == "__main__":
          app.run()