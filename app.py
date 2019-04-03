from flask import Flask
from flask import render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://naucrm:naucrm@192.168.200.199/naumendb'
app.debug = True
db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True)
    email = db.Column(db.String(120), unique=True)

    def __init__(self, username, email):
        self.username = username
        self.email = email

    def __repr__(self):
        return '<User %r>' % self.username

@app.route('/')
@app.route('/index')
def index():
    myUser = User.query.all()
    oneItem = User.query.filter_by(username='test2').firts()
    return render_template('add_user.html', myUser=myUser, oneItem=oneItem)
    ''' if request.args.get('username')==None:
        aq = 'Пользователь'
        sur = '!'
    else:
        if request.args.get('surname')==None:
            aq = request.args.get('username')
            sur = '!'
        else:
            aq = request.args.get('username')
            aw = request.args.get('surname')
            sur = {'surname': aw}
    user = {'username': aq} '''

    #return render_template('index.html', title='Home', user=user, sur=sur)


@app.route('/post_user', methods=['GET'])
def post_user():
    user = User(request.args.get('username'), request.args.get('surname'))
    db.session.add(user)
    db.session.commit()
    return redirect(url_for('index'))
if __name__ == "__main__":
    app.run()


