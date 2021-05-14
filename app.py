from flask import Flask, render_template, request, redirect
from catboost import CatBoostRegressor
from flask_sqlalchemy import SQLAlchemy
import sqlite3
from Python_algo.support import user_details

import pandas as pd
import numpy as np

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///burnout.db'
db = SQLAlchemy(app)

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


# @app.route('/train')
# def train_data():
#     return render_template("train_data.html")


# @app.route('/login')
# def login():
#     return render_template("login.html")


# l = []


@app.route('/login', methods=['POST'])
def signup():
    emp1 = str(request.form['Employee Id'])
    Men = float(request.form['Mental fatigue'])
    # l.append(emp1)

    details = user_details(emp1, Men)
    burnout = model.predict(details)
    
    if (check_user_db(emp1)):
        try:
            entry = bout(emp_id=emp1, Burn=burnout)
            db.session.add(entry)
            db.session.commit()
            return (f"Done successfully, your burnout rate is {burnout}, and commited the changes")
        except Exception as e:
            return (f"Done successfully, your burnout rate is {burnout}, and Updated changes")
    else:
        return "You are not a user, Please sign up"


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
        # Men = float(request.form['Mental fatigue'])
        # if check_user(emp, date_emp, Gender, Com, WFH, Des, Res):
        #  return redirect("/login")

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
            # except Exception as e:
            #     return "You are already Registered in Database\n Please login!!"
            # df = pd.DataFrame(
            #     np.array([[Gender, Com, WFH, Des, Res, Men]]),columns=['Gender','Company Type', 'WFH Setup Available', 'Designation', 'Resource Allocation', 'Mental Fatigue Score'])
            # # print(df)
            # burnout = str(model.predict(df))

        else:
            return "You are already registered! Please login!!"


# @app.route('/Mental', methods=['POST'])
# def mental():

    # l.append(Men)

    # conn = sqlite3.connect(db_file)
    # cur = conn.cursor()
    # query_1 = "SELECT emp_id FROM bout WHERE Fat={Men}".format(Men=Men)
    # n = cur.execute(query_1)
    # n = cur.fetchall()[0][0]

    # details = login_details(l[0])

    # X_train = details.drop(labels=["Employee ID", "Date of Joining"], axis=1)
    # X_train["Gender"].replace({'Female': 0, 'Male': 1}, inplace=True)
    # X_train["Company Type"].replace({'Service': 0, 'Product': 1}, inplace=True)
    # X_train["WFH Setup Available"].replace({'No': 0, 'Yes': 1}, inplace=True)
    # X_train["Mental Fatigue Score"] = n

    # burnout = str(model.predict(X_train))
    # print(burnout)

    # return "a"


if __name__ == '__main__':
    app.run(debug=True)
