import sqlite3

db_file = "burnout.db"

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

    # print(type(emp_id))

    # if len(d)>=1:
    #     nam = cur.fetchall()[0][0]
    #     print(nam)
    #     if(nam == emp_id):
    #         return True
    #     else:
    #         return False
    # else:
    #     return False
    


print(check_user_db("nehalchutiya"))