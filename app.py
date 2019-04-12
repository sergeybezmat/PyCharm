from flask import Flask
from flask import render_template, request#, redirect, url_for
from sqlalchemy import create_engine
import datetime

now = datetime.datetime.now()
dataa = now.strftime("%Y-%m-%d")
data_vhera = now - datetime.timedelta(days=1)
vhera = data_vhera.strftime("%Y-%m-%d")
mon = now.month

app = Flask(__name__)
engine = create_engine("postgresql://naucrm:naucrm@172.16.200.199:5432/naumenreportsdb")
connection1 = engine.connect()

@app.route('/')
def home():
     return render_template('home.html')

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
    spisok = [(' ', 'Пусто') for i in range(3)]
    t = connection1.execute("with vspom as (select operatortitle, Sum(Case When direction = 'Inbound' Then 1 Else 0 End) as direction From mv_phone_call where direction = 'Inbound' and creationdate >= '{0}'::date and creationdate <'{0}'::date+1 group by operatortitle) select direction, operatortitle from vspom order by direction desc, operatortitle".format(dataa))
    for i, v in enumerate(t):
        spisok[i] = v
        eq=spisok[i][1].split()
        del eq[-1]
        eq = eq[1] + ' ' + eq[0]
        spisok[i] = (spisok[i][0], eq)
    return render_template('ind.html', title='Статистика', user=fio, za_seg=zv_seg, za_vch=zv_vch, za_mes=za_mes, name1=spisok[0][1], rez1=spisok[0][0], name2=spisok[1][1], rez2=spisok[1][0], name3=spisok[2][1], rez3=spisok[2][0])


if __name__ == "__main__":
          app.run()