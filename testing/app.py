from glob import escape
from flask import Flask
 

app = Flask(__name__)

store = {'Ram':'He is very genuine and respectful','Ravi':'He is very bad and he usually dont respect others'}
 

@app.route('/')

def hello_world():
    return 'Hello World,it is working now'

@app.route('/about')

def about_world():
    return 'this is working fine and you can move further' 

@app.route('/user/<username>')

def show_user(username):
    return f'user{escape(username)}'

@app.route('/user/<string:username>')

def show_user(username):
    return f'user{escape(username)}'





# main driver function
if __name__ == '__main__':
 
    # run() method of Flask class runs the application
    # on the local development server.
    app.run(debug=True)