from datetime import timedelta
from functools import update_wrapper
from flask import Flask, json, render_template, request, redirect, jsonify, request, make_response
from catboost import CatBoostRegressor
from flask.globals import current_app
from flask.helpers import make_response
from flask_sqlalchemy import SQLAlchemy
import sqlite3
from flask_cors import CORS
from Python_algo.support import user_details


import pandas as pd
import numpy as np
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///burnout.db'
db = SQLAlchemy(app)
CORS(app)

db_file = "burnout.db"


# Entry class for Db stuff
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    emp_id = db.Column(db.String(25), unique=True, nullable=False)
    date = db.Column(db.String(20), nullable=False)
    Gender = db.Column(db.String(6), nullable=False)
    company = db.Column(db.String(10), nullable=False)
    WFH = db.Column(db.String(10), nullable=False)
    Designation = db.Column(db.Float, nullable=False)
    Resource_Allocation = db.Column(db.Float, nullable=False)

    def __repr__(self):
        return f"User('{self.emp_id}', '{self.date}', '{self.Gender}', {self.Designation}, {self.Resource_Allocation})"


class bout(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    emp_id = db.Column(db.String(25), nullable=False)
    Burn = db.Column(db.Float, nullable=False)

    def __repr__(self):
        return f"User('{self.emp_id}', {self.fat})"


def check_user_db(emp_id):
    conn = sqlite3.connect(db_file)
    cur = conn.cursor()
    names = cur.execute(
        "SELECT emp_id FROM User WHERE emp_id='{emp_id}'".format(emp_id=emp_id))
    nam = names.fetchall()
    for i in nam:
        if(i[0] == emp_id):
            return True
        else:
            return False
 


from_file = CatBoostRegressor()
model = from_file.load_model("model.pkl")


@app.route('/')
def hello_world():
    return render_template("index.html")

@app.route('/error')
def error():
    return render_template("404.html")


@app.route('/login', methods=['POST'])
def signup():
    req = request.form 

    emp1 = str(req.get('employee_id'))
    Men = float(req.get('mental_fatigue'))
    print(emp1, Men)
    respo = "You are not a user, Please sign up"


    details = user_details(emp1, Men)
    burnout = model.predict(details)
    
    if (check_user_db(emp1)):
        try:
            entry = bout(emp_id=emp1, Burn=burnout)
            db.session.add(entry)
            db.session.commit()

            return str(burnout)
        except Exception as e:
            return str(burnout)
    else:
        return respo


@app.route('/submit', methods=['POST'])
def submit():
    if request.method == 'POST':

        emp = request.form['Employee Id']
        date_emp = (request.form['date'])
        Gender = int(request.form['Gender'])
        Com = int(request.form['Company type'])
        WFH = int(request.form['WFH'])
        Des = float(request.form['Designation'])
        Res = float(request.form['Resorce Allocation'])
      
        if (not check_user_db(emp)):
            if(Gender == 0):
                G="Female"
            else:
                G="Male"
            if Com == 0:
                c = "Service"
            else:
                c = "Product"
            if WFH == 0:
                w = "Not WFH"
            else:
                w = "WFH"
            # try:
            entry = User(emp_id=emp, date=date_emp, Gender=G, company=c,
                         WFH=w, Designation=Des, Resource_Allocation=Res)
            db.session.add(entry)
            db.session.commit()

            return redirect("/")
        

        else:
            return "You are already registered! Please login!!"





if __name__ == '__main__':
    app.run(debug=True)
