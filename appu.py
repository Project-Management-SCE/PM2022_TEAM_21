from flask import Flask, render_template, request, redirect, url_for, flash
import sqlite3 as sql

app = Flask(__name__)


@app.route("/")
@app.route("/index")
def index():
    con = sql.connect("db_web.db")
    con.row_factory = sql.Row
    cur = con.cursor()
    cur.execute("select * from users")
    data = cur.fetchall()
    return render_template("index.html", datas=data)


@app.route("/Patient_R")
def Patient_R():
    con = sql.connect("db_web.db")
    con.row_factory = sql.Row
    cur = con.cursor()
    cur.execute("select * from users")
    data = cur.fetchall()
    return render_template("Patient_R.html", datas=data)


@app.route("/add_user", methods=['POST', 'GET'])
def add_user():
    if request.method == 'POST':
        uname = request.form['uname']
        contact = request.form['contact']
        con = sql.connect("db_web.db")
        cur = con.cursor()
        cur.execute("insert into users(UNAME,CONTACT) values (?,?)", (uname, contact))
        con.commit()
        flash('Appointment Added', 'success')
        return redirect(url_for("index"))
    return render_template("add_user.html")


@app.route("/edit_user/<string:uid>", methods=['POST', 'GET'])
def edit_user(uid):
    if request.method == 'POST':
        uname = request.form['uname']
        contact = request.form['contact']
        con = sql.connect("db_web.db")
        cur = con.cursor()
        cur.execute("update users set UNAME=?,CONTACT=? where UID=?", (uname, contact, uid))
        con.commit()
        flash('The Appointment Has Been Approved', 'success')
        return redirect(url_for("index"))
    con = sql.connect("db_web.db")
    con.row_factory = sql.Row
    cur = con.cursor()
    cur.execute("select * from users where UID=?", (uid,))
    data = cur.fetchone()
    return render_template("edit_user.html", datas=data)


@app.route("/delete_user/<string:uid>", methods=['GET'])
def delete_user(uid):
    con = sql.connect("db_web.db")
    cur = con.cursor()
    cur.execute("delete from users where UID=?", (uid,))
    con.commit()
    flash('Appointment Deleted', 'warning')
    return redirect(url_for("index"))



@app.route("/approval_user/<string:uid>", methods=['POST', 'GET'])
def approval_user(uid):
    if request.method == 'POST':
        uname = request.form['uname']
        contact = request.form['contact']
        con = sql.connect("db_web.db")
        cur = con.cursor()
        cur.execute("update users set UNAME=?,CONTACT=? where UID=?", (uname, contact, uid))
        con.commit()
        flash('The Appointment Has Been Sent and Waiting for Doctor Approval', 'success')
        return redirect(url_for("index"))
    con = sql.connect("db_web.db")
    con.row_factory = sql.Row
    cur = con.cursor()
    cur.execute("select * from users where UID=?", (uid,))
    data = cur.fetchone()
    return render_template("approval_user.html", datas=data)


if __name__ == '__main__':
    app.secret_key = 'admin123'
    app.run(debug=True)
