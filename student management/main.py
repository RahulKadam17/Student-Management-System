from flask import Flask,render_template,request,session,redirect,url_for,flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash,check_password_hash
from flask_login import login_user,logout_user,login_manager,LoginManager
from flask_login import login_required,current_user
import json
import pandas as pd
import mysql.connector
import cv2
import numpy as np
import face_recognition
import os
from datetime import datetime
import time
from pymongo import MongoClient
from bson.objectid import ObjectId

# MY db connection
local_server= True
app = Flask(__name__)
app.secret_key='rahul'

#nosql(mongoDB) connection
client = MongoClient('mongodb://localhost:27017/')
db1 = client['stud']
collection = db1['mycollection']


# this is for getting unique user access
login_manager=LoginManager(app)
login_manager.login_view='login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


#mySQL connectivity
# app.config['SQLALCHEMY_DATABASE_URL']='mysql://username:password@localhost/databas_table_name'
app.config['SQLALCHEMY_DATABASE_URI']='mysql://root:@localhost/students'
db=SQLAlchemy(app)



class Department(db.Model):
    cid=db.Column(db.Integer,primary_key=True)
    branch=db.Column(db.String(100))

class Attendence(db.Model):
    aid=db.Column(db.Integer,primary_key=True)
    rollno=db.Column(db.String(100))
    course=db.Column(db.String(100))
    attendance=db.Column(db.Integer())

class Atte(db.Model):
    rollno=db.Column(db.String(100))
    course=db.Column(db.String(100))
    date=db.Column(db.Date)
    aid=db.Column(db.Integer,primary_key=True)

class Trig(db.Model):
    tid=db.Column(db.Integer,primary_key=True)
    rollno=db.Column(db.String(100))
    action=db.Column(db.String(100))
    timestamp=db.Column(db.String(100))


class User(UserMixin,db.Model):
    id=db.Column(db.Integer,primary_key=True)
    username=db.Column(db.String(50))
    email=db.Column(db.String(50),unique=True)
    password=db.Column(db.String(1000))



class Student(db.Model):
    rollno=db.Column(db.String(50),primary_key=True)
    sname=db.Column(db.String(50))
    sem=db.Column(db.Integer)
    gender=db.Column(db.String(50))
    branch=db.Column(db.String(50))
    email=db.Column(db.String(50))
    number=db.Column(db.String(12))
    address=db.Column(db.String(100))
    counsellor=db.Column(db.String(10))


#new enrol class
class Enrol(db.Model):
    rollno=db.Column(db.String(10),primary_key=True) 
    coursecode=db.Column(db.String(10),primary_key=True)
    
    # id=db.Column(db.Integer,primary_key=True)
    
class Grade(db.Model):
    gid=db.Column(db.Integer,primary_key=True)
    rollno=db.Column(db.String(10),primary_key=True) 
    coursecode=db.Column(db.String(10),primary_key=True)
    tid=db.Column(db.Integer)
    marks=db.Column(db.Integer)

class Course(db.Model):
    coursecode=db.Column(db.String(10),primary_key=True)
    coursename=db.Column(db.String(10))
    branch_id=db.Column(db.String(10))
    sem=db.Column(db.Integer)

@app.route('/')
def index(): 
    return render_template('main.html')

@app.route('/base')
@login_required
def base(): 
    return render_template('index.html')

@app.route('/studentdetails')
@login_required
def studentdetails():
    query=db.engine.execute(f"SELECT * FROM `student`") 
    return render_template('studentdetails.html',query=query)

@app.route('/triggers')
def triggers():
    query=db.engine.execute(f"SELECT * FROM `trig`") 
    return render_template('triggers.html',query=query)

@app.route('/department',methods=['POST','GET'])
@login_required
def department():
    if request.method=="POST":
        dept=request.form.get('dept')
        cid=request.form.get('cid')
        query=Department.query.filter_by(branch=dept).first()
        if query:
            flash("Department Already Exist","warning")
            return redirect('/department')
        dep=Department(cid=cid,branch=dept)
        db.session.add(dep)
        db.session.commit()
        flash("Department Added","success")
    return render_template('department.html')


def markAttendance(name,course):
    
    nameList = []
    courseList= []
    dates = []
    
    q=db.engine.execute(f"SELECT * FROM `atte`;")
    now = datetime.now()
    dtString = now.strftime('%d/%m/%Y')
        
    #Open file in append mode to write new data
    with open('C://Users//rahul//OneDrive//Desktop//StudentManagement-System-dbms-miniproject//student management//templates//Attendance.csv', 'a') as f:
        f.write(f'\n{name},{dtString},{course}')
            
        # Query database to update attendance records
    q=db.engine.execute(f"DELETE FROM `atte` WHERE rollno='{name}' AND course='{course}' AND date='{dtString}' ;")
    quer=db.engine.execute(f"INSERT INTO `atte` (`rollno`,`date`,`course`) VALUES ('{name}','{dtString}','{course}')")
    quer1=db.engine.execute(f"DELETE FROM `attendence` WHERE `rollno`='{name}' AND `course`='{course}';")
        # a=db.engine.execute(f"SELECT COUNT(rollno) AS c FROM `atte` WHERE `course`='{course}' AND `rollno`='{name}' ; ")
    a=db.engine.execute(f"SELECT COUNT( DISTINCT(date)) AS c FROM  `atte` WHERE `course`='{course}' AND `rollno`='{name}'  ;")
    for i in a:
      var=i.c
      var=(var/30)*100
    quer2=db.engine.execute(f"INSERT INTO `attendence` (`rollno`,`course`,`attendance`) VALUES ('{name}','{course}','{var}')  ")
        
    return

def findEncodings(images):
    encodeList = []


    for img in images:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        encode = face_recognition.face_encodings(img)[0]
        encodeList.append(encode)
    return encodeList


@app.route('/addattendance',methods=['POST','GET'])
@login_required
def addattendance():
      quer=0
      course=db.engine.execute("SELECT * FROM `course`")
      query=db.engine.execute(f"SELECT * FROM `student`;") 
      if request.method=="POST":
         rollno=request.form.get('rollno')
         cours=request.form.get('coursecode')
         attend=request.form.get('attend')
         print(attend,rollno)
         quer=db.engine.execute(f"DELETE FROM `attendence` WHERE `rollno`='{rollno}' AND `course`='{cours}';")
         quer=db.engine.execute(f"INSERT INTO `attendence` (`rollno`,`course`,`attendance`) VALUES ('{rollno}','{cours}','{attend}')  ")
         flash("Attendance added","warning")

        
      return render_template('attendance.html',query=query,quer=quer,course=course)

@app.route('/image/<rollno>')
def get_image(rollno):
    # Query MongoDB for the image data associated with the given rollno
    result = collection.find_one({'rollno': rollno})

    # If the rollno is not found, return a 404 error
    if result is None:
        return 'Image not found', 404

    # Return the image data as a response
    return result['image'], 3, {'Content-Type': 'image/png'}


@app.route('/search',methods=['POST','GET'])
@login_required
def search():

    if request.method=="POST":
        rollno=request.form.get('rollno')
        bio=Student.query.filter_by(rollno=rollno).first()
        cns=db.engine.execute(f"SELECT s.rollno,st.name FROM `staff` as st,`student` as s WHERE st.staffid=s.counsellor AND s.rollno='{rollno}'; ")
         
        attend=Attendence.query.filter_by(rollno=rollno).all()
        enroll=Enrol.query.filter_by(rollno=rollno).all()
        grad=Grade.query.with_entities(Grade.coursecode).order_by(Grade.coursecode.asc()).distinct().all()
        grade=Grade.query.filter_by(rollno=rollno).order_by(Grade.coursecode.asc(),Grade.tid.asc()).all()
        # cou=Grade.query.filter_by(f"")
        query1=db.engine.execute(f"SELECT staffid,course,rollno FROM (`enrol` JOIN `teach` ON coursecode=course AND `rollno`='{rollno}');")
        print(query1)
        print(grade)
        return render_template('search.html',bio=bio,attend=attend,enroll=enroll,grade=grade,query1=query1,grad=grad,cns=cns)
        
    return render_template('search.html')

@app.route("/delete/<string:rollno>",methods=['POST','GET'])
@login_required
def delete(rollno):
    db.engine.execute(f"DELETE FROM `student` WHERE `rollno`='{rollno}'")
    flash("Deleted Successfully","danger")
    return redirect('/studentdetails')


@app.route("/edit/<string:rollno>",methods=['POST','GET'])
@login_required
def edit(rollno):
    dept=db.engine.execute("SELECT * FROM `department`")
    posts=Student.query.filter_by(rollno=rollno).first()
    if request.method=="POST":
        rollno=request.form.get('rollno')
        sname=request.form.get('sname')
        sem=request.form.get('sem')
        gender=request.form.get('gender')
        branch=request.form.get('branch')
        email=request.form.get('email')
        num=request.form.get('num')
        address=request.form.get('address')
        counsellor=request.form.get('counsellor')
        query=db.engine.execute(f"UPDATE `student` SET `rollno`='{rollno}',`sname`='{sname}',`sem`='{sem}',`gender`='{gender}',`branch`='{branch}',`email`='{email}',`number`='{num}',`address`='{address}',`counsellor`='{counsellor}' WHERE `student`.`rollno`='{rollno}'")
        flash("Details Updated","success")
        return redirect('/studentdetails')
    
    return render_template('edit.html',posts=posts,dept=dept)


@app.route('/signup',methods=['POST','GET'])
def signup():
    if request.method == "POST":
        username=request.form.get('username')
        email=request.form.get('email')
        password=request.form.get('password')
        user=User.query.filter_by(email=email).first()
        
        if user:
            flash("Email Already Exist","warning")
            return render_template('/signup.html')
        encpassword=generate_password_hash(password)
        
        new_user=db.engine.execute(f"INSERT INTO `user` (`username`,`email`,`password`) VALUES ('{username}','{email}','{encpassword}')")
       
            
        flash("Signup Succes Please Login","success")
        return render_template('login.html')

          

    return render_template('signup.html')

@app.route('/login',methods=['POST','GET'])
def login():
    if request.method == "POST":
        email=request.form.get('email')
        password=request.form.get('password')
        user=User.query.filter_by(email=email).first()

        if user and check_password_hash(user.password,password):
            login_user(user)
            flash("Login Success","primary")
            return redirect(url_for('base'))
        else:
            flash("invalid credentials","danger")
            return render_template('login.html')    

    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash("Logout SuccessFul","warning")
    return redirect(url_for('login'))



@app.route('/addstudent',methods=['POST','GET'])
@login_required
def addstudent():
    dept=db.engine.execute("SELECT * FROM `department`")
    couns=db.engine.execute("SELECT * FROM `staff`")
    if request.method=="POST":
        rollno=request.form.get('rollno')
        stud=Student.query.filter_by(rollno=rollno).first()
        
        if stud:
            flash("Student Already Exist","warning")
            return render_template('/student.html')
        sname=request.form.get('sname')
        sem=request.form.get('sem')
        gender=request.form.get('gender')
        branch=request.form.get('branch')
        email=request.form.get('email')
        user=Student.query.filter_by(email=email).first()
        
        if user:
            flash("Email Already Exist","warning")
            return render_template('/student.html')
        num=request.form.get('num')
        address=request.form.get('address')
        counsellor=request.form.get('counsellor')
        file = request.files['file']

        # Save the image to MongoDB
        collection.insert_one({'rollno': rollno, 'image': file.read()})
        query=db.engine.execute(f"INSERT INTO `student` (`rollno`,`sname`,`sem`,`gender`,`branch`,`email`,`number`,`address`,`counsellor`) VALUES ('{rollno}','{sname}','{sem}','{gender}','{branch}','{email}','{num}','{address}','{counsellor}')")
    
        
        flash("Appended success","info")


    return render_template('student.html',dept=dept,couns=couns)

@app.route('/enrol',methods=['POST','GET'])
@login_required
def enrol():
    enroll=db.engine.execute(f"SELECT * FROM `enrol`") 
    stud=db.engine.execute("SELECT * FROM `student`")
    course=db.engine.execute(f"SELECT * FROM `course` ")

    if request.method=="POST":
        rollno=request.form.get('rollno')
        coursecode=request.form.get('coursecode')
        print(coursecode,rollno)
        en=Enrol(rollno=rollno,coursecode=coursecode)
        db.session.add(en)
        db.session.commit()
        flash("Enrolled successfully","warning")
        
        
    return render_template('enrol.html',enroll=enroll,course=course,stud=stud)


@app.route('/grade',methods=['POST','GET'])
@login_required
def grade():
    marks=db.engine.execute("SELECT * FROM `grade`")
    course=db.engine.execute("SELECT * FROM `course`") 
    if request.method=="POST":
        rollno=request.form.get('rollno')
        coursecode=request.form.get('coursecode')
        marks=request.form.get('marks')
        tid=request.form.get('tid')
        print(coursecode,rollno)
        grad=Grade(rollno=rollno,coursecode=coursecode,tid=tid,marks=marks)
        db.session.add(grad)
        db.session.commit()
        flash("success","warning")

        
    return render_template('grades.html',marks=marks,course=course)


@app.route('/marks',methods=['POST','GET'])
@login_required
def marks():
    marks=db.engine.execute("SELECT * FROM `grade`")
    course=db.engine.execute("SELECT * FROM `course`") 
    if request.method=="POST":
        file = request.files['file']
        df = pd.read_excel(file)
        mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="students"
        )
        cursor = mydb.cursor()
        
        # # Insert the data into the MySQL table
        # for i, row in data.iterrows():
        #     sql = "INSERT INTO grade (tid, rollno, coursecode, marks) VALUES (%s, %s, %s, %s)"
        #     val = (row['tid'], row['rollno'], row['coursecode'], row['marks'])
        #     mycursor.execute(sql, val)
        for index, row in df.iterrows():
          testid = row['tid']
          rollno = row['rollno']
    
    # loop through the course code columns and insert a separate record for each one
          for i in range(1, 6):  # assumes there are 6 course code columns, adjust as needed
           if i == 1:
            marks = row['18CS52']
            coursecode='18CS52'
           elif i == 2:
            marks = row['18CS53']
            coursecode='18CS53'
           elif i == 3:
            marks = row['18CS54']
            coursecode='18CS54'
           elif i == 4:
            marks = row['18G5B09']
            coursecode='18G5B09'
           else:
            marks = row['18IS55']
            coursecode='18IS55'
           
    
           
        
        # skip if the marks column is empty
           if pd.isna(marks):
             continue
        
        # construct the SQL query
           sql = "INSERT INTO grade (tid, rollno, coursecode,marks) VALUES (%s, %s, %s, %s)"
        
        # execute the SQL query
           cursor.execute(sql, (testid, rollno, coursecode, marks))
        mydb.commit()
        cursor.close()
        mydb.close()
        flash("success","warning")

        
    return render_template('grades.html',marks=marks,course=course)





@app.route('/attendance',methods=['POST','GET'])
def attendance():
 
 course=db.engine.execute("SELECT * FROM `course`")
 
 if request.method=="POST":

    cours=request.form.get('coursecode')
    if 'att' in request.form:
    # path = 'C:\\Users\\rahul\\OneDrive\\Desktop\\StudentManagement-System-dbms-miniproject\\student management\\Training_images'
      images = []
      classNames = []
   
    
      for doc in collection.find():
            img_data = doc['image']
            img_np = np.frombuffer(img_data, np.uint8)
            img = cv2.imdecode(img_np, cv2.IMREAD_COLOR)
            images.append(img)
            classNames.append(str(doc['rollno']))
      print(classNames)
     
      encodeListKnown = findEncodings(images)
      print('Encoding Complete')
    
      
      cap = cv2.VideoCapture(0)
   
      while True:
        success, img = cap.read()
        imgS = cv2.resize(img, (0, 0), None, 0.25, 0.25)
        imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)

        facesCurFrame = face_recognition.face_locations(imgS)
        encodesCurFrame = face_recognition.face_encodings(imgS, facesCurFrame)

        for encodeFace, faceLoc in zip(encodesCurFrame, facesCurFrame):
          matches = face_recognition.compare_faces(encodeListKnown, encodeFace)
          faceDis = face_recognition.face_distance(encodeListKnown, encodeFace)
          matchIndex = np.argmin(faceDis)
          
          if matches[matchIndex]:
            name = classNames[matchIndex].upper()
            y1, x2, y2, x1 = faceLoc
            y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4
            cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv2.rectangle(img, (x1, y2 - 35), (x2, y2), (0, 255, 0), cv2.FILLED)
            cv2.putText(img, name, (x1 + 6, y2 - 6), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 0, 0), 2)
            markAttendance(name,cours)
          if 'close' in request.form:
            cap.release()
            cv2.destroyAllWindows()
            return redirect(url_for(''))
        cv2.imshow('Webcam', img)
        if cv2.waitKey(1) & 0XFF == ord('q'):
         break

      cap.release()
      cv2.destroyAllWindows()

    
 return render_template('vatt.html',course=course)

app.run(debug=True)

