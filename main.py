from flask import Flask,render_template,redirect,url_for,request
from flask_login import LoginManager,login_required
from flask_login import login_user
from mockdbhelper import MockDBHelper as DBhelper
from user import User
DB = DBhelper()
app = Flask(__name__)
app.secret_key = 'cMlCVgyfbFYllvKDM5QzBc5en09yydjez+FcA3m55o02GeKZGWY3c6/z6AdBZHMUd7QErw2lKgUv2SXNk2Y2WM6156lmwCcYijs'
login_manager = LoginManager(app)
@app.route('/')
def home():
    return render_template('home.html')
@app.route('/account')
@login_required
def account():
    return 'You are logged in'
@app.route("/login", methods=["POST"])
def login():
    email = request.form.get("email")
    password = request.form.get("password")
    user_password = DB.get_user(email)
    if user_password and user_password == password:
        user = User(email)
        return redirect(url_for('account'))
    return home()
@login_manager.user_loader
def loaduser(user_id):
    user_password = DB.get_user(user_id)
    if user_password:
        return User(user_id)
if __name__ == '__main__':
    app.run(port=int('3000'),debug=True)