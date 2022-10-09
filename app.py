#------------------------------------------ Importing Modules ----------------------------------------------------

from flask import Flask
from flask import request,render_template,redirect,url_for

from flask_sqlalchemy import SQLAlchemy


#----------------------------------------- App initialization ----------------------------------------------------

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///exam_app_database.sqlite3"
db=SQLAlchemy()
db.init_app(app)
app.app_context().push()

#---------------------------------------------- Database ---------------------------------------------------------

class Questions(db.Model):
    __tablename___="questions"
    QID=db.Column(db.Integer,primary_key=True,nullable=False,autoincrement=True,unique=True)
    question=db.Column(db.String,nullable=False,unique=True)
    appear_year=db.Column(db.String,nullable=False)
    frequency=db.Column(db.Integer,nullable=False)

class Answers(db.Model):
    __tablename___="answers"
    AID=db.Column(db.Integer,primary_key=True,nullable=False,autoincrement=True,unique=True)
    answer=db.Column(db.String,nullable=False)


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
    ""

#*********************************************** User_Homepage ********************************************************
@app.route("/<username>/user_homepage",methods=["GET","POST"])
def user_homepage(username):
    ""

#*********************************************** List_Edit ********************************************************
@app.route("/<username>/<list_name>/edit",methods=["GET","POST"])
def edit_list(username,list_name):
    if request.method=="GET":
        return render_template("list_edit.html",username=username)

#*********************************************** List_Delete ********************************************************
@app.route("/<username>/<list_name>/delete",methods=["GET","POST"])
def delete_list(username,list_name):
    ""

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
    ""

#---------------------------------------------- App Run ---------------------------------------------------------

if __name__=="__main__":
    app.run(host="0.0.0.0",
            port=8080)


#================================================ END ============================================================