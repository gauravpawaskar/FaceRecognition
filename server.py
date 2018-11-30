#!/usr/bin/python

from flask import Flask, render_template
from flask import request
from flask import g
import json
import face_recognition
import numpy as np
import os
#import sqlite3
#from sqlite3 import Error
import mysql.connector

#database = "student.db"

db = mysql.connector.connect(user='root', password='root', host='127.0.0.1', database='student', buffered=True)

app = Flask(__name__)

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

@app.route("/")
def hello():
        #template = Template("Hello {{ name }}!")
        return render_template("home.html")

@app.route("/enroll", methods=["POST"])
def enroll():
  image = []
  req_data = request.get_json()
  cur = db.cursor()
  sql = "INSERT INTO student (rn, fname, lname, image, class) VALUES (%s,%s,%s,%s,%s)"
  values = (int(req_data["roll"]), req_data["fname"], req_data["lname"], json.dumps(np.asarray(req_data["image"]).tolist()) , req_data["class"])
  print values
  #try:
  res = cur.execute(sql, values)
  print cur.lastrowid
  db.commit()
  #except Exception as e:
   # print e
  return "ok"
  
@app.route("/getclass", methods=["GET"])
def getClass():
  cur = db.cursor(buffered=True,dictionary=True)
  className = request.args.get("class").encode('ascii','ignore')
  sql = "SELECT * FROM student WHERE class = %s"
  values = (className,)
  #print sql, values
  cur.execute(sql, values)
  sendRes = []
  rows = cur.fetchall()
  for row in rows:
    #print row["lname"]
    data = {
	    "roll" : row["rn"],
	    "fname" : row["fname"],
	    "lname" : row["lname"],
	    "image" : row["image"].decode("utf-8")
	  }
    sendRes.append(data)
  return json.dumps(sendRes)

if __name__ == "__main__":
  app.run(debug=True, host="0.0.0.0", port=80)
