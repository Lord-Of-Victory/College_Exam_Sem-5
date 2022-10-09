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
    answer=db.relationship("Answers",secondary="ques_ans_reln")

class Answers(db.Model):
    __tablename___="answers"
    AID=db.Column(db.Integer,primary_key=True,nullable=False,autoincrement=True,unique=True)
    answer=db.Column(db.String,nullable=False)
    question=db.relationship("Questions",secondary="ques_ans_reln")

class Ques_Ans_Reln(db.Model):
    __tablename___="ques_ans_reln"
    QID=db.Column(db.Integer,db.ForeignKey("questions.QID"),primary_key=True,nullable=False)
    AID=db.Column(db.Integer,db.ForeignKey("answers.AID"),primary_key=True,nullable=False)


#--------------------------------------------- App Routes -------------------------------------------------------

#*********************************************** Index_Page ********************************************************
@app.route("/",methods=["GET"])
def homepage():
    active="SE"
    all_subs=["CG","JAVA","ECOM","NS","SE"]
    inactive=all_subs.remove(active)
    return render_template("homepage.html")

#---------------------------------------------- App Run ---------------------------------------------------------

if __name__=="__main__":
    app.run(host="0.0.0.0",
            port=8080)


#================================================ END ============================================================