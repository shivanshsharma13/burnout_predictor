import sqlite3
import pandas as pd

db_file = "burnout.db"


def user_details(emp_id, men):
    conn = sqlite3.connect(db_file)
    cur = conn.cursor()
    query_1 = "SELECT Gender, company, WFH, Designation, Resource_Allocation FROM user WHERE emp_id='Shivansh Sharma';"

    n = cur.execute(query_1)
    n = cur.fetchall()
    lst = []
    details = pd.DataFrame()

    for i in (n):
        details['Gender'] = [i[0]]
        details['Company Type'] = [i[1]]
        details['WFH Setup Available'] = [i[2]]
        details['Designation'] = [i[3]]
        details['Resource Allocation'] = [i[4]]
        details['Mental Fatigue Score'] = [men]

    return details


# user_details("Shivansh Sharma")

    # X_train = details.drop(labels=["Employee ID", "Date of Joining"], axis=1)
    # X_train["Gender"].replace({'Female': 0, 'Male': 1}, inplace=True)
    # X_train["Company Type"].replace({'Service': 0, 'Product': 1}, inplace=True)
    # X_train["WFH Setup Available"].replace({'No': 0, 'Yes': 1}, inplace=True)
    # X_train["Mental Fatigue Score"] = n
