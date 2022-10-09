#------------------------------------------ Importing Modules ----------------------------------------------------

from flask import Flask
from flask import request,render_template,redirect,url_for

from flask_sqlalchemy import SQLAlchemy


#----------------------------------------- App initialization ----------------------------------------------------

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///app_database.sqlite3"
db=SQLAlchemy()
db.init_app(app)
app.app_context().push()

#---------------------------------------------- Database ---------------------------------------------------------

class List(db.Model):
    __tablename___="list"
    list_id=db.Column(db.Integer,primary_key=True,nullable=False,autoincrement=True,unique=True)
    list_name=db.Column(db.String,nullable=False,unique=True)
    list_desc=db.Column(db.String)
    list_created_date=db.Column(db.String,nullable=False)
    list_modified_date=db.Column(db.String)

class Card(db.Model):
    __tablename___="card"
    card_id=db.Column(db.Integer,primary_key=True,nullable=False,autoincrement=True,unique=True)
    card_created_date=db.Column(db.String,nullable=False)
    card_name=db.Column(db.String,nullable=False)
    card_desc=db.Column(db.String)
    card_deadline=db.Column(db.String,nullable=False)
    card_completed=db.Column(db.String,nullable=False)
    card_completed_date=db.Column(db.String)

class Member(db.Model):
    __tablename___="member"
    member_id=db.Column(db.Integer,primary_key=True,nullable=False,autoincrement=True,unique=True)
    member_username=db.Column(db.String,nullable=False,unique=True)
    member_password=db.Column(db.String,nullable=False)
    member_created_date=db.Column(db.String,nullable=False)

class Mem_list(db.Model):
    __tablename__="mem_list"
    mem_list_id=db.Column(db.Integer,primary_key=True,nullable=False,autoincrement=True,unique=True)
    member_id=db.Column(db.Integer,db.ForeignKey("member.member_id"),nullable=False)
    list_id=db.Column(db.Integer,db.ForeignKey("list.list_id"),nullable=False)

class List_card(db.Model):
    __tablename__="list_card"
    list_card_id=db.Column(db.Integer,primary_key=True,nullable=False,autoincrement=True,unique=True)
    card_id=db.Column(db.Integer,db.ForeignKey("card.card_id"),nullable=False)
    list_id=db.Column(db.Integer,db.ForeignKey("list.list_id"),nullable=False)

#--------------------------------------------- App Routes -------------------------------------------------------

#*********************************************** Index_Page ********************************************************
@app.route("/",methods=["GET"])
def homepage():
    return render_template("homepage.html")

#*********************************************** Signup_Page ********************************************************
@app.route("/signup",methods=["GET","POST"])
def signup_page():
    if request.method == "GET":
        return render_template("signup_page.html")
#*********************************************** Login_Page ********************************************************
@app.route("/login",methods=["GET","POST"])
def login_page():
    if request.method == "GET":
        return render_template("login_page.html")

#*********************************************** User_Summary ********************************************************
@app.route("/<username>/summary",methods=["GET","POST"])
def user_summary(username):
    user=Member.query.filter_by(member_username=username).first()

#*********************************************** User_Homepage ********************************************************
@app.route("/<username>/user_homepage",methods=["GET","POST"])
def user_homepage(username):
    user=Member.query.filter_by(member_username=username).first()

#*********************************************** List_Edit ********************************************************
@app.route("/<username>/<list_name>/edit",methods=["GET","POST"])
def edit_list(username,list_name):
    if request.method=="GET":
        lst=List.query.filter_by(list_name=list_name).first()
        return render_template("list_edit.html",username=username,list_name=lst.list_name,list_desc=lst.list_desc)

#*********************************************** List_Delete ********************************************************
@app.route("/<username>/<list_name>/delete",methods=["GET","POST"])
def delete_list(username,list_name):
    list=List.query.filter_by(list_name=list_name).first()

#*********************************************** List_Add ********************************************************
@app.route("/<username>/add_list",methods=["GET","POST"])
def add_list(username):
    if request.method=="GET":
        return redirect(url_for('user_homepage',username=username))

#*********************************************** Card_Add ********************************************************
@app.route("/<username>/<list_name>/add_card",methods=["GET","POST"])
def add_card(username,list_name):
    if request.method=="GET":
        new_lst=[]
        

#*********************************************** Card_Edit ********************************************************
@app.route("/<username>/<list_name>/<card_name>/edit",methods=["GET","POST"])
def edit_card(username,list_name,card_name):
    if request.method=="GET":
        new_lst=[]

#*********************************************** Card_Delete ********************************************************
@app.route("/<username>/<list_name>/<card_name>/delete")
def delete_card(username,list_name,card_name):
    card=Card.query.filter_by(card_name=card_name).first()

#---------------------------------------------- App Run ---------------------------------------------------------

if __name__=="__main__":
    app.run(host="0.0.0.0",
            port=8080)


#================================================ END ============================================================