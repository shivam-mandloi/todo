from flask import Flask,render_template,request,session
import json
from datetime import datetime
import smtplib
import random
from mongoengine import connect,document,StringField,IntField,EmailField

class user:
    def __init__(self,name,login):
        self.name = name
        self.login = login


class Otp(document.DynamicDocument):
    email=EmailField()
    otp=StringField()
    time=StringField()
    def to_json(self):
        return{
            "id":self.id,
            "email":self.email,
            "otp":self.otp,
            "time":self.time
        }

class Tasks(document.DynamicDocument):
    title=StringField()
    message=StringField()
    time = StringField()
    complete=IntField()
    def to_json(self):
        return {
            "id":self.id,
            "message":self.message,
            "date":self.date,
            "time":self.time,
            "complete":self.complete
        }

class User(document.DynamicDocument):
    name = StringField()
    email = EmailField()
    password = StringField()
    def to_json(self):
        return{
        "name":self.name,
        "email":self.email,
        "password":self.password
        }

def Now_time():
    # change formate of time convert "2021-11-20 13:17:11.661696" to "26 jan 2017 , 11pm"
    time = str(datetime.now())
    date={"1":"jan","2":"feb","3":"mar","4":"apr","5":"may","6":"jun","7":"jul","8":"aug","9":"sep","10":"oct","11":"nov","12":"dec"}
    if int(time[11:13]) > 11:
        hour = str(int(time[11:13])-12)+time[13:16]+"pm"
    else:
        hour = time[11:16]+"am"
    date_time = time[8:10]+" "+date[time[5:7]]+" "+time[0:4]+" "+hour
    return date_time

with open("config.json","r") as f:
    params = json.load(f)["params"]

connect(db=params['db_name'],
            host=params['db_host']
            )

user_login = user("login",0)

collection_task = Tasks()
collection_otp = Otp()
collection_user = User()

app = Flask(__name__)

@app.route("/")
def index():
    # Home page
    if user_login.login == 1:
        collection_task = Tasks.objects()
        return render_template("index.html",data=collection_task)
    return render_template("email.html",msg=params["default_msg_email"])

@app.route("/update/<string:todo_id>")
def update_todo(todo_id):
    # Update the list
    if user_login.login == 1:
        collection_task = Tasks.objects(id=todo_id).first()
        return render_template("update.html",data=collection_task,id=todo_id)
    return render_template("email.html",msg=params["default_msg_email"])

@app.route("/update_task/<string:todo_id>",methods=["POST","GET"])
def update_task(todo_id):
    # Update the database
    if user_login.login == 1:
        if request.method == "POST":
            title = request.form.get("title")
            message = request.form.get("message")
            if message == None:
                message = " "
            collection_task = Tasks.objects(id=todo_id).first()
            collection_task.update(title=title,message=message)
        collection_task = Tasks.objects()
        return render_template("index.html",data=collection_task)
    return render_template("email.html",msg=params["default_msg_email"])

@app.route("/add_todo")
def add_todo():
    # Add new todo in list
    if user_login.login == 1:
        return render_template("add_todo.html")
    return render_template("email.html",msg=params["default_msg_email"])

@app.route("/add_new_todo",methods=["GET","POST"])
def add_todo_in_database():
    # Add todo in database
    if user_login.login == 1:
        if request.method == "POST":
            title = request.form.get("title")
            message = request.form.get("message")
            date = Now_time()
            if message == None:
                message = " "
            collection_task = Tasks()
            collection_task.title = title
            collection_task.message = message
            collection_task.date = date
            collection_task.complete = 0
            collection_task.save()
            task_id = collection_task.id
        collection_task = Tasks.objects()
        return render_template("index.html",data=collection_task)
    return render_template("email.html",msg=params["default_msg_email"])

@app.route("/form",methods=["GET","POST"])
def otp():
    # send otp to email
    if request.method == "POST":
        email = request.form.get('email')
        if email != None and email != "":
            return render_template('form.html',email=email,user="",password="",msg=params["default_username_msg"])
    return render_template("email.html",msg=params["default_msg_email"])
    
@app.route("/email")
def email():
    # Email verification
    return render_template("email.html",msg=params["default_msg_email"])

@app.route("/delete/<string:todo_id>")
def delete(todo_id):
    # Delete task from database
    if user_login.login == 1:
        collection_task = Tasks.objects(id=todo_id).first()
        collection_task.delete()
        collection_task = Tasks()
        collection_task = Tasks.objects()
        return render_template("index.html",data=collection_task)
    return render_template("email.html",msg=params["default_msg_email"])

@app.route("/complete/<string:todo_id>")
def complete(todo_id):
    # Mark task to complete
    if user_login.login == 1:
        collection_task = Tasks.objects(id=todo_id).first()
        collection_task.to_json()
        if collection_task.complete == 0:
            collection_task.update(complete=1)
        else:
            collection_task.update(complete=0)
        collection_task = Tasks.objects()
        return render_template("index.html",data=collection_task)
    return render_template('email.html',msg=params["default_msg_email"])

@app.route("/submit-user-information/<string:email>",methods=["GET","POST"])
def submit_information(email):
    # add user information in database
    if request.method == "POST":
        name = request.form.get('name')
        password = request.form.get('password')        
        collection_user = User.objects(name=name).first()
        if collection_user != None:
            return render_template("form.html",user=name,pasword=password,email=email,msg=params["username_exist"])
        collection_user = User()
        collection_user.name = name
        collection_user.email = email
        collection_user.password = password
        collection_user.save()
        user_id = collection_user.id
        user_login.name = name
        user_login.login = 1
        collection_task = Tasks.objects()
        return render_template("index.html",data=collection_task)
    return render_template('email.html',msg=params["default_msg_email"])

@app.route("/logout")
def logout():
    # logout from user account
    user_login.login = 1
    return render_template("email.html",msg=params["default_msg_email"])

@app.route('/login')
def login():
    return render_template("login.html")

@app.route("/cheack-username",methods=["GET","POST"])
def cheack_username():
    # Cheack username and password give by user in login
    if request.method == "POST":
        user_name = request.form.get('name')        
        password = request.form.get("password")
        collection_user = User.objects(name=user_name).first()        
        if collection_user == None:
            return render_template("login.html",msg=params["msg_user_wrong_username"])
        collection_user.to_json()
        if  collection_user.password == password:
            collection_user = Tasks.objects()
            user_login.login = 1
            return render_template("index.html",data=collection_user)
        return render_template("login.html",msg=params["msg_user_wrong_pas"])
    return render_template("email.html",msg=params["default_msg_email"])

if "__main__" == __name__:
    app.run(debug=True)