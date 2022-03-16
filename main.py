from flask import Flask,render_template,flash
from flask.helpers import url_for
from forms import bill_pay, contact,singin,transfer_pay,register
from werkzeug import redirect, security,secure_filename
from flask_sqlalchemy import SQLAlchemy
# from sqlalchemy.sql import text
from flask_migrate import Migrate
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import redirect
from flask_login import LoginManager, login_user, logout_user,current_user,UserMixin,login_required
import random
app= Flask(__name__,template_folder='templates')
# DATABASE STUFF
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///bank.db'
app.config['SECRET_KEY'] = "princeofDevils!!"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db=SQLAlchemy(app)
migrate=Migrate(app, db)
## LOGIN SETUP
login_manager=LoginManager()
login_manager.init_app(app)
@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(user_id)
### DB CLASSes
class Users(db.Model,UserMixin):
    id = db.Column(db.Integer,primary_key=True)
    f_name = db.Column(db.String(200),nullable=False)
    l_name = db.Column(db.String(200),nullable=False)
    email = db.Column(db.String(200),nullable=False,unique=True)
    password = db.Column(db.String(200),nullable=False)
    date_added = db.Column(db.DateTime,default=datetime.utcnow)
    mbal = db.Column(db.Integer,nullable=False,unique=False)
    ipal = db.Column(db.Integer,nullable=False,unique=False)
    cpal = db.Column(db.Integer,nullable=False,unique=False)
    account_no=db.Column(db.String(200),nullable=False,unique=True)
    credit_no=db.Column(db.String(200),nullable=False,unique=True)
    bills=db.relationship('Bill',backref='trans')
    def __repr__(self):
        return '<email%r>' % self.email
class Bill(db.Model,UserMixin):
    id = db.Column(db.Integer,primary_key=True)
    sender=db.Column(db.Integer,db.ForeignKey('users.id'))
    name = db.Column(db.String(200),nullable=False)
    amount= db.Column(db.Integer,nullable=False)
    refence_number= db.Column(db.Integer,nullable=False)
    date_added = db.Column(db.DateTime,default=datetime.utcnow)
class Account(db.Model,UserMixin):
    id = db.Column(db.Integer,primary_key=True)
    sender=db.Column(db.Integer,db.ForeignKey('users.id'))
    name = db.Column(db.String(200),nullable=False)
    amount= db.Column(db.Integer,nullable=False)
    refence_number= db.Column(db.Integer,nullable=False)
    date_added = db.Column(db.DateTime,default=datetime.utcnow)
class Trans(db.Model,UserMixin):
    id = db.Column(db.Integer,primary_key=True)
    sender=db.Column(db.Integer,db.ForeignKey('users.id'))
    name = db.Column(db.String(200),nullable=False)
    amount= db.Column(db.Integer,nullable=False)
    refence_number= db.Column(db.Integer,nullable=False)
    date_added = db.Column(db.DateTime,default=datetime.utcnow)
class Main(db.Model,UserMixin):
    id = db.Column(db.Integer,primary_key=True)
    sender=db.Column(db.Integer,db.ForeignKey('users.id'))
    name = db.Column(db.String(200),nullable=False)
    amount= db.Column(db.Integer,nullable=False)
    refernce_num= db.Column(db.Integer,nullable=False)
    date_added = db.Column(db.DateTime,default=datetime.utcnow)
class Credit(db.Model,UserMixin):
    id = db.Column(db.Integer,primary_key=True)
    sender = db.Column(db.Integer,db.ForeignKey('users.id'))
    account_no=db.Column(db.Integer,nullable=False)
    credit_no = db.Column(db.String(200),nullable=False)
    amount= db.Column(db.Integer,nullable=False)
    refernce_num= db.Column(db.Integer,nullable=False)
    date_added = db.Column(db.DateTime,default=datetime.utcnow)
def gen_balance():
    final_num=""
    n_list=[6,7]
    num_list=[1,2,3,4,5,6,7,8,9,0]
    n=random.choice(n_list)
    if n==6:
        for i in num_list:
            a = [2,3,1]
            b=i+random.choice(a)
            if len(str(final_num))<n:
                final_num= eval(f"{final_num}{b}")
    else:
        for i in num_list:
            a = [2,1,3,]
            b=i+random.choice(a)
            if len(str(final_num))<n:
                final_num= eval(f"{final_num}{b}")
    
    return final_num
def gen_invest_bal():
    num_list=[1,2,3,4,5,6,7,8,9,0]
    i_num=""
    i_list=5
    for i in num_list:
        a =[1,3,2]
        b = i+random.choice(a)
        if len(str(i_num))<i_list:
            i_num=eval(f'{i_num}{b}')
    return i_num
def gen_credit_bal():
    num_list=[1,2,3,4,5,6,7,8,9,0]
    c_num=""
    c_list=5
    for i in num_list:
        a =[1,3,2]
        b = i+random.choice(a)
        if len(str(c_num))<c_list:
            c_num=eval(f'{c_num}{b}')
    return c_num
def gen_ref_num():
    num_list=[1,2,3,4,5,6,7,8,9,0]
    c_num=""
    c_list=5
    for i in num_list:
        a =[1,3,2]
        b = i+random.choice(a)
        if len(str(c_num))<c_list:
            c_num=eval(f'{c_num}{b}')
    return c_num
def gen_acc_num():
    num_list=[1,2,3,4,5,6,7,8,9,0]
    c_num=""
    c_list=14
    for i in num_list:
        a =[1,3,2]
        b = i+random.choice(a)
        if len(str(c_num))<c_list:
            c_num=eval(f'{c_num}{b}')
    return c_num

@app.route('/',methods=['GET','POST'])
def index():
    form=register()
    if form.validate_on_submit():
        user_email = Users.query.filter_by(email=form.email.data).first()
        if user_email is None:
            phas = generate_password_hash(form.password.data)
            add_user= Users(f_name=form.fname.data,l_name=form.lname.data,email=form.email.data,password=phas,mbal=gen_balance(),ipal=gen_invest_bal(),cpal=gen_credit_bal(),account_no=gen_acc_num(),credit_no=gen_acc_num())
            db.session.add(add_user)
            db.session.commit()
            user=Users.query.filter_by(email=form.email.data).first()
            login_user(user)
        else:
            form.fname.data=form.fname.data
            form.lname.data=form.lname.data
            form.email.data=form.email.data
            form.password.data=form.password.data   
        user=Users.query.filter_by(email=form.email.data).first()
        return redirect(url_for('home',user=user))
    return render_template('register.html',form=form)
@app.route('/login', methods=['GET','POST'])
def sigin():
    form=singin()
    if form.validate_on_submit():
        user = Users.query.filter_by(email=form.email.data).first()
        if user:
            login_user(user)
            return redirect(url_for('home',user=user))
        else:
            flash("User Doesn't exist")
            return redirect(url_for('sigin'))
    return render_template('index.html', form=form)
@app.route('/home',methods=['GET'])
@login_required
def home():
    user=current_user
    return render_template("home.html",user=user)
@app.route('/bill',methods=['GET','POST'])
@login_required
def bill():
    form=bill_pay()
    if form.validate_on_submit():
        if current_user.mbal >= form.amount.data:
            refernce=gen_ref_num()
            add_bill = Bill(sender=current_user.id,name=form.name.data,amount=form.amount.data,refence_number=refernce)
            add_account = Account(sender=current_user.id,name=form.name.data,amount=form.amount.data,refence_number=refernce)
            db.session.add(add_bill)
            db.session.commit()
            db.session.add(add_account)
            db.session.commit()
            mbal=current_user.mbal - form.amount.data   
            user = Users.query.get_or_404(current_user.id)
            user.mbal=mbal
            db.session.add(user)
            db.session.commit()
            flash('Bill Payment Successfull')
            form.name.data=""
            form.amount.data=""
        else:
            fail=0
            form.name.data=form.name.data
            form.amount.data=form.amount.data
            flash('Bill Payment Failed')
            redirect(url_for('bill',fail=fail))
    return render_template("bill.html",form=form)

@app.route('/transfer',methods=['GET','POST'])
@login_required
def transfer():
    form=transfer_pay()
    user = Users.query.get_or_404(current_user.id)
    if form.validate_on_submit():
        if current_user.mbal >= form.amount.data:
            refernce=gen_ref_num()
            add_bill = Trans(sender=form.withdraw.data,name=form.to.data,amount=form.amount.data,refence_number=refernce)
            add_account= Account(sender=form.withdraw.data,name=form.to.data,amount=form.amount.data, refence_number=refernce)
            add_credit= Credit( sender = current_user.id,account_no=form.withdraw.data,credit_no=form.to.data,amount=form.amount.data, refernce_num=refernce)
            db.session.add(add_bill)
            db.session.commit()
            db.session.add(add_account)
            db.session.commit()
            db.session.add(add_credit)
            db.session.commit()
            mbal=current_user.mbal - form.amount.data   
            cpal=current_user.cpal - form.amount.data   
            user.mbal=mbal
            user.cpal=cpal
            db.session.add(user)
            db.session.commit()
            flash('Transfer Successfull')
            form.withdraw.data=""
            form.amount.data=""
            form.to.data=""
        else:
            fail=0
            form.withdraw.data=""
            form.amount.data=""
            form.to.data=""
            flash('Transfer Failed')
            redirect(url_for('transfer.html',fail=fail))
    return render_template("transfer.html",form=form,user=user)

@app.route('/bill/histroy',methods=['GET'])
@login_required
def phistory():
    user= Users.query.get_or_404(current_user.id)
    histroy= Bill.query.filter_by(sender=user.id)
    return render_template("p-history.html",histroy=histroy,current_user=current_user)
@app.route('/account/histroy',methods=['GET'])
@login_required
def ahistory():
    user= Users.query.get_or_404(current_user.id)
    histroy= Account.query.filter_by(sender=user.id)
    return render_template("a-history.html",histroy=histroy,current_user=current_user)
@app.route('/account/credit',methods=['GET'])
@login_required
def cr_history():
    user= Users.query.get_or_404(current_user.id)
    histroy= Credit.query.filter_by(sender=user.id)
    return render_template("cr_histroy.html",histroy=histroy,current_user=current_user)
@app.route('/contact',methods=['GET',"POST"])
@login_required
def contact_us():
    form=contact()
    if form.validate_on_submit():
        flash('Report Submitted')
        redirect(url_for('contact_us'))
    form.fname.data=""
    form.lname.data=""
    form.p.data=""
    return render_template('contact.html',form=form)
@app.route('/thankyou')
def thankyou():
    return render_template("thanks.html")



# if __name__=='main':
#     app.run(debug=True)