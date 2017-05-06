from flask import Flask,render_template,redirect,url_for,request
from flask_login import LoginManager,login_required
from flask_login import login_user,logout_user,current_user
from dbhelper import DBHelper as DBhelper
from user import User
from passwordhelper import passHelper
from bitlyhelper import BitlyHelper
import datetime
import config
from forms import RegistrationForm,LoginForm,CreateTableForm
ph = passHelper()
DB = DBhelper()
BH = BitlyHelper()
app = Flask(__name__)
app.secret_key = 'cMlCVgyfbFYllvKDM5QzBc5en09yydjez+FcA3m55o02GeKZGWY3c6/z6AdBZHMUd7QErw2lKgUv2SXNk2Y2WM6156lmwCcYijs'
login_manager = LoginManager(app)
@app.route('/')
def home():
    return render_template("home.html",loginform=LoginForm(), registrationform=RegistrationForm())
@app.route("/account")
@login_required
def account():
    tables = DB.get_tables(current_user.get_id())
    return render_template("account.html",createtableform=CreateTableForm(), tables=tables)

@app.route("/login", methods=["POST"])
def login():
    form = LoginForm(request.form)
    if form.validate():
        stored_user = DB.get_user(form.loginemail.data)
        if stored_user and ph.validate_password(form.loginpassword.data,stored_user['salt'], stored_user['hashed']):
            user = User(form.loginemail.data)
            login_user(user, remember=True)
            return redirect(url_for('account'))
        form.loginemail.errors.append("Email or password invalid")
    return render_template("home.html", loginform=form,registrationform=RegistrationForm())
@login_manager.user_loader
def loaduser(user_id):
    user_password = DB.get_user(user_id)
    if user_password:
        return User(user_id)
@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))
@app.route("/register", methods=["POST"])
def register():
    form = RegistrationForm(request.form)
    if form.validate():
        if DB.get_user(form.email.data):
            form.email.errors.append("Email address already registered")
            return render_template('home.html',loginform=LoginForm(), registrationform=form)
        salt = ph.get_salt()
        hashed = ph.get_hash(form.password2.data + salt)
        DB.add_user(form.email.data, salt, hashed)
        return render_template("home.html", loginform=LoginForm(),registrationform=form,onloadmessage="Registration successful. Please log in.")
    return render_template("home.html", loginform=LoginForm(),registrationform=form)
@app.route("/account/createtable", methods=["POST"])
@login_required
def createtable():
    form = CreateTableForm(request.form)
    if form.validate():
        tableid = DB.add_table(form.tablenumber.data,current_user.get_id())
        new_url = config.base_url + "newrequest/" +str(tableid)
        DB.update_table(tableid, new_url)
        return redirect(url_for('account'))
    return render_template("account.html", createtableform=form,tables=DB.get_tables(current_user.get_id()))
@app.route('/account/deletetable')
def del_table():
    tableid = request.args.get('tableid')
    DB.delete_table(tableid)
    return redirect(url_for('account'))
@app.route("/newrequest/<tid>")
def new_request(tid):
    DB.add_request(tid, datetime.datetime.now())
    return "Your request has been logged and a waiter will be with you shortly"
@app.route("/dashboard")
@login_required
def dashboard():
    now = datetime.datetime.now()
    requests = DB.get_requests(current_user.get_id())
    print(requests)
    for req in requests:
        deltaseconds = (now - req['time']).seconds
        req['wait_minutes'] = "{}.{}".format((deltaseconds/60),str(deltaseconds % 60).zfill(2))
    return render_template("dashboard.html", requests=requests)
@app.route("/dashboard/resolve")
@login_required
def dashboard_resolve():
    request_id = request.args.get("request_id")
    DB.delete_request(request_id)
    return redirect(url_for('dashboard'))
if __name__ == '__main__':
    app.run(port=int('3000'),debug=True)