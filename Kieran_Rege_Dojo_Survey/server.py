from flask import Flask, render_template, request, redirect, session, flash, url_for
import re
from datetime import datetime, date, time
emailRegex=re.compile(r'^[a-zA-Z0-9\.\+_-]+@[a-zA-Z0-9\._-]+\.[a-zA-Z]*$')
passwordRegex=re.compile(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d).+$')
app=Flask(__name__)
app.secret_key='662687b7b24bd888107908d02db45278'
def validate():
    errors=0
    if request.form['firstName']=='':
        flash('Name cannot be blank', 'firstNameError')
        errors+=1
        pass
    elif any(char.isdigit() for char in request.form['firstName'])==True:
        flash('Name cannot have numbers', 'firstNameError')
        errors+=1
        pass
    else:
        session['firstName']=request.form['firstName']
    if request.form['lastName']=='':
        flash('Name cannot be blank', 'lastNameError')
        errors+=1
        pass
    elif any(char.isdigit() for char in request.form['lastName'])==True:
        flash('Name cannot have numbers', 'lastNameError')
        errors+=1
        pass
    else:
        session['lastName']=request.form['lastName']
    if request.form['birthdate']=='':
        flash('Please pick a birthday', 'dateError')
        errors+=1
        pass
    else:
        session['birthdate']=request.form['birthdate']
        now=datetime.now()
        birthDate=datetime.strptime(session['birthdate'], "%Y-%m-%d")
        if now>birthDate:
            pass
        else:
            errors+=1
            flash('Birthdate must be in the past', 'dateError')
    if request.form['email']=='':
        flash('Email cannot be blank', 'emailError')
        errors+=1
        pass
    elif not emailRegex.match(request.form['email']):
        flash('Invalid email address', 'emailError')
        errors+=1
        pass
    else:
        session['email']=request.form['email']
    if request.form['password']=='':
        flash('Password cannot be blank', 'passwordError')
        errors+=1
        pass
    elif len(request.form['password'])<8:
        flash('Password must be greater than 8 characters', 'passwordError')
        errors+=1
        pass
    elif not passwordRegex.match(request.form['password']):
        flash('Password must contain at least one lowercase letter, one uppercase letter, and one digit', 'passwordError')
    else:
        session['password']=request.form['password']
    if request.form['confirmPassword']=='':
        flash('Please confirm password', 'confirmPasswordError')
        errors+=1
        pass
    elif request.form['confirmPassword']!=request.form['password']:
        flash('Passwords do not match', 'confirmPasswordError')
        errors+=1
    else:
        session['confirmPassword']=request.form['confirmPassword']
    if errors>0:
        session['password']=''
        session['confirmPassword']= ''
        return False
    else:
        return True
@app.route('/')
def index():
    if session['firstName']==None:
        session['firstName']=''
    if session['lastName']==None:
        session['lastName']=''
    if session['birthdate']==None:
        session['birthdate']=''
    if session['email']==None:
        session['email']=''
    if session['password']==None:
        session['password']=''
    if session['confirmPassword']==None:
        session['confirmPassword']=''
    return render_template('index.html')
@app.route('/create', methods=['POST'])
def create_user():
    if validate()==False:
        return redirect('/')
    return redirect('/process')
@app.route('/process')
def show_user():
    return render_template('results.html')
@app.route('/clear', methods=['POST'])
def clear():
    session['firstName']=''
    session['lastName']=''
    session['birthdate']=''
    session['email']=''
    session['password']=''
    session['confirmPassword']=''
    return redirect('/')
app.run(debug=True)