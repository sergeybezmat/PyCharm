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
def home():
     return render_template('home.html')


@app.route('/index')
def index():
     l = request.args.get('login')
     if l == None:
          vvedi=1
     else:
            zaplog = connection.execute("SELECT namee, surname, plan, fakt, plan_mes, fakt_mes, za_vch, za_seg FROM TEST WHERE login='{0}'".format(l)).fetchone()
            user = {'username': zaplog[0]}
            sur = {'surname': zaplog[1]}
            plan = {'p': zaplog[2]}
            fakt = {'f': zaplog[3]}
            plan_mes = {'p': zaplog[4]}
            fakt_mes = {'f': zaplog[5]}
            za_vch = {'z': zaplog[6]}
            za_seg = {'z': zaplog[7]}
            vvedi = 0
     return render_template('index.html', title='Статистика', user=user, sur=sur, plan=plan, fakt=fakt, plan_mes=plan_mes, fakt_mes=fakt_mes, za_vch=za_vch, za_seg=za_seg, vvedi=vvedi)



@app.route('/redis')
def redis():

     return render_template('redis.html', title='Redis', r=r)

if __name__ == "__main__":
          app.run()