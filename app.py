from flask import Flask, render_template, request
from sqlalchemy import create_engine
import datetime
import json
import sqlalchemy

now = datetime.datetime.now()
dataa = now.strftime("%Y-%m-%d")
data_yesterday = now - datetime.timedelta(days=1)
yesterday = data_yesterday.strftime("%Y-%m-%d")
mon = now.month

app = Flask(__name__)
engine = create_engine("postgresql://naucrm:naucrm@192.168.226.136:5432/naumenreportsdb") # Отчетная БД
connection1 = engine.connect()

corebo = 'corebo'

#@app.route('/published')
#@app.route('/')
@app.route('/ind')
def ind():
    uuid = request.args.get('uuid')
    if uuid[0] !='c':
        uuid = corebo + uuid[6:]
    login = connection1.execute("select login from mv_employee where uuid = '{0}'".format(uuid))
    for i in login:
        login = i[0]
    if isinstance(login, sqlalchemy.engine.result.ResultProxy):
        print('Ошибка запроса из бд')
        return render_template('ind.html', title='Ошибка при запросе данных по указанному логину', plan_outcalls=0,
         plan_month_out=0, plan_calls=0, plan_month=0,
         name1=' ', calls1=' ', name2=' ', calls2=' ',
         name3=' ', calls3=' ')
    #количество рабочих дней
    working_day = connection1.execute("select distinct stringcontent from mv_phone_call, mv_flex_attribute, mv_employee where mv_flex_attribute.identifier = 'working_day' and mv_phone_call.operatoruuid=mv_flex_attribute.objuuid and mv_phone_call.operatoruuid=mv_employee.uuid and login = '{0}'".format(login))
    for i in working_day:
        working_day = i[0]

    # план звонков за день
    plan_calls = connection1.execute("select distinct stringcontent from mv_phone_call, mv_flex_attribute, mv_employee where mv_flex_attribute.identifier = 'plan_calls' and mv_phone_call.operatoruuid=mv_flex_attribute.objuuid and mv_phone_call.operatoruuid=mv_employee.uuid and login = '{0}'".format(login))
    for i in plan_calls:
       plan_calls = i[0]
    plan_month = int(plan_calls)*int(working_day)
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
    #топ исходящих звонков за день

    out_spisok = [(' ', 'Пусто') for i in range(3)]
    out_top = connection1.execute("with vspom as (select operatortitle, Sum(Case When direction = 'Outbound' Then 1 Else 0 End) as direction From mv_phone_call where dstphonenumber != '1234' and direction = 'Outbound' and creationdate >= '{0}'::date and creationdate <'{0}'::date+1 group by operatortitle) select direction, operatortitle from vspom order by direction desc, operatortitle".format(dataa))
    for i, v in enumerate(out_top):
        if i < 3:
            out_spisok[i] = v
            surname_name = out_spisok[i][1].split()
            del surname_name[-1]
            surname_name = surname_name[1] + ' ' + surname_name[0]
            out_spisok[i] = (out_spisok[i][0], surname_name)
        else:
            break

    # план звонков за день
    plan_outcalls = connection1.execute("select distinct stringcontent from mv_phone_call, mv_flex_attribute, mv_employee where mv_flex_attribute.identifier = 'plan_outcalls' and mv_phone_call.operatoruuid=mv_flex_attribute.objuuid and mv_phone_call.operatoruuid=mv_employee.uuid and login = '{0}'".format(login))
    for i in plan_outcalls:
        plan_outcalls = i[0]
    plan_month_out = int(plan_outcalls) * int(working_day)
    return render_template('ind.html', title='Статистика', plan_outcalls=plan_outcalls, plan_month_out=plan_month_out, plan_calls=plan_calls, plan_month=plan_month, name1=spisok[0][1], calls1=spisok[0][0], name2=spisok[1][1], calls2=spisok[1][0], name3=spisok[2][1], calls3=spisok[2][0], out_name1=out_spisok[0][1], out_calls1=out_spisok[0][0], out_name2=out_spisok[1][1], out_calls2=out_spisok[1][0], out_name3=out_spisok[2][1], out_calls3=out_spisok[2][0], working_day=working_day)

@app.route('/calls_all')
def calls_all():
    uuid = request.args.get('login1')
    if uuid[0] !='c':
        uuid = corebo + uuid[6:]
    login = connection1.execute("select login from mv_employee where uuid = '{0}'".format(uuid))
    for i in login:
        login = i[0]
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
    outcalls_month = connection1.execute("select count(*) from mv_phone_call, mv_employee where operatortitle = title and direction"
                                         " = 'Outbound' and login = '{0}' and mv_phone_call.creationdate >= '2019-0{1}-01'::date and"
                                         " mv_phone_call.creationdate <'2019-0{1}-30'::date;".format(login, mon))
    for i in outcalls_month:
        outcalls_month = i[0]
    calls_all = {"calls_month": calls_month, "calls_today": calls_today, "calls_yest": calls_yest,
                 "outcalls_today": outcalls_today, "outcalls_yest": outcalls_yest, "outcalls_month": outcalls_month}
    calls_all = json.dumps(calls_all, ensure_ascii=False)

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

    out_spisok = [(' ', 'Пусто') for i in range(3)]
    out_top = connection1.execute("with vspom as (select operatortitle, Sum(Case When direction = 'Outbound' Then 1 Else 0 End) as direction From mv_phone_call where dstphonenumber != '1234' and direction = 'Outbound' and creationdate >= '{0}'::date and creationdate <'{0}'::date+1 group by operatortitle) select direction, operatortitle from vspom order by direction desc, operatortitle".format(dataa))

    if isinstance(out_top, sqlalchemy.engine.result.ResultProxy): #new
         print("пустой список лидеров")
    else:  #end new
       for i, v in enumerate(out_top):
          if i < 3:
              out_spisok[i] = v
              surname_name = out_spisok[i][1].split()
              del surname_name[-1]
              surname_name = surname_name[1] + ' ' + surname_name[0]
              out_spisok[i] = (out_spisok[i][0], surname_name)
          else:
              break

    top1 = {"name1": spisok[0][1], "calls1": spisok[0][0], "name2": spisok[1][1], "calls2": spisok[1][0], "name3": spisok[2][1], "calls3": spisok[2][0], "out_name1": out_spisok[0][1], "out_calls1": out_spisok[0][0], "out_name2": out_spisok[1][1], "out_calls2": out_spisok[1][0], "out_name3": out_spisok[2][1], "out_calls3": out_spisok[2][0]}
    top1 = json.dumps(top1, ensure_ascii=False)

    return top1



if __name__ == "__main__":
    app.run(treding = True)