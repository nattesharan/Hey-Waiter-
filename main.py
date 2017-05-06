from flask import Flask,render_template,redirect,url_for,request
from flask_login import LoginManager,login_required
from flask_login import login_user,logout_user,current_user
from mockdbhelper import MockDBHelper as DBhelper
from user import User
from passwordhelper import passHelper
from bitlyhelper import BitlyHelper
import config
ph = passHelper()
DB = DBhelper()
BH = BitlyHelper()
app = Flask(__name__)
app.secret_key = 'cMlCVgyfbFYllvKDM5QzBc5en09yydjez+FcA3m55o02GeKZGWY3c6/z6AdBZHMUd7QErw2lKgUv2SXNk2Y2WM6156lmwCcYijs'
login_manager = LoginManager(app)
@app.route('/')
def home():
    return render_template('home.html')
@app.route('/account')
@login_required
def account():
    tables = DB.get_tables(current_user.get_id())
    return render_template('account.html', tables = tables)
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
@login_required
def dashboard():
    return render_template('dashboard.html')
@app.route('/account/createtable', methods = ['POST'])
@login_required
def createtable():
    tablename = request.form['tablenumber']
    tableid = DB.add_table(tablename,current_user.get_id())
    new_url = config.base_url + "newrequest/" + tableid
    DB.update_table(tableid,new_url)
    return redirect(url_for('account'))
@app.route('/account/deletetable')
def del_table():
    tableid = request.args.get('tableid')
    DB.delete_table(tableid)
    return redirect(url_for('account'))
@app.route("/newrequest/<tid>")
def new_request(tid):
    DB.add_request(tid, datetime.datetime.now())
    return "Your request has been logged and a waiter will be with you shortly"
if __name__ == '__main__':
    app.run(port=int('3000'),debug=True)