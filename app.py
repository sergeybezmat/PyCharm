from flask import Flask
from flask import render_template, request, redirect, url_for
from sqlalchemy import create_engine
from flask import render_template
from flask_redis import Redis
import datetime

now = datetime.datetime.now()
dataa = now.strftime("%Y-%m-%d")
data_vhera = now - datetime.timedelta(days=1)
vhera = data_vhera.strftime("%Y-%m-%d")



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
    zv = connection.execute("SELECT is_processed FROM ns_inbound_call_data WHERE agent_connected = '{0}' and created_date = '{1}' ".format(l, dataa)) #Звонки за сегодня
    chet_seg = 0
    for i in zv:
        if i[0] == True:
            chet_seg += 1

    zv1 = connection.execute("SELECT is_processed FROM ns_inbound_call_data WHERE agent_connected = '{0}' and created_date = '{1}' ".format(l, vhera))  # Звонки за вчера
    chet_vch = 0
    for i in zv1:
        if i[0] == True:
            chet_vch += 1




    zaplog = connection.execute("SELECT namee, surname, plan, fakt, plan_mes, fakt_mes, za_vch, za_seg FROM TEST WHERE login='{0}'".format(l)).fetchone()
    user = {'username': zaplog[0]}
    sur = {'surname': zaplog[1]}
    plan = {'p': zaplog[2]}
    fakt = {'f': zaplog[3]}
    plan_mes = {'p': zaplog[4]}
    fakt_mes = {'f': zaplog[5]}
    za_vch = {'z': chet_vch}
    za_seg = {'z': chet_seg}
    return render_template('index.html', title='Статистика', user=user, sur=sur, plan=plan, fakt=fakt, plan_mes=plan_mes, fakt_mes=fakt_mes, za_vch=za_vch, za_seg=za_seg)



@app.route('/redis')
def redis():

     return render_template('redis.html', title='Redis', r=r)

if __name__ == "__main__":
          app.run()