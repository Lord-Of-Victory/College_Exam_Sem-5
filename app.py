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
    subject=db.Column(db.String,nullable=False)
    frequency=db.Column(db.Integer,nullable=False)
    #answer=db.relationship("Answers",secondary="ques_ans_reln")

class Answers(db.Model):
    __tablename___="answers"
    AID=db.Column(db.Integer,primary_key=True,nullable=False,autoincrement=True,unique=True)
    answer=db.Column(db.String,nullable=False)
    #question=db.relationship("Questions",secondary="ques_ans_reln")

#class Ques_Ans_Reln(db.Model):
#   __tablename___="ques_ans_reln"
#   QID=db.Column(db.Integer,db.ForeignKey("Questions.QID"),primary_key=True,nullable=False)
#   AID=db.Column(db.Integer,db.ForeignKey("Answers.AID"),primary_key=True,nullable=False)


#-------------------------------------------- App Functions -------------------------------------------------------
def questions_finder(subject):
    question=Questions.query.filter_by(subject=subject).order_by(Questions.frequency.desc()).all()
    quest=[]
    for que in question:
        quest.append(que.question)
    return quest

def inactive_subs(active_sub):
    all_subs=["CG","JAVA","ECOM","NS","SE"]
    all_subs.remove(active_sub)
    return all_subs
    
#--------------------------------------------- App Routes -------------------------------------------------------

#*********************************************** Index_Page ********************************************************
@app.route("/",methods=["GET"])
def homepage():
    subjects=["CG","JAVA","ECOM","NS","SE"]
    return render_template("homepage.html",subjects=subjects)

@app.route("/SE",methods=["GET"])
def SE():
    active="SE"
    inactive=inactive_subs(active)
    quest=questions_finder(active)
    return render_template("subject_page.html",active=active,inactive=inactive,question=quest)

@app.route("/CG",methods=["GET"])
def CG():
    active="CG"
    inactive=inactive_subs(active)
    quest=questions_finder(active)
    return render_template("subject_page.html",active=active,inactive=inactive,question=quest)


@app.route("/JAVA",methods=["GET"])
def JAVA():
    active="JAVA"
    inactive=inactive_subs(active)
    quest=questions_finder(active)
    return render_template("subject_page.html",active=active,inactive=inactive,question=quest)


@app.route("/ECOM",methods=["GET"])
def ECOM():
    active="ECOM"
    inactive=inactive_subs(active)
    quest=questions_finder(active)
    return render_template("subject_page.html",active=active,inactive=inactive,question=quest)


@app.route("/NS",methods=["GET"])
def NS():
    active="NS"
    inactive=inactive_subs(active)
    quest=questions_finder(active)
    return render_template("subject_page.html",active=active,inactive=inactive,question=quest)


#---------------------------------------------- App Run ---------------------------------------------------------

if __name__=="__main__":
    app.run(host="0.0.0.0",
            port=8080)


#================================================ END ============================================================