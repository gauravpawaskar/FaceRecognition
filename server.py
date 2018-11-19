#!/usr/bin/python

from flask import Flask, render_template
from flask import request
from flask import g
import json
import face_recognition
import numpy as np
import os
import sqlite3
from sqlite3 import Error
#from jinja2 import

database = "student.db"

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(database)
    return db

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
  cur = get_db().cursor()
  try:
    res = cur.execute("INSERT INTO student (rn, fname, lname, image, class) values (?,?,?,?,?)", 
    (int(req_data["roll"]), req_data["fname"], req_data["lname"], json.dumps(np.asarray(req_data["image"]).tolist()) , req_data["class"]))
    print cur.lastrowid
    get_db().commit()
  except Error as e:
    print e
  return "ok"
  
@app.route("/getclass", methods=["GET"])
def getClass():
  cur = get_db().cursor()
  cls = request.args.get("class")
  res = cur.execute("SELECT * FROM student WHERE class = ?", (cls,))
  sendRes = []
  rows = res.fetchall()
  for row in rows:
	  data = {
	  "roll" : row[0],
	  "fname" : row[1],
	  "lname" : row[2],
	  "image" : row[3]
	  }
	  sendRes.append(data)
  return json.dumps(sendRes)

if __name__ == "__main__":
  app.run(debug=True, host="0.0.0.0", port=80)
