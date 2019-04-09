from flask import Flask
from flask import render_template, request#, redirect, url_for
from sqlalchemy import create_engine
from flask_redis import Redis
import datetime

now = datetime.datetime.now()
dataa = now.strftime("%Y-%m-%d")
data_vhera = now - datetime.timedelta(days=1)
vhera = data_vhera.strftime("%Y-%m-%d")
mon = now.month

app = Flask(__name__)
engine = create_engine("postgresql://naucrm:naucrm@172.16.200.199:5432/naumendb")
connection = engine.connect()

app.config['REDIS_URL'] = 'redis://172.16.200.199:6379/db0'
redis = Redis(app, 'REDIS')
r = redis.hgetall("agents:state:offline")


#топ





@app.route('/')
def home():
     return render_template('home.html')


@app.route('/index')
def index():
    l = request.args.get('login')
    # Звонки за сегодня
    zv = connection.execute("SELECT is_processed FROM ns_inbound_call_data WHERE agent_connected = '{0}' and created_date = '{1}' ".format(l, dataa))
    chet_seg = 0
    for i in zv:
        if i[0] == True:
            chet_seg += 1
    # Звонки за вчера
    zv1 = connection.execute("SELECT is_processed FROM ns_inbound_call_data WHERE agent_connected = '{0}' and created_date = '{1}' ".format(l, vhera))
    chet_vch = 0
    for i in zv1:
        if i[0] == True:
            chet_vch += 1
    #время реакции на заявку
    vreak = connection.execute("select avg(incoming_rt) from ns_inbound_call_data where agent_connected = '{0}' and is_processed = true group by agent_connected".format(l))
    for i in vreak:
        vreak = round(i[0], 2)
    # время разговора
    vraz = connection.execute("select avg(incoming_tt) from ns_inbound_call_data where agent_connected = '{0}' and is_processed = true group by agent_connected".format(l))
    for i in vraz:
        vraz = round(i[0], 2)
    #Звонки за месяц
    if mon < 10:
        vmes = connection.execute("SELECT is_processed FROM ns_inbound_call_data WHERE agent_connected = '{0}' and created_date like '____-0{1}-__'".format(l, mon))
    else:
        vmes = connection.execute("SELECT is_processed FROM ns_inbound_call_data WHERE agent_connected = '{0}' and created_date like '____-{1}-__'".format(l, mon))
    vmon = 0
    for i in vmes:
        if i[0] == True:
            vmon += 1
    #топ операторов

    t = connection.execute("with vspom as (select agent_connected, Sum(Case When is_processed = true Then 1 Else 0 End) as is_processed From ns_inbound_call_data where created_date = '{0}' and is_processed!=false group by agent_connected ) select is_processed, agent_connected from vspom order by is_processed DESC, agent_connected".format(dataa))
    spisok = []
    for i in t:
        spisok.append(i)
    for k in range(2):
        if spisok[k][0]:
            for i in range(2):
                spisok.append((' ', 0))
    user = {'username':l}
    za_mes = {'z': vmon}
    timeraz = {'t': vraz}
    timereak = {'t': vreak}
    za_vch = {'z': chet_vch}
    za_seg = {'z': chet_seg}
    return render_template('index.html', title='Статистика', user=user, za_mes=za_mes, timeraz=timeraz, timereak=timereak, za_vch=za_vch, za_seg=za_seg, name1=spisok[0][1], rez1=spisok[0][0], name2=spisok[1][1], rez2=spisok[1][0], name3=spisok[2][1], rez3=spisok[2][0])



@app.route('/redis') #Не нужен, но вдруг пригодится
def redis():
     return render_template('redis.html', title='Redis', r=r)

if __name__ == "__main__":
          app.run()