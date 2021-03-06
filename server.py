#!/usr/bin/python

from flask import Flask, render_template
from flask import request
from flask import g
import json
import numpy as np
import os
import mysql.connector
from datetime import datetime

db = mysql.connector.connect(user='root', password='root', host='127.0.0.1', database='student', buffered=True)

app = Flask(__name__)

@app.teardown_appcontext
def close_connection(exception):
  db = getattr(g, '_database', None)
  if db is not None:
    db.close()

@app.route("/")
def hello():
  return render_template("home.html")

@app.route("/enroll", methods=["POST"])
def enroll():
  image = []
  req_data = request.get_json()
  cur = db.cursor()
  sql = "INSERT INTO student (rn, fname, lname, image, class) VALUES (%s,%s,%s,%s,%s)"
  values = (int(req_data["roll"]), req_data["fname"], req_data["lname"], json.dumps(np.asarray(req_data["image"]).tolist()) , req_data["class"])
  print values
  res = cur.execute(sql, values)
  print cur.lastrowid
  db.commit()
  return "ok"

@app.route("/createlecture", methods=["POST"])
def createLecture():
  req_data = request.get_json()
  cur = db.cursor()
  tsStart = req_data["startTime"]
  tsEnd = req_data["endTime"]
  name = req_data["name"]
  classNum = req_data["class"]
  print tsStart, tsEnd, name, classNum
  cur = db.cursor()
  sql = "INSERT INTO lectures (class, lectureName, startTime, endTime) VALUES (%s, %s, %s, %s)"
  values = (classNum, name, tsStart, tsEnd)
  res = cur.execute(sql, values)
  db.commit()
  return "ok"

  
@app.route("/getclass", methods=["GET"])
def getClass():
  cur = db.cursor(buffered=True,dictionary=True)
  className = request.args.get("class").encode('ascii','ignore')
  sql = "SELECT * FROM student WHERE class = %s"
  values = (className,)
  cur.execute(sql, values)
  sendRes = []
  rows = cur.fetchall()
  for row in rows:
    data = {
	    "roll" : row["rn"],
	    "fname" : row["fname"],
	    "lname" : row["lname"],
	    "image" : row["image"].decode("utf-8")
	  }
    sendRes.append(data)
  return json.dumps(sendRes)

@app.route("/getattendance", methods=["GET"])
def getattendance():
  cur = db.cursor(buffered=True,dictionary=True)
  className = request.args.get("class").encode('ascii','ignore')
  startTime = request.args.get("starttime").encode('ascii','ignore')
  sql = "SELECT rn, fname, lname, class from student where rn in (select rn from lectures, attend where lectures.class = %s and lectures.startTime = %s and attend.time >= lectures.startTime and attend.time < lectures.endTime)"
  values = (className, startTime,)
  cur.execute(sql, values)
  students = []
  present = 0
  rows = cur.fetchall()
  for row in rows:
    data = {
      "roll" : row["rn"],
      "fname" : row["fname"],
      "lname" : row["lname"]
    }
    present = present + 1
    students.append(data)
  
  sql = "SELECT count(*) as count from student where class = %s"
  values = (className,)
  cur.execute(sql,values)
  total = cur.fetchone()["count"]

  sendRes = {
    "students" : students,
    "total" : total,
    "present" : present
  }
  return json.dumps(sendRes)

@app.route("/attend", methods=["POST"])
def attend():
  req_data = request.get_json()
  cur = db.cursor()
  sql = "INSERT INTO attend (rn, class) VALUES (%s, %s)"
  values = (int(req_data["rn"]), req_data["class"])
  res = cur.execute(sql, values)
  db.commit()
  return "ok"

if __name__ == "__main__":
  app.run(debug=True, host="0.0.0.0", port=80)
