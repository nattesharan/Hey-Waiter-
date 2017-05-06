from flask import Flask,render_template,redirect,url_for,request
from flask_login import LoginManager,login_required
from flask_login import login_user,logout_user
from mockdbhelper import MockDBHelper as DBhelper
from user import User
from passwordhelper import passHelper
ph = passHelper()
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
    return render_template('account.html')
@app.route("/login", methods=["POST"])
def login():
    email = request.form.get("email")
    password = request.form.get("password")
    stored_user = DB.get_user(email)
    if stored_user and ph.validate_password(password,stored_user['salt'],stored_user['hashed']):
        user = User(email)
        login_user(user, remember = True)
        return redirect(url_for('account'))
    return home()
@login_manager.user_loader
def loaduser(user_id):
    user_password = DB.get_user(user_id)
    if user_password:
        return User(user_id)
@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))
@app.route('/register',methods = ['POST'])
def register():
    email = request.form['email']
    passwd = request.form['password']
    passwd1 = request.form['password2']
    if not passwd == passwd1:
        return redirect(url_for('home'))
    if DB.get_user(email):
        return redirect(url_for('home'))
    salt = ph.get_salt()
    hashed = ph.get_hash(passwd + salt)
    DB.add_user(email,salt,hashed)
    return redirect(url_for('home'))
@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')
if __name__ == '__main__':
    app.run(port=int('3000'),debug=True)