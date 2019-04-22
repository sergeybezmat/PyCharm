from flask import Flask, render_template, request
from sqlalchemy import create_engine
import datetime
import json

now = datetime.datetime.now()
dataa = now.strftime("%Y-%m-%d")
data_yesterday = now - datetime.timedelta(days=1)
yesterday = data_yesterday.strftime("%Y-%m-%d")
mon = now.month

app = Flask(__name__)
engine = create_engine("postgresql://naucrm:naucrm@172.16.201.15:5432/naumenreportsdb")
connection1 = engine.connect()

@app.route('/')
def home():
     return render_template('home.html')

@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/ind')
def ind():
    login = request.args.get('login')
    # план звонков за день
    plan_calls = connection1.execute("select distinct stringcontent from mv_phone_call, mv_flex_attribute, mv_employee where mv_flex_attribute.identifier = 'plan_calls' and mv_phone_call.operatoruuid=mv_flex_attribute.objuuid and mv_phone_call.operatoruuid=mv_employee.uuid and login = '{0}'".format(login))
    for i in plan_calls:
        plan_calls = i[0]
    plan_month = int(plan_calls)*21
    # топ
    spisok = [(' ', 'Пусто') for i in range(3)]
    top = connection1.execute("with vspom as (select operatortitle, Sum(Case When direction = 'Inbound' Then 1 Else 0 End) as direction From mv_phone_call where direction = 'Inbound' and creationdate >= '{0}'::date and creationdate <'{0}'::date+1 group by operatortitle) select direction, operatortitle from vspom order by direction desc, operatortitle".format(dataa))

    for i, v in enumerate(top):
      if i<3:
        spisok[i] = v
        surname_name = spisok[i][1].split()
        del surname_name[-1]
        surname_name = surname_name[1] + ' ' + surname_name[0]
        spisok[i] = (spisok[i][0], surname_name)
      else:
          break
    #исходящие звонки за сегодня
    # план звонков за день
    plan_outcalls = connection1.execute("select distinct stringcontent from mv_phone_call, mv_flex_attribute, mv_employee where mv_flex_attribute.identifier = 'plan_outcalls' and mv_phone_call.operatoruuid=mv_flex_attribute.objuuid and mv_phone_call.operatoruuid=mv_employee.uuid and login = '{0}'".format(login))
    for i in plan_outcalls:
        plan_outcalls = i[0]
    plan_month_out = int(plan_outcalls) * 21

    return render_template('ind.html', title='Статистика', plan_outcalls=plan_outcalls, plan_month_out=plan_month_out, plan_calls=plan_calls, plan_month=plan_month, name1=spisok[0][1], calls1=spisok[0][0], name2=spisok[1][1], calls2=spisok[1][0], name3=spisok[2][1], calls3=spisok[2][0])

@app.route('/calls_all')
def calls_all():
    login = request.args.get('login1')
    # звонки за сегодня
    calls_today = connection1.execute("select count(*) from mv_phone_call, mv_employee where operatortitle = title and direction = 'Inbound' and login = '{0}' and mv_phone_call.creationdate >= '{1}'::date and mv_phone_call.creationdate <'{1}'::date+1;".format(login, dataa))
    for i in calls_today:
        calls_today = i[0]
    calls_month = connection1.execute("select count(*) from mv_phone_call, mv_employee where operatortitle = title and direction = 'Inbound' and login = '{0}' and mv_phone_call.creationdate >= '2019-0{1}-01'::date and mv_phone_call.creationdate <'2019-0{1}-30'::date;".format(login, mon))
    for i in calls_month:
        calls_month = i[0]

    calls_yest = connection1.execute("select count(*) from mv_phone_call, mv_employee where operatortitle = title and direction = 'Inbound' and login = '{0}' and mv_phone_call.creationdate >= '{1}'::date and mv_phone_call.creationdate <'{1}'::date+1;".format(login, yesterday))
    for i in calls_yest:
        calls_yest = i[0]

 #исходящие звонки за сегодня
    outcalls_today = connection1.execute("select count(*) from mv_phone_call, mv_employee where operatortitle = title and direction = 'Outbound' and login = '{0}' and mv_phone_call.creationdate >= '{1}'::date and mv_phone_call.creationdate <'{1}'::date+1;".format(login, dataa))
    for i in outcalls_today:
        outcalls_today = i[0]

    #Исходящие звонки за вчера
    outcalls_yest = connection1.execute("select count(*) from mv_phone_call, mv_employee where operatortitle = title and direction = 'Outbound' and login = '{0}' and mv_phone_call.creationdate >= '{1}'::date and mv_phone_call.creationdate <'{1}'::date+1;".format(login, yesterday))
    for i in outcalls_yest:
        outcalls_yest = i[0]
    #Исходящие звонки за месяц
    outcalls_month = connection1.execute("select count(*) from mv_phone_call, mv_employee where operatortitle = title and direction = 'Outbound' and login = '{0}' and mv_phone_call.creationdate >= '2019-0{1}-01'::date and mv_phone_call.creationdate <'2019-0{1}-30'::date;".format(login, mon))
    for i in outcalls_month:
        outcalls_month = i[0]
    calls_all = {"calls_month": calls_month, "calls_today": calls_today, "calls_yest": calls_yest, "outcalls_today": outcalls_today, "outcalls_yest": outcalls_yest, "outcalls_month": outcalls_month}
    calls_all = json.dumps(calls_all, ensure_ascii=False)
    print(calls_all)
    return calls_all

@app.route('/top')
def top():
    spisok = [(' ', 'Пусто') for i in range(3)]
    top = connection1.execute("with vspom as (select operatortitle, Sum(Case When direction = 'Inbound' Then 1 Else 0 End) as direction From mv_phone_call where direction = 'Inbound' and creationdate >= '{0}'::date and creationdate <'{0}'::date+1 group by operatortitle) select direction, operatortitle from vspom order by direction desc, operatortitle".format(dataa))
    for i, v in enumerate(top):
      if i<3:
        spisok[i] = v
        surname_name = spisok[i][1].split()
        del surname_name[-1]
        surname_name = surname_name[1] + ' ' + surname_name[0]
        spisok[i] = (spisok[i][0], surname_name)
      else:
          break
    top1 = {"name1": spisok[0][1], "calls1": spisok[0][0], "name2": spisok[1][1], "calls2": spisok[1][0], "name3": spisok[2][1], "calls3": spisok[2][0]}
    top1 = json.dumps(top1, ensure_ascii=False)

    return top1




if __name__ == "__main__":
          app.run(treding = True)