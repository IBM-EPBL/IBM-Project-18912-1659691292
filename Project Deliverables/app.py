# from glob import escape
from jinja2 import escape
from flask import Flask, render_template, request, redirect, url_for, session,flash,g
import ibm_db
from email.message import EmailMessage
import ssl
import smtplib
import random
from datetime import datetime
from time import sleep
import warnings
import requests
from dateparser import parse


app = Flask(__name__)
app.secret_key = "abc"
conn = ibm_db.connect("DATABASE=bludb;HOSTNAME=0c77d6f2-5da9-48a9-81f8-86b520b87518.bs2io90l08kqb1od8lcg.databases.appdomain.cloud;PORT=31198;SECURITY=SSL;SSLServerCertificate=DigiCertGlobalRootCA.crt;UID=fdx62360;PWD=4tPpQjJgI1zLFx6a",'','')

@app.route('/')
def login():
    return redirect('signin.html')

@app.route('/signin.html')
def render_page():
    session.pop("name",None)
    return render_template('signin.html')  

@app.route('/signin.html',methods = ['POST'])
def getUser():
    if request.method == 'POST':
        user = request.form['uname']
        password = request.form['upwd']
        session["name"] = user
        sql = "SELECT * FROM LOGIN where Email = ?"
        stmt = ibm_db.prepare(conn, sql)
        email = user
        # Explicitly bind parameters
        ibm_db.bind_param(stmt, 1,user)
        ibm_db.execute(stmt)
        dictionary = ibm_db.fetch_assoc(stmt)
        pwd = dictionary["PASSWORD"]
        if password != pwd:
            return render_template('error.html')
        return redirect('Main.html')
        # return redirect('Main.html')

@app.route('/Main.html')
def start_session():
    if g.name:
        return render_template('Main.html')
    return redirect('/')

@app.before_request
def before_request():
    g.name = None
    if 'name' in session:
        g.name = session['name']



@app.route('/signup.html')
def putUser():
        redirect('signup.html')
        return render_template('signup.html')   

@app.route('/signup.html',methods = ['POST'])
def storedUser():
    if request.method == 'POST':
        fname = request.form['fname']
        lname = request.form['lname']
        mail = request.form['mail']
        npwd = request.form['npwd']
        cpwd = request.form['cpwd']
        res = fname + lname + mail + npwd + cpwd
    

        if npwd != cpwd:
            return render_template('signup.html')

        sql = "INSERT INTO login(FirstName,LastName,Email,password) VALUES(?,?,?,?);"
        stmt = ibm_db.prepare(conn, sql)
        ibm_db.bind_param(stmt, 1, fname)
        ibm_db.bind_param(stmt, 2, lname)
        ibm_db.bind_param(stmt, 3, mail)
        ibm_db.bind_param(stmt, 4, npwd)
        ibm_db.execute(stmt)
    send_mail(mail,'signup',fname)
    return redirect('signin.html')


@app.route('/forpass.html')
def forpassfun():
    return render_template('forpass.html')


@app.route('/forpass.html',methods = ['POST'])
def changepwd():
    if request.method == 'POST':
        ename = request.form['ename']
        session['mail'] = ename
    return redirect('passotp.html')
    
    
@app.route('/passotp.html')
def getotp():
    recvmail = session.get('mail',None)
    codegen = send_mail(recvmail,'change','')
    session['codegen'] = int(codegen)
    return render_template('passotp.html')

@app.route('/passotp.html',methods = ['POST'])
def putotp():
    if request.method == 'POST':
        otp =int(request.form['otp'])

    codecheck = session.get('codegen',None)
    print(type(codecheck))
    print(type(otp))
    if codecheck == otp:
        return redirect('changepass.html')
    flash('please verify otp')
    return render_template('passotp.html')
@app.route('/changepass.html')
def changepass():
    redirect('changepass.html')
    return render_template('changepass.html')

@app.route('/changepass.html',methods = ['POST'])
def enterpass():
    if request.method == 'POST':
        npass = request.form['npass']
        cpass = request.form['cpass']

        if npass == cpass:
            uname = session.get('mail',None)
            sql = "UPDATE LOGIN SET password = ? where Email = ?;"
            stmt = ibm_db.prepare(conn, sql)
            ibm_db.bind_param(stmt, 1, cpass)
            ibm_db.bind_param(stmt, 2,uname )
            ibm_db.execute(stmt)
            return redirect('/') 
        else:
            flash('Please enter same passwords')
            return redirect('changepass.html')
    
@app.route('/logout')
def logout():
    session.pop("name",None)
    return redirect('/')

def send_mail(receiver,flag,firstname):
    email_sender = 'itouch.lmt@gmail.com'
    email_password = 'dbupsqdptwobniud'

    email_receiver = receiver

    code = random.randrange(100000,999999)

    if flag == 'signup':
        subject = 'signup confirmation'
        body = """
        Welcome """ + firstname + """ ,

        You have successfully created your account
        
        Enjoy surfing through the latest news!.. 
        """
        em = EmailMessage()
        em['From'] = email_sender
        em['To'] = email_receiver
        em['subject'] = subject
        em.set_content(body)

        context = ssl.create_default_context()

        with smtplib.SMTP_SSL('smtp.gmail.com',465,context = context) as smtp:
            smtp.login(email_sender,email_password)
            smtp.sendmail(email_sender,email_receiver,em.as_string())
    else:
        subject = 'Password change request'
        body = """
        Welcome """ + firstname + """ ,
        your password verification code for password change is: """+str(code)
        em = EmailMessage()
        em['From'] = email_sender
        em['To'] = email_receiver
        em['subject'] = subject
        em.set_content(body)

        context = ssl.create_default_context()

        with smtplib.SMTP_SSL('smtp.gmail.com',465,context = context) as smtp:
            smtp.login(email_sender,email_password)
            smtp.sendmail(email_sender,email_receiver,em.as_string())
        return code




if __name__ == '__main__':
    #run() method of Flask class runs the application
    #on the local development server.
    app.run(debug=True)