from flask import Flask,render_template,redirect,url_for,request
from flask_login import LoginManager,login_required
from flask_login import login_user,logout_user,current_user
from mockdbhelper import MockDBHelper as DBhelper
from user import User
from passwordhelper import passHelper
from bitlyhelper import BitlyHelper
import datetime
import config
from forms import RegistrationForm
ph = passHelper()
DB = DBhelper()
BH = BitlyHelper()
app = Flask(__name__)
app.secret_key = 'cMlCVgyfbFYllvKDM5QzBc5en09yydjez+FcA3m55o02GeKZGWY3c6/z6AdBZHMUd7QErw2lKgUv2SXNk2Y2WM6156lmwCcYijs'
login_manager = LoginManager(app)
@app.route('/')
def home():
    registrationform = RegistrationForm()
    return render_template('home.html',registrationform=registrationform)
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
@app.route("/register", methods=["POST"])
def register():
    form = RegistrationForm(request.form)
    if form.validate():
        if DB.get_user(form.email.data):
            form.email.errors.append("Email address already registered")
            return render_template('home.html', registrationform=form)
        salt = PH.get_salt()
        hashed = PH.get_hash(form.password2.data + salt)
        DB.add_user(form.email.data, salt, hashed)
        return redirect(url_for("home"))
    return render_template("home.html", registrationform=form)
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