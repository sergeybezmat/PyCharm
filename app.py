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

engine = create_engine("postgresql://naucrm:naucrm@172.16.200.199:5432/naumenreportsdb")
connection1 = engine.connect()

app.config['REDIS_URL'] = 'redis://172.16.200.199:6379/db0'
redis = Redis(app, 'REDIS')
r = redis.hgetall("agents:state:offline")

#топ операторов



@app.route('/')
def home():
     return render_template('home.html')


@app.route('/index')
def index():
    l = request.args.get('login')
    # Звонки за сегодня
    zv = connection.execute("SELECT Sum(Case When is_processed = true Then 1 Else 0 End) as is_processed FROM ns_inbound_call_data WHERE agent_connected = '{0}' and created_date = '{1}' ".format(l, dataa))
    for i in zv:
        za_seg = i[0]
        if za_seg == None:
            za_seg = 0
    # Звонки за вчера
    zv1 = connection.execute("SELECT Sum(Case When is_processed = true Then 1 Else 0 End) as is_processed FROM ns_inbound_call_data WHERE agent_connected = '{0}' and created_date = '{1}' ".format(l, vhera))
    for i in zv1:
        za_vch = i[0]
        if za_vch == None:
            za_vch = 0
    #время реакции на заявку
    vreak = connection.execute("select avg(incoming_rt) from ns_inbound_call_data where agent_connected = '{0}' and is_processed = true group by agent_connected".format(l))
    for i in vreak:
        vreak = round(i[0])
    if type(vreak) != int:
        vreak = 0

    # время разговора
    vraz = connection.execute("select avg(incoming_tt) from ns_inbound_call_data where agent_connected = '{0}' and is_processed = true group by agent_connected".format(l))
    for i in vraz:
        vraz = round(i[0])
    if type(vraz) != int:
        vraz = 0

    #Звонки за месяц
    if mon < 10:
        vmes = connection.execute("SELECT Sum(Case When is_processed = true Then 1 Else 0 End) as is_processed FROM ns_inbound_call_data WHERE agent_connected = '{0}' and created_date like '____-0{1}-__'".format(l, mon))
    else:
        vmes = connection.execute("SELECT Sum(Case When is_processed = true Then 1 Else 0 End) as is_processed FROM ns_inbound_call_data WHERE agent_connected = '{0}' and created_date like '____-{1}-__'".format(l, mon))
    for i in vmes:
        vmon = i[0]
        if vmon == None:
            vmon = 0

    #топ операторов
    spisok = [(' ', 0) for i in range(3)]
    t = connection.execute("with vspom as (select agent_connected, Sum(Case When is_processed = true Then 1 Else 0 End) as is_processed From ns_inbound_call_data where created_date = '{0}' and is_processed!=false group by agent_connected ) select is_processed, agent_connected from vspom order by is_processed DESC, agent_connected".format(dataa))
    for i, v in enumerate(t):
        spisok[i] = v
    return render_template('index.html', title='Статистика', user=l, za_mes=vmon, timeraz=vraz, timereak=vreak, za_vch=za_vch, za_seg=za_seg, name1=spisok[0][1], rez1=spisok[0][0], name2=spisok[1][1], rez2=spisok[1][0], name3=spisok[2][1], rez3=spisok[2][0])

@app.route('/redis') #Не нужен, но вдруг пригодится
def redis():
     return render_template('redis.html', title='Redis', r=r)

@app.route('/ind')
def ind():
    l = request.args.get('login')
    # вывод ФИО по логину
    imya = connection1.execute("select objtitle from mv_skill_relation where login = '{0}'".format(l))
    for i in imya:
        fio = i[0]
    # звонки за сегодня
    zv_seg = connection1.execute("select count(*) from mv_phone_call where direction = 'Inbound' and operatortitle = '{0}' and creationdate >= '{1}'::date and creationdate <'{1}'::date+1;".format(fio, dataa))
    for i in zv_seg:
        zv_seg = i[0]

    # звонки за вчера
    zv_vch = connection1.execute("select count(*) from mv_phone_call where direction = 'Inbound' and operatortitle = '{0}' and creationdate >= '{1}'::date and creationdate <'{1}'::date+1;".format(fio, vhera))
    for i in zv_vch:
        zv_vch = i[0]

    # звонки за месяц
    za_mes = connection1.execute("select count(*) from mv_phone_call where direction = 'Inbound' and operatortitle = '{0}' and creationdate >= '2019-0{1}-01'::date and creationdate <'2019-0{1}-30'::date;".format(fio, mon))
    for i in za_mes:
        za_mes = i[0]
    # топ
    spisok = [(' ', 0) for i in range(3)]
    t = connection1.execute("with vspom as (select operatortitle, Sum(Case When direction = 'Inbound' Then 1 Else 0 End) as direction From mv_phone_call where direction = 'Inbound' and creationdate >= '{0}'::date and creationdate <'{0}'::date+1 group by operatortitle) select direction, operatortitle from vspom order by direction desc, operatortitle".format(dataa))
    for i, v in enumerate(t):
        spisok[i] = v
    return render_template('ind.html', title='Статистика', user=fio, za_seg=zv_seg, za_vch=zv_vch, za_mes=za_mes, name1=spisok[0][1], rez1=spisok[0][0], name2=spisok[1][1], rez2=spisok[1][0], name3=spisok[2][1], rez3=spisok[2][0])


if __name__ == "__main__":
          app.run()