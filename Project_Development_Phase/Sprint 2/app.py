from glob import escape
import os
import pathlib
from flask import Flask, render_template, request, redirect, url_for, session, abort
import flask
from google_auth_oauthlib.flow import Flow
import ibm_db
import requests
import google.auth.transport.requests
from flask import Flask, session, abort, redirect, request
from google.oauth2 import id_token
from google_auth_oauthlib.flow import Flow
from pip._vendor import cachecontrol

import google.oauth2.credentials
import google_auth_oauthlib.flow
import googleapiclient.discovery


app = Flask(__name__)
app.secret_key = "vikramkrishna"
os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

#conn = ibm_db.connect("DATABASE=bludb;HOSTNAME=824dfd4d-99de-440d-9991-629c01b3832d.bs2io90l08kqb1od8lcg.databases.appdomain.cloud;PORT=30119;SECURITY=SSL;SSLServerCertificate=DigiCertGlobalRootCA.crt;UID=pss83307;PWD=Lab47l4rodOvB2WE",'','')
conn = ibm_db.connect("DATABASE=bludb;HOSTNAME=824dfd4d-99de-440d-9991-629c01b3832d.bs2io90l08kqb1od8lcg.databases.appdomain.cloud;PORT=30119;SECURITY=SSL;SSLServerCertificate=DigiCertGlobalRootCA.crt;UID=pss83307;PWD=ZYca8KfFcZAQ3rTh",'','')

GOOGLE_CLIENT_ID = "490779147189-s4mbeeac083imr8qr7h1asrpavn36q30.apps.googleusercontent.com"
client_secrets_file = os.path.join(pathlib.Path(__file__).parent ,"client_secret.json")

flow = Flow.from_client_secrets_file(
    # 'C:\\Users\\vikik\\Desktop\\IBM-Project-18912-1659691292\\Project_Development_Phase\\Sprint_1\\client_secret.json',
    client_secrets_file=client_secrets_file,
    scopes=["https://www.googleapis.com/auth/userinfo.profile", "https://www.googleapis.com/auth/userinfo.email", "openid"],
    redirect_uri="http://127.0.0.1:5000/callback"
    )

def login_is_required(function):
    def wrapper(*args, **kwargs):
        if "google_id" not in session:
            return abort(401)  
        else:
            return function()
    return wrapper

@app.route("/login")
def login():
    authorization_url,state = flow.authorization_url()
    session["state"] = state 
    return redirect(authorization_url)

@app.route("/logout")
def logout():
    requests.session().cookies.clear()
    if 'credentials' in flask.session:
        del flask.session['credentials']
    session.clear()
    return redirect("/")

@app.route('/')
def index(): 
   return render_template('signin.html')

@app.route('/signin.html',methods = ['POST'])
def getUser():
    if request.method == 'POST':
        user = request.form['uname']
        password = request.form['upwd']
        sql = "SELECT * FROM CUSTOMERS where Email = ?"
        stmt = ibm_db.prepare(conn, sql)
        email = user
        # Explicitly bind parameters
        ibm_db.bind_param(stmt, 1,user)
        ibm_db.execute(stmt)
        dictionary = ibm_db.fetch_assoc(stmt)
        pwd = dictionary["PASSWORD"]
        if password != pwd:
            return render_template('error.html')
        return render_template('base.html')
    

@app.route('/signup.html')
def putUser():
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

        sql = "INSERT INTO customers (FirstName,LastName,Email,password,confirmpassword) VALUES(?,?,?,?,?);"
        stmt = ibm_db.prepare(conn, sql)
        ibm_db.bind_param(stmt, 1, fname)
        ibm_db.bind_param(stmt, 2, lname)
        ibm_db.bind_param(stmt, 3, mail)
        ibm_db.bind_param(stmt, 4, npwd)
        ibm_db.bind_param(stmt, 5, cpwd)
        ibm_db.execute(stmt)
    return render_template('signin.html')

@app.route("/protected_area")
@login_is_required
def protected_area():
    return f"Hello {session['name']}! <br/> <a href='/logout'><button>Logout</button></a>"


@app.route("/callback")
def callback():
    flow.fetch_token(authorization_response=request.url)

    if not flask.session['state'] == request.args['state']:
        abort(500)  # State does not match!

    credentials = flow.credentials
    request_session = requests.session() #request.authorized_session() #
    cached_session = cachecontrol.CacheControl(request_session)
    token_request = google.auth.transport.requests.Request(session=cached_session)

    id_info = id_token.verify_oauth2_token(   
        id_token=credentials._id_token,
        request=token_request, 
        audience=GOOGLE_CLIENT_ID
    )

    session["google_id"] = id_info.get("sub")
    session["name"] = id_info.get("name")
    return redirect("/protected_area")


if __name__ == '__main__':
 
    # run() method of Flask class runs the application
    # on the local development server.
    app.run(debug=True)


###########################################################################################
# from flask import Flask, render_template, url_for, redirect
# from authlib.integrations.flask_client import OAuth

# app = Flask(__name__)

# oauth = OAuth(app)

# app.config['SECRET_KEY'] = "THIS SHOULD BE SECRET"
# app.config['GOOGLE_CLIENT_ID'] = "490779147189-s4mbeeac083imr8qr7h1asrpavn36q30.apps.googleusercontent.com"
# app.config['GOOGLE_CLIENT_SECRET'] = "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"
# # app.config['GITHUB_CLIENT_ID'] = "<your github client id>"
# # app.config['GITHUB_CLIENT_SECRET'] = "<your github client secret>"

# def fetch_token(name, request):
#         token = OAuth2Token.find(
#             name=name,
#             user=request.user
#         )
#         return token.to_token()

# google = oauth.register(
#     name = 'google',
#     client_id = app.config["GOOGLE_CLIENT_ID"],
#     client_secret = app.config["GOOGLE_CLIENT_SECRET"],
#     access_token_url = 'https://accounts.google.com/o/oauth2/token',
#     access_token_params = None,
#     authorize_url = 'https://accounts.google.com/o/oauth2/auth',
#     authorize_params = None,
#     api_base_url = 'https://www.googleapis.com/oauth2/v1/',
#     userinfo_endpoint = 'https://openidconnect.googleapis.com/v1/userinfo',  # This is only needed if using openId to fetch user info
#     client_kwargs = {'scope': 'email profile'},
#     # fetch_token=fetch_token,
# )


# # github = oauth.register (
# #   name = 'github',
# #     client_id = app.config["GITHUB_CLIENT_ID"],
# #     client_secret = app.config["GITHUB_CLIENT_SECRET"],
# #     access_token_url = 'https://github.com/login/oauth/access_token',
# #     access_token_params = None,
# #     authorize_url = 'https://github.com/login/oauth/authorize',
# #     authorize_params = None,
# #     api_base_url = 'https://api.github.com/',
# #     client_kwargs = {'scope': 'user:email'},
# # )


# # Default route
# @app.route('/')
# def index():
#   return render_template('index.html')


# # Google login route
# @app.route('/login/google')
# def google_login():
#     google = oauth.create_client('google')
#     redirect_uri = url_for('google_authorize', _external=True)
#     return google.authorize_redirect(redirect_uri)


# # Google authorize route
# @app.route('/login/google/authorize')
# def google_authorize():
#     google = oauth.create_client('google')
#     token = google.authorize_access_token()
#     resp = google.get('userinfo').json()
#     print(f"\n{resp}\n")
#     return "You are successfully signed in using google"


# # Github login route
# # @app.route('/login/github')
# # def github_login():
# #     github = oauth.create_client('github')
# #     redirect_uri = url_for('github_authorize', _external=True)
# #     return github.authorize_redirect(redirect_uri)


# # Github authorize route
# # @app.route('/login/github/authorize')
# # def github_authorize():
# #     github = oauth.create_client('github')
# #     token = github.authorize_access_token()
# #     resp = github.get('user').json()
# #     print(f"\n{resp}\n")
# #     return "You are successfully signed in using github"


# if __name__ == '__main__':
#   app.run(debug=True)





#------------------------------------------------------------------------------------
#################################final#############################################

# from glob import escape
# from flask import Flask, render_template, request, redirect, url_for, session
# import ibm_db
# from flask import Flask, render_template, url_for, redirect
# from authlib.integrations.flask_client import OAuth
 

# app = Flask(__name__)
# #conn = ibm_db.connect("DATABASE=bludb;HOSTNAME=824dfd4d-99de-440d-9991-629c01b3832d.bs2io90l08kqb1od8lcg.databases.appdomain.cloud;PORT=30119;SECURITY=SSL;SSLServerCertificate=DigiCertGlobalRootCA.crt;UID=pss83307;PWD=Lab47l4rodOvB2WE",'','')
# conn = ibm_db.connect("DATABASE=bludb;HOSTNAME=824dfd4d-99de-440d-9991-629c01b3832d.bs2io90l08kqb1od8lcg.databases.appdomain.cloud;PORT=30119;SECURITY=SSL;SSLServerCertificate=DigiCertGlobalRootCA.crt;UID=pss83307;PWD=ZYca8KfFcZAQ3rTh",'','')



# oauth = OAuth(app)

# app.config['SECRET_KEY'] = "THIS SHOULD BE SECRET"
# app.config['GOOGLE_CLIENT_ID'] = "490779147189-s4mbeeac083imr8qr7h1asrpavn36q30.apps.googleusercontent.com"
# app.config['GOOGLE_CLIENT_SECRET'] = "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"


# google = oauth.register(
#     name = 'google',
#     client_id = app.config["GOOGLE_CLIENT_ID"],
#     client_secret = app.config["GOOGLE_CLIENT_SECRET"],
#     access_token_url = 'https://accounts.google.com/o/oauth2/token',
#     access_token_params = None,
#     authorize_url = 'https://accounts.google.com/o/oauth2/auth',
#     authorize_params = None,
#     api_base_url = 'https://www.googleapis.com/oauth2/v1/',
#     userinfo_endpoint = 'https://openidconnect.googleapis.com/v1/userinfo',  # This is only needed if using openId to fetch user info
#     client_kwargs = {'scope': 'email profile'},
# )


# # Google login route
# @app.route('/login/google')
# def google_login():
#     google = oauth.create_client('google')
#     redirect_uri = url_for('google_authorize', _external=True)
#     return google.authorize_redirect(redirect_uri)


# # Google authorize route
# @app.route('/login/google/authorize')     #in signin.html <a href="{{ url_for('google_login')}}"><p class="white"><b>Sign in with <img src="static/Images/golo.png" alt=" " width="50" height="50"></b></p></a>
# def google_authorize():
#     google = oauth.create_client('google')
#     token = google.authorize_access_token()
#     resp = google.get('userinfo').json()
#     print(f"\n{resp}\n")
#     return "You are successfully signed in using google"



# @app.route('/')
# def login():
#     return render_template('signin.html')

# @app.route('/signin.html',methods = ['POST'])
# def getUser():
#     if request.method == 'POST':
#         user = request.form['uname']
#         password = request.form['upwd']
#         sql = "SELECT * FROM CUSTOMERS where Email = ?"
#         stmt = ibm_db.prepare(conn, sql)
#         email = user
#         # Explicitly bind parameters
#         ibm_db.bind_param(stmt, 1,user)
#         ibm_db.execute(stmt)
#         dictionary = ibm_db.fetch_assoc(stmt)
#         pwd = dictionary["PASSWORD"]
#         if password != pwd:
#             return render_template('error.html')
#         return render_template('base.html')
    

# @app.route('/signup.html')
# def putUser():
#     return render_template('signup.html')   

# @app.route('/signup.html',methods = ['POST'])
# def storedUser():
#     if request.method == 'POST':
#         fname = request.form['fname']
#         lname = request.form['lname']
#         mail = request.form['mail']
#         npwd = request.form['npwd']
#         cpwd = request.form['cpwd']

#         res = fname + lname + mail + npwd + cpwd

#         if npwd != cpwd:
#             return render_template('signup.html')

#         sql = "INSERT INTO customers (FirstName,LastName,Email,password,confirmpassword) VALUES(?,?,?,?,?);"
#         stmt = ibm_db.prepare(conn, sql)
#         ibm_db.bind_param(stmt, 1, fname)
#         ibm_db.bind_param(stmt, 2, lname)
#         ibm_db.bind_param(stmt, 3, mail)
#         ibm_db.bind_param(stmt, 4, npwd)
#         ibm_db.bind_param(stmt, 5, cpwd)
#         ibm_db.execute(stmt)
#     return render_template('signin.html')


# if __name__ == '__main__':
 
#     # run() method of Flask class runs the application
#     # on the local development server.
#     app.run(debug=True)