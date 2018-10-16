from flask import Flask, render_template, request, redirect, session
app = Flask(__name__)
app.secret_key = 'ThisIsSecret'
app.count = 0
@app.route('/')
def index():
    session['count'] += 1
    return render_template('index.html', count=session['count'])
@app.route('/increment', methods=['POST'])
def two_increment():
    session['count'] += 1
    return redirect('/')
@app.route('/clear', methods=['POST'])
def clear():
    session['count'] = 0
    return redirect('/')
app.run(debug=True)