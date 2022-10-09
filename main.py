#------------------------------------------ Importing Modules ----------------------------------------------------

from datetime import date as dt
from sqlite3 import Date

from flask import Flask
from flask import request,render_template,redirect,url_for

from flask_sqlalchemy import SQLAlchemy

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt  

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
    elif request.method == "POST" :
        user_name = request.form["signup-username"]
        password = request.form["signup-password"]
        user=Member.query.filter_by(member_username=user_name).first()
        if user:
            alert="user_exist"
            return render_template("signup_page.html",alert=alert)
        date = str(dt.today())
        member = Member(member_username = user_name,member_password = password,member_created_date = date)
        db.session.add(member)
        db.session.commit()
        alert="signup_success"
        return redirect(url_for('user_homepage',username=user_name))
        
#*********************************************** Login_Page ********************************************************
@app.route("/login",methods=["GET","POST"])
def login_page():
    if request.method == "GET":
        return render_template("login_page.html")
    elif request.method == "POST" :
        user_name = request.form["login-username"]
        password = request.form["login-password"]
        user = Member.query.filter_by(member_username=user_name).first()
        if user:
            if user.member_password==password:
                alert="login_success"
                return redirect(url_for('user_homepage',username=user_name))
            else:
                alert="wrong_password"
                return render_template("login_page.html",alert=alert)
        else:
            alert="user_does_not_exist"
            return render_template("login_page.html",alert=alert)

#*********************************************** User_Summary ********************************************************
@app.route("/<username>/summary",methods=["GET","POST"])
def user_summary(username):
    user=Member.query.filter_by(member_username=username).first()
    mem_l=Mem_list.query.filter_by(member_id=user.member_id).all()
    if mem_l:
        cards=Card.query.all()
        list_card=[]
        lists=[]
        cl_dict={}
        samp_l={}
        for_graph={}
        for i in range(len(mem_l)):
            lists.append(List.query.filter_by(list_id=mem_l[i].list_id).all())
        for i in lists:
            for j in range(len(i)):
                card_l=List_card.query.filter_by(list_id=i[j].list_id).all()
            if card_l:
                for_graph[i[j].list_id]=[]
                samp_l[i[j].list_id]=[]
                for z in card_l:
                    a_card=Card.query.get(z.card_id)
                    samp_l[i[j].list_id].append(a_card)
                    cc,unc,tot=0,0,0
                for m in (samp_l[i[j].list_id]):
                    tot+=1
                    if m.card_completed=="checked":
                        cc+=1
                        for_graph[i[j].list_id].append(m.card_completed_date)
                    else:
                        unc+=1
                    cl_dict[i[j].list_id]=(cc,unc,tot)
        for key in list(for_graph.keys()):
            data = for_graph[key]
            data.sort()
            plt.hist(data,color="#00b100")
            plt.xlabel("Date")
            plt.ylabel("Number of tasks completed")
            plt.savefig("./static/"+str(key)+".png")
            plt.close()

        return render_template("user_summary.html",cards=cards,username=username,
                            lists=lists,list_card=list_card,
                            cl_dict=cl_dict)
    else:
        return render_template("user_summary.html",username=username)

#*********************************************** User_Homepage ********************************************************
@app.route("/<username>/user_homepage",methods=["GET","POST"])
def user_homepage(username):
    user=Member.query.filter_by(member_username=username).first()
    mem_l=Mem_list.query.filter_by(member_id=user.member_id).all()
    list_card=[]
    lists=[]
    cards=Card.query.all()
    if mem_l:
        for i in range(len(mem_l)):
            lists.append(List.query.filter_by(list_id=mem_l[i].list_id).all())
        for i in lists:
            for j in range(len(i)):
                card_l=List_card.query.filter_by(list_id=i[j].list_id).all()
            if card_l:
                list_card.append(card_l)
    return render_template("user_homepage_card.html",username=username,lists=lists,
                            cards=cards,list_card=list_card,
                            date=str(dt.today()))

#*********************************************** List_Edit ********************************************************
@app.route("/<username>/<list_name>/edit",methods=["GET","POST"])
def edit_list(username,list_name):
    if request.method=="GET":
        lst=List.query.filter_by(list_name=list_name).first()
        return render_template("list_edit.html",username=username,list_name=lst.list_name,list_desc=lst.list_desc)
    elif request.method=="POST":
        memb=Member.query.filter_by(member_username=username).first()
        mem_l=Mem_list.query.filter_by(member_id=memb.member_id).all()
        if mem_l:
            for ml in mem_l:
                l=List.query.filter_by(list_id=ml.list_id).first()
                if (l.list_name==request.form['get_list_name'] and l.list_name != list_name):
                    alert="list_already_exist"
                    return render_template("add_list.html",username=username,alert=alert)
        lst=List.query.filter_by(list_name=list_name).first()
        db.session.delete(lst)
        lst.list_name=request.form['get_list_name']
        lst.list_desc=request.form['get_list_desc']
        lst_modified_dt= dt.today()
        lst.list_modified_date=lst_modified_dt
        db.session.add(lst)
        db.session.commit()
        return redirect(url_for('user_homepage',username=username))

#*********************************************** List_Delete ********************************************************
@app.route("/<username>/<list_name>/delete",methods=["GET","POST"])
def delete_list(username,list_name):
    list=List.query.filter_by(list_name=list_name).first()
    m_l=Mem_list.query.filter_by(list_id=list.list_id).all()
    for i in m_l:
        db.session.delete(i)
    l_c=List_card.query.filter_by(list_id=list.list_id).all()
    for i in l_c:
        db.session.delete(i)
    db.session.delete(list)
    db.session.commit()
    return redirect(url_for('user_homepage',username=username))

#*********************************************** List_Add ********************************************************
@app.route("/<username>/add_list",methods=["GET","POST"])
def add_list(username):
    if request.method=="GET":
        return render_template("add_list.html",username=username)
    elif request.method=="POST":
        list_name=request.form["add_list_name"]
        list_desc=request.form["add_list_desc"]
        memb=Member.query.filter_by(member_username=username).first()
        mem_l=Mem_list.query.filter_by(member_id=memb.member_id).all()
        if mem_l:
            for ml in mem_l:
                l=List.query.filter_by(list_id=ml.list_id).first()
                if l.list_name==list_name:
                    alert="list_already_exist"
                    return render_template("add_list.html",username=username,alert=alert)
        date = str(dt.today())
        new_list=List(list_name=list_name,list_desc=list_desc,list_created_date=date)
        db.session.add(new_list)
        db.session.flush()
        user=Member.query.filter_by(member_username=username).first()
        user_id=user.member_id
        new_mem_list = Mem_list(member_id=user_id,list_id=new_list.list_id)
        db.session.add(new_mem_list)
        db.session.commit()
        return redirect(url_for('user_homepage',username=username))

#*********************************************** Card_Add ********************************************************
@app.route("/<username>/<list_name>/add_card",methods=["GET","POST"])
def add_card(username,list_name):
    if request.method=="GET":
        new_lst=[]
        member=Member.query.filter_by(member_username=username).first()
        mem_lst=Mem_list.query.filter_by(member_id=member.member_id)
        for lst in mem_lst:
            new_lst.append(lst.list_id)
        #print(new_lst)
        new_lists=[]
        for i in new_lst:
            lists=List.query.get(i)
            new_lists.append(lists)
        #print(new_lists)
        return render_template("add_card.html",username=username,list_name=list_name,lists=new_lists)
    elif request.method=="POST":
        title=request.form["card_title"]
        content=request.form["card_content"]
        deadline=request.form["card_deadline"]
        new_lst=[]
        member=Member.query.filter_by(member_username=username).first()
        mem_lst=Mem_list.query.filter_by(member_id=member.member_id)
        for lst in mem_lst:
            new_lst.append(lst.list_id)
        #print(new_lst)
        new_lists=[]
        for i in new_lst:
            lists=List.query.get(i)
            new_lists.append(lists)
        lt=List.query.filter_by(list_name=list_name).first()
        l_card=List_card.query.filter_by(list_id=lt.list_id).all()
        if l_card:
            for lc in l_card:
                c=Card.query.filter_by(card_id=lc.card_id).first()
                if c.card_name==title:
                    alert="card_already_exist"
                    return render_template("add_card.html",username=username,list_name=list_name,lists=new_lists,alert=alert)
        date = str(dt.today())
        new_card=Card(card_name=title,card_desc=content,card_created_date=date,card_deadline=deadline,card_completed="unchecked")
        db.session.add(new_card)
        db.session.flush()
        lst=List.query.filter_by(list_name=list_name).first()
        lst_id=lst.list_id
        new_list_card = List_card(card_id=new_card.card_id,list_id=lst_id)
        db.session.add(new_list_card)
        db.session.commit()
        return redirect(url_for('user_homepage',username=username))   

#*********************************************** Card_Edit ********************************************************
@app.route("/<username>/<list_name>/<card_name>/edit",methods=["GET","POST"])
def edit_card(username,list_name,card_name):
    if request.method=="GET":
        new_lst=[]
        member=Member.query.filter_by(member_username=username).first()
        mem_lst=Mem_list.query.filter_by(member_id=member.member_id)
        for lst in mem_lst:
            new_lst.append(lst.list_id)
        #print(new_lst)
        new_lists=[]
        for i in new_lst:
            lists=List.query.get(i)
            new_lists.append(lists)
        #print(new_lists)
        card=Card.query.filter_by(card_name=card_name).first()
        return render_template("edit_card.html",username=username,list_name=list_name,lists=new_lists,cards=card)
    elif request.method=="POST":
        new_lst=[]
        member=Member.query.filter_by(member_username=username).first()
        mem_lst=Mem_list.query.filter_by(member_id=member.member_id)
        for lst in mem_lst:
            new_lst.append(lst.list_id)
        #print(new_lst)
        new_lists=[]
        for i in new_lst:
            lists=List.query.get(i)
            new_lists.append(lists)
        lt=List.query.filter_by(list_name=list_name).first()
        l_card=List_card.query.filter_by(list_id=lt.list_id).all()
        card=Card.query.filter_by(card_name=card_name).first()
        if l_card:
            for lc in l_card:
                c=Card.query.filter_by(card_id=lc.card_id).first()
                if (c.card_name==request.form["card_title"] and c.card_name != card_name) :
                    alert="card_already_exist"
                    return render_template("edit_card.html",username=username,list_name=list_name,lists=new_lists,alert=alert,cards=card)
        lst=List.query.filter_by(list_name=list_name).first()
        lst_card=List_card.query.filter_by(card_id=card.card_id).first()
        #print(lst_card)
        db.session.delete(card)
        db.session.delete(lst_card)
        card.card_name=request.form["card_title"]
        card.card_desc=request.form["card_content"]
        card.card_deadline=request.form["card_deadline"]
        if request.form["card_completed"]=="on":
            card.card_completed="checked"
            card.card_completed_date=dt.today()
        elif request.form["card_completed"]=="off":
            card.card_completed="unchecked"
            card.card_completed_date=None
        db.session.add(card)
        lst_card.card_id=card.card_id
        lst_card.list_id=lst.list_id
        db.session.add(lst_card)
        db.session.commit()
        return redirect(url_for('user_homepage',username=username))

#*********************************************** Card_Delete ********************************************************
@app.route("/<username>/<list_name>/<card_name>/delete")
def delete_card(username,list_name,card_name):
    card=Card.query.filter_by(card_name=card_name).first()
    list_card=List_card.query.filter_by(card_id=card.card_id).first()
    db.session.delete(card)
    db.session.delete(list_card)
    db.session.commit()
    return redirect(url_for('user_homepage',username=username))


#---------------------------------------------- App Run ---------------------------------------------------------

if __name__=="__main__":
    app.run(host="0.0.0.0",
            port=8080)


#================================================ END ============================================================