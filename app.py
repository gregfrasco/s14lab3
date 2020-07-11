import random
from faker import Faker
from flask import Flask, render_template, request, redirect, url_for
from os import environ

from models.user import Db, User
from modules.userform import UserForm

fake = Faker()

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = "s14a-key"
Db.init_app(app)


@app.route('/')
def index():
    # Query all
    users = User.query.all()

    return render_template("index.html", users=users, userLen=len(users))


# @route /adduser - GET, POST
@app.route('/adduser', methods=['GET', 'POST'])
def addUser():
    form = UserForm()
    # If GET
    if request.method == 'GET':
        return render_template('adduser.html', form=form)
    # If POST
    else:
        if form.validate_on_submit():
            first_name = request.form['first_name']
            age = request.form['age']
            new_user = User(first_name=first_name, age=age)
            Db.session.add(new_user)
            Db.session.commit()
            return redirect(url_for('index'))
        else:
            return render_template('adduser.html', form=form)


# @route /user/edit/:id - GET, POST
@app.route('/user/edit/<id>', methods=['GET', 'POST'])
def editUser(id):
    # If GET
    if request.method == 'GET':
        user = User.query.get(id)
        return render_template('updateuser.html', user=user)
    # If POST
    else:
        first_name = request.json['first_name']
        age = request.json['age']

        user = User.query.get(id)
        Db.session.delete(user)
        user.first_name = first_name
        user.age = age
        Db.session.add(user)
        Db.session.commit()
        return redirect(url_for('index'))


# @route /adduser/<first_name>/<age>
@app.route('/adduser/<first_name>/<age>')
def addUserFromUrl(first_name, age):
    Db.session.add(User(first_name=first_name, age=age))
    Db.session.commit()
    return redirect(url_for('index'))


@app.route('/user/<id>', methods=['GET', 'POST'])
def getOrRemoveUser(id):
    if request.method == 'GET':
        user = User.query.get(id)
        return render_template('user.html', user=user)
    else:
        user = User.query.get(id)
        Db.session.delete(user)
        Db.session.commit()
        return redirect(url_for('index'))


@app.route('/mock/<num>')
def MockUsers(num):
    n = int(num)
    if n < 0:
        return "Number must be greater than zero"
    for _ in range(n):
        first_name = fake.name().split(' ')[0]
        age = random.randrange(18, 100, 1)
        new_user = User(first_name=first_name, age=age)
        Db.session.add(new_user)
        Db.session.commit()
    return redirect(url_for('index'))
