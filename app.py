from flask import Flask, render_template, request, redirect, send_from_directory
import sqlite3
import os

app = Flask(__name__)

currentdirectory = os.path.dirname(os.path.abspath(__file__))
# conn = sqlite3.connect('database.db')
# conn.execute('CREATE TABLE items (name TEXT, price INT)')
APP_ROOT = os.path.dirname(os.path.abspath(__file__))


@app.route('/')
def Main():
    return render_template('Main.html')

@app.route('/Main')
def Main_():
    return render_template('Main.html')


########################################## Login/Sign_up #################
message_login = ''
message_signup = ''
email = ''
message_table = ''
message_vip = ''


def email__(email__):
    global email
    email = email__


@app.route('/Login', methods=['POST', 'GET'])
def Login():
    if request.method == 'POST':

        if request.form.get("login"):
            _reset_message_signup_()
            conn = sqlite3.connect('database.db')
            email = request.form["email"]
            email__(email)
            password = request.form["pswd"]
            if check_login_email(email) == 0 or check_login(email, password) == 0:
                error_login()
            else:
                _reset_message_login_()
                position = "SELECT D_P_A FROM Login WHERE email=? and pass=?"
                result = conn.execute(position, (email, password,)).fetchone()
                if result == ('Doctor',):
                    return Doctor()
                elif result == ('Admin',):
                    return Admin()
                elif result == ('Patient',):
                    return Patient_()
            return redirect('/Login')

        elif request.form.get("sign_up"):
            conn = sqlite3.connect('database.db')
            first_name = request.form["first_name"]
            last_name = request.form["last_name"]
            email = request.form["email_"]
            password = request.form["pswd_"]
            D_P = request.form["d_p"]
            status = 'Available'
            if check_login_email(email) == 1 or check_login(email, password) == 1:
                error_signup()
            else:
                _Success_message_signup_()
                cursor = conn.cursor()
                if D_P == 'Doctor':
                    x = '''INSERT INTO Login(first_name,last_name,email,pass,D_P_A,status) VALUES(?,?,?,?,?,?)'''
                    cursor.execute(x, (first_name, last_name, email, password, D_P, status,))
                if D_P == 'Patient':
                    x = '''INSERT INTO Login(first_name,last_name,email,pass,D_P_A) VALUES(?,?,?,?,?)'''
                    cursor.execute(x, (first_name, last_name, email, password, D_P,))
                conn.commit()
            return redirect('/Login')

    else:
        return render_template('Login.html', message=get_message_login(), message_=get_message_signup())


def get_email():
    global email
    return email


def get_message_signup():
    global message_signup
    return message_signup


def error_signup():
    global message_signup
    message_signup = 'Invalid input'


def _Success_message_signup_():
    global message_signup
    message_signup = 'Success'


def _reset_message_signup_():
    global message_signup
    message_signup = ''


def get_message_login():
    global message_login
    return message_login


def error_login():
    global message_login
    message_login = 'Invalid input'


def _reset_message_login_():
    global message_login
    message_login = ''


def check_login_email(email):
    conn = sqlite3.connect('database.db')
    x = "SELECT email FROM Login"
    x_ = conn.execute(x)
    for row in x_:
        if row == (email,):
            return 1
            break
    return 0


def check_login(email, pass_):
    conn = sqlite3.connect('database.db')
    x = "SELECT pass FROM Login WHERE email = ?"
    x_ = conn.execute(x, (email,))
    for row in x_:
        if row == (pass_,):
            return 1
            break
    return 0


@app.route('/upload00/<filename>')
def send_image(filename):
    return send_from_directory("Thumbnail", filename)


########################################## Admin #################
@app.route('/Admin')
def Admin():
    return render_template('Admin.html')


############################################### Sign_Up ################################
message_ = ''


@app.route('/New_Doctor', methods=['POST', 'GET'])
def New_Doctor():
    if request.method == 'POST':

        if request.form.get("Add"):
            first_name = request.form["first_name"]
            last_name = request.form["last_name"]
            email = request.form["email"]
            password = request.form["pass"]
            Doctor = 'Doctor'
            status = 'Available'
            if first_name == '' or last_name == '' or email == '' or password == '':
                _error_()
            else:
                reset__message__()
                conn = sqlite3.connect(currentdirectory + '\database.db')
                cursor = conn.cursor()
                x = '''INSERT INTO Login(first_name,last_name,email,pass,D_P_A,status) VALUES(?,?,?,?,?)'''
                cursor.execute(x, (first_name, last_name, email, password, Doctor, status,))
                conn.commit()
            return redirect('/New_Doctor')

        elif request.form.get("Delete"):
            first_name = request.form["first_name"]
            last_name = request.form["last_name"]
            email = request.form["email"]
            password = request.form["pass"]
            conn = sqlite3.connect('database.db')
            cursor = conn.cursor()
            if first_name == '' or last_name == '' or email == '' or password == '':
                _error_()
            else:
                reset__message__()
                delete = "DELETE FROM Login WHERE first_name=? and last_name=? and email=? and pass=?"
                # get_message_delete__(name, price_s, price_m, price_l)
                cursor.execute(delete, (first_name, last_name, email, password,))
                conn.commit()
            return redirect('/New_Doctor')

        elif request.form.get("Back"):
            reset__message__()
            return Admin()

    else:
        Doctor = 'Doctor'
        Patient = 'Patient'
        headings = ("First_Name", "Last_Name", "Email", "Password", "D/P")
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        x = "SELECT first_name,last_name,email,pass,D_P_A FROM Login WHERE D_P_A=? or D_P_A=?"
        result = cursor.execute(x, (Doctor,Patient,)).fetchall()
        return render_template('Admin-New_Doctor.html', headings=headings, data=result, message=_get_message_())


def _error_():
    global message_
    message_ = 'Invalid'


def reset__message__():
    global message_
    message_ = ''


def _get_message_():
    global message_
    return message_


########################################## Doctor #################
@app.route('/Doctor')
def Doctor():
    return render_template('Doctor.html')


########################################## Doctor_Profile #################
########################################## change pass doctor #################
message__ = ''


@app.route('/Doctor_P', methods=['POST', 'GET'])
def Doctor_P():
    if request.method == 'POST':

        if request.form.get("Change"):
            password = request.form["pass"]
            email_ = get_email()
            if password == '':
                _error__()
            else:
                reset__message___()
                conn = sqlite3.connect('database.db')
                cursor = conn.cursor()
                update = "UPDATE Login SET pass = ? WHERE email =?"
                cursor.execute(update, (password, email_,))
                conn.commit()
            return redirect('/Doctor_P')

        elif request.form.get("Back"):
            reset__message___()
            return Doctor()

    else:
        email_ = get_email()
        headings = ("First_Name", "Last_Name", "Email", "Password")
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        profile = "SELECT first_name,last_name,email,pass FROM Login WHERE email=?"
        result = cursor.execute(profile, (email_,)).fetchall()
        return render_template('Doctor_P.html', headings=headings, data=result, message=_get_message___())


def _error__():
    global message__
    message__ = 'Invalid'


def reset__message___():
    global message__
    message__ = ''


def _get_message___():
    global message__
    return message__


########################################## change f/l name doctor #################
message___ = ''


@app.route('/Doctor_F_L', methods=['POST', 'GET'])
def Doctor_F_L():
    if request.method == 'POST':

        if request.form.get("Change"):
            first_name = request.form["first_name"]
            last_name = request.form["last_name"]
            email_ = get_email()
            if first_name == '' or last_name == '':
                _error___()
            else:
                reset__message____()
                conn = sqlite3.connect('database.db')
                cursor = conn.cursor()
                update = "UPDATE Login SET first_name = ?, last_name = ? WHERE email =?"
                cursor.execute(update, (first_name, last_name, email_,))
                conn.commit()
            return redirect('/Doctor_F_L')

        elif request.form.get("Back"):
            reset__message____()
            return Doctor()

    else:
        email_ = get_email()
        headings = ("First_Name", "Last_Name", "Email", "Password")
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        profile = "SELECT first_name,last_name,email,pass FROM Login WHERE email=?"
        result = cursor.execute(profile, (email_,)).fetchall()
        return render_template('Doctor_F_L.html', headings=headings, data=result, message=_get_message____())


def _error___():
    global message___
    message___ = 'Invalid'


def reset__message____():
    global message___
    message___ = ''


def _get_message____():
    global message___
    return message___


########################################## change email doctor #################
message____ = ''
first = ''
last = ''
password = ''


def get_first():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    first = "SELECT first_name FROM Login WHERE email=?"
    result = cursor.execute(first, (get_email(),)).fetchone()
    return result[0]


def get_last():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    last = "SELECT last_name FROM Login WHERE email=?"
    result = cursor.execute(last, (get_email(),)).fetchone()
    return result[0]


def get_pass():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    password = "SELECT pass FROM Login WHERE email=?"
    result = cursor.execute(password, (get_email(),)).fetchone()
    return result[0]


@app.route('/Doctor_E', methods=['POST', 'GET'])
def Doctor_E():
    if request.method == 'POST':

        if request.form.get("Change"):
            email = request.form["email"]
            # old_email = get_email()
            first_name = get_first()
            last_name = get_last()
            password = get_pass()
            doctor = 'Doctor'
            if email == '':
                _error____()
            else:
                reset__message_____()
                conn = sqlite3.connect('database.db')
                cursor = conn.cursor()

                # update = "UPDATE Order_Doc SET email_d = ? WHERE email_d = ?"
                # cursor.execute(update, (email, old_email,))
                # conn.commit()

                update_ = "UPDATE Login SET email = ? WHERE first_name =? AND last_name =? AND pass = ? AND D_P_A = ?"
                cursor.execute(update_, (email, first_name, last_name, password, doctor,))
                email__(email)
                conn.commit()
            return redirect('/Doctor_E')

        elif request.form.get("Back"):
            reset__message_____()
            return Doctor()

    else:
        email_ = get_email()
        headings = ("First_Name", "Last_Name", "Email", "Password")
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        profile = "SELECT first_name,last_name,email,pass FROM Login WHERE email=?"
        result = cursor.execute(profile, (email_,)).fetchall()
        return render_template('Doctor_E.html', headings=headings, data=result, message=_get_message_____())


def _error____():
    global message____
    message____ = 'Invalid'


def reset__message_____():
    global message____
    message____ = ''


def _get_message_____():
    global message____
    return message____


########################################## Oredr #################
message_______ = ''


def get__first_():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    first = "SELECT first_name FROM Login WHERE email=?"
    result = cursor.execute(first, (get_email(),)).fetchone()
    return result[0]


def get__last_():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    last = "SELECT last_name FROM Login WHERE email=?"
    result = cursor.execute(last, (get_email(),)).fetchone()
    return result[0]


@app.route('/Order_Doc', methods=['POST', 'GET'])
def Order_Doc():
    if request.method == 'POST':

        if request.form.get("Done"):
            first_name = request.form["first_name"]
            last_name = request.form["last_name"]
            email = request.form["email"]
            doctor = 'Doctor'
            status = 'Available'
            status_ = 'Done'
            if first_name == '' or last_name == '' or email == '':
                ___error____()
            else:
                reset____message_____()
                conn = sqlite3.connect('database.db')
                cursor = conn.cursor()

                update = "UPDATE Login SET status = ? WHERE first_name =? AND last_name =? AND email =? AND D_P_A =?"
                cursor.execute(update, (status, get__first_(), get__last_(), get_email(), doctor,))
                conn.commit()

                update_ = "UPDATE Order_Doc SET status = ? WHERE first_name =? AND last_name =? AND email_p =?"
                cursor.execute(update_, (status_, first_name, last_name, email,))
                conn.commit()

                update__ = "UPDATE history SET status = ? WHERE first_name =? AND last_name =? AND email_p =?"
                cursor.execute(update__, (status_, get__first_(), get__last_(), email,))
                conn.commit()
            return redirect('/Order_Doc')

        elif request.form.get("Back"):
            reset____message_____()
            return Doctor()

    else:
        headings = ("First_Name", "Last_Name", "Email", "Status")
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        order = "SELECT first_name,last_name,email_p,status FROM Order_Doc"
        result = cursor.execute(order,).fetchall()
        return render_template('Order_Doc.html', headings=headings, data=result, message=__get__message_____())


def ___error____():
    global message_______
    message_______ = 'Invalid'


def reset____message_____():
    global message_______
    message_______ = ''


def __get__message_____():
    global message_______
    return message_______


########################################## Patient #################
@app.route('/Patient')
def Patient_():
    return render_template('Patient.html')


########################################## Patient_Profile #################
########################################## change pass Patient #################
__message__ = ''


@app.route('/Patient_P', methods=['POST', 'GET'])
def Patient_P():
    if request.method == 'POST':

        if request.form.get("Change"):
            password = request.form["pass"]
            email_ = get_email()
            if password == '':
                __error__()
            else:
                _reset__message___()
                conn = sqlite3.connect('database.db')
                cursor = conn.cursor()
                update = "UPDATE Login SET pass = ? WHERE email =?"
                cursor.execute(update, (password, email_,))
                conn.commit()
            return redirect('/Patient_P')

        elif request.form.get("Back"):
            _reset__message___()
            return Patient_()

    else:
        email_ = get_email()
        headings = ("First_Name", "Last_Name", "Email", "Password")
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        profile = "SELECT first_name,last_name,email,pass FROM Login WHERE email=?"
        result = cursor.execute(profile, (email_,)).fetchall()
        return render_template('Patient_P.html', headings=headings, data=result, message=__get_message___())


def __error__():
    global __message__
    __message__ = 'Invalid'


def _reset__message___():
    global __message__
    __message__ = ''


def __get_message___():
    global __message__
    return __message__


########################################## change f/l name Patient #################
___message___ = ''


@app.route('/Patient_F_L', methods=['POST', 'GET'])
def Patient_F_L():
    if request.method == 'POST':

        if request.form.get("Change"):
            first_name = request.form["first_name"]
            last_name = request.form["last_name"]
            email_ = get_email()
            Patient = 'Patient'
            if first_name == '' or last_name == '':
                _error___()
            else:
                reset__message____()
                conn = sqlite3.connect('database.db')
                cursor = conn.cursor()
                update = "UPDATE Login SET first_name = ?, last_name = ? WHERE email =? AND D_P_A =?"
                cursor.execute(update, (first_name, last_name, email_, Patient,))
                conn.commit()

                update = "UPDATE Order_Doc SET first_name = ?, last_name = ? WHERE email_p =?"
                cursor.execute(update, (first_name, last_name, email_,))
                conn.commit()

            return redirect('/Patient_F_L')

        elif request.form.get("Back"):
            reset__message____()
            return Patient_()

    else:
        email_ = get_email()
        headings = ("First_Name", "Last_Name", "Email", "Password")
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        profile = "SELECT first_name,last_name,email,pass FROM Login WHERE email=?"
        result = cursor.execute(profile, (email_,)).fetchall()
        return render_template('Patient_F_L.html', headings=headings, data=result, message=_get_message____())


def _error___():
    global ___message___
    ___message___ = 'Invalid'


def reset__message____():
    global message___
    message___ = ''


def _get_message____():
    global message___
    return message___


########################################## change email Patient #################
_____message____ = ''


def _get__first_():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    first = "SELECT first_name FROM Login WHERE email=?"
    result = cursor.execute(first, (get_email(),)).fetchone()
    return result[0]


def _get__last_():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    last = "SELECT last_name FROM Login WHERE email=?"
    result = cursor.execute(last, (get_email(),)).fetchone()
    return result[0]


def _get__pass_():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    password = "SELECT pass FROM Login WHERE email=?"
    result = cursor.execute(password, (get_email(),)).fetchone()
    return result[0]


@app.route('/Patient_E', methods=['POST', 'GET'])
def Patient_E():
    if request.method == 'POST':

        if request.form.get("Change"):
            email = request.form["email"]
            old_email = get_email()
            first_name = _get__first_()
            last_name = _get__last_()
            password = _get__pass_()
            Patient = 'Patient'
            if email == '':
                ____error____()
            else:
                ____reset__message_____()
                conn = sqlite3.connect('database.db')
                cursor = conn.cursor()

                update = "UPDATE Order_Doc SET email_p = ? WHERE email_p = ?"
                cursor.execute(update, (email, old_email,))
                conn.commit()

                update = "UPDATE history SET email_p = ? WHERE email_p = ?"
                cursor.execute(update, (email, old_email,))
                conn.commit()


                update_ = "UPDATE Login SET email = ? WHERE first_name =? AND last_name =? AND pass = ? AND D_P_A = ?"
                cursor.execute(update_, (email, first_name, last_name, password, Patient,))
                email__(email)
                conn.commit()
            return redirect('/Patient_E')

        elif request.form.get("Back"):
            ____reset__message_____()
            return Patient_()

    else:
        email_ = get_email()
        headings = ("First_Name", "Last_Name", "Email", "Password")
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        profile = "SELECT first_name,last_name,email,pass FROM Login WHERE email=?"
        result = cursor.execute(profile, (email_,)).fetchall()
        return render_template('Patient_E.html', headings=headings, data=result, message=_____get_message_____())


def ____error____():
    global _____message____
    _____message____ = 'Invalid'


def ____reset__message_____():
    global _____message____
    _____message____ = ''


def _____get_message_____():
    global _____message____
    return _____message____


########################################## Order_Doctor #################
message_____ = ''


def get_first_():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    first = "SELECT first_name FROM Login WHERE email=?"
    result = cursor.execute(first, (get_email(),)).fetchone()
    return result[0]


def get_last_():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    last = "SELECT last_name FROM Login WHERE email=?"
    result = cursor.execute(last, (get_email(),)).fetchone()
    return result[0]


@app.route('/Order_Doctor', methods=['POST', 'GET'])
def Order_Doctor():
    if request.method == 'POST':

        if request.form.get("Order"):
            first_name = request.form["first_name"]
            last_name = request.form["last_name"]
            email = request.form["email"]
            doctor = 'Doctor'
            status = 'Unavailable'
            status_ = 'In Progress'
            if first_name == '' or last_name == '' or email == '':
                __error____()
            else:
                reset___message_____()
                conn = sqlite3.connect('database.db')
                cursor = conn.cursor()

                update = "UPDATE Login SET status = ? WHERE first_name =? AND last_name =? AND email =? AND D_P_A =?"
                cursor.execute(update, (status, first_name, last_name, email, doctor,))
                conn.commit()

                x = '''INSERT INTO Order_Doc(first_name,last_name,email_p,status) VALUES(?,?,?,?)'''
                cursor.execute(x, (get_first_(), get_last_(), get_email(), status_,))
                conn.commit()

                y = '''INSERT INTO history(first_name,last_name,email_p,status) VALUES(?,?,?,?)'''
                cursor.execute(y, (first_name, last_name, get_email(), status_,))
                conn.commit()
            return redirect('/Order_Doctor')

        elif request.form.get("Back"):
            reset__message_____()
            return Patient_()

    else:
        status = 'Available'
        doctor = 'Doctor'
        headings = ("First_Name", "Last_Name", "Email")
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        order = "SELECT first_name,last_name,email FROM Login WHERE D_P_A=? AND status=?"
        result = cursor.execute(order, (doctor, status,)).fetchall()
        return render_template('Order_Doctor_P.html', headings=headings, data=result, message=_get__message_____())


def __error____():
    global message_____
    message_____ = 'Invalid'


def reset___message_____():
    global message_____
    message_____ = ''


def _get__message_____():
    global message_____
    return message_____


########################################## Oredrs_History #################
@app.route('/Orders_History', methods=['POST','GET'])
def Orders_History():
    if request.method == 'POST':

        if request.form.get("Back"):
            return Patient_()

    else:
        headings = ("First_Name", "Last_Name", "status")
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        order = "SELECT first_name,last_name,status FROM history WHERE email_p =?"
        result = cursor.execute(order, (get_email(),)).fetchall()
        return render_template('Orders_History_P.html', headings=headings, data=result)

if __name__ == '__main__':
    app.run()
