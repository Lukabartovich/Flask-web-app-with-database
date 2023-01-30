from flask import Flask, render_template, request
from flask.views import MethodView
from wtforms import Form, StringField, SubmitField

import sqlite3
from StringSort import StringSort

app = Flask('myapp')

class Checks:

    def __init__(self):
        self.connection = sqlite3.connect('names.db')
        self.cursor = self.connection.cursor()

    def update(self, name, password):

        self.connection.execute("""
            INSERT INTO "Names" VALUES
                (?, ?)
            """, [str(name), str(password)])

        self.connection.commit()

    def check(self, name, password):

        self.cursor.execute("""
            SELECT "password" FROM "Names" WHERE "name" = ?
        """, [name])

        password_real = self.cursor.fetchall()

        if password_real == []:
            return False
        else:
            s = StringSort(str(password_real))
            s = s.delete("[(',)]")
            if s == str(password):
                return True
            else:
                return False

class HomePage(MethodView):
    def get(self):
        return render_template('HomePage.html')

class LogIn(MethodView):
    def get(self):
        get = GetLog()
        return render_template('LogIn.html', form=get)

class SignIn(MethodView):
    def get(self):
        get = GetSign()
        return render_template('SignIn.html', form = get)

class SingResult(MethodView):
    def post(self):
        get_form = GetSign(request.form)
        if get_form.name.data != '' and get_form.password.data != '':
            self.db(get_form.name.data, get_form.password.data)
            self.name = get_form.name.data
            self.password = get_form.password.data

            return render_template('SingResult.html', name=self.name)
        else:
            get = GetSign()
            return render_template('SignIn.html', form = get)

    def db(self, name, password):
        c1 = Checks()
        c1.update(name, password)
        print('done')

class LogResult(MethodView):
    def post(self):
        get_form = GetSign(request.form)
        self.name = get_form.name.data
        self.password = get_form.password.data
        return render_template('LogResult.html', db = self.db())

    def db(self):
        c1 = Checks()
        output = c1.check(self.name, self.password)
        if output == True:
            return f'Hello {self.name}!'
        else:
            return 'Name or password are not correct!'

class GetSign(Form):

    name = StringField('name: ')
    password = StringField('password: ')

    button_commit = SubmitField('sign in')

class GetLog(Form):

    name = StringField('name: ')
    password = StringField('password: ')

    button_commit = SubmitField('log in')



app.add_url_rule('/', view_func=HomePage.as_view('home page'))
app.add_url_rule('/log_in', view_func=LogIn.as_view('log_in'))
app.add_url_rule('/sign_in', view_func=SignIn.as_view('sign_in'))
app.add_url_rule('/SingResult', view_func=SingResult.as_view('SingResult'))
app.add_url_rule('/LogResult', view_func=LogResult.as_view('LogResult'))

app.run(debug=True, host='0.0.0.0')