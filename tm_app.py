#!/usr/bin/env python3

from flask import Flask, request, make_response, render_template, session, redirect, url_for
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

app = Flask(__name__)
app.config['SECRET_KEY']="alicewasbeginning"

class NameForm(FlaskForm):
    name = StringField("Name: ", validators=[DataRequired()])
    submit = SubmitField("Go")

@app.route('/bad')
def bad():
    user_agent = request.headers.get('User-Agent')
    return "Your browser is %s" % user_agent

@app.route('/', methods=['GET','POST'])
def index():
    name = None
    form = NameForm()
    if form.validate_on_submit():
        session['name'] = form.name.data
        return redirect(url_for('bad'))
    return render_template('index.html', form=form, name=session.get('name'))

@app.route('/user/<name>')
def user(name):
    return render_template("user.html", name = name)

if __name__ == '__main__':
    app.run(debug=True)