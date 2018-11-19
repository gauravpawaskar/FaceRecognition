#!/usr/bin/python

import Tkinter as tk
from tkMessageBox import showinfo
import cv2
from PIL import Image, ImageTk
import face_recognition
import requests
import json
import numpy as np

class Home:
    def __init__(self, master):
        self.master = master
        self.frame = tk.Frame(self.master)
        self.button1 = tk.Button(self.frame, text = 'Enroll', width = 25, command = self.new_window)
        self.quitButton = tk.Button(self.frame, text = 'Quit', width = 25, command = self.close_windows)
        self.button1.pack()
        self.quitButton.pack()
        self.frame.pack()

    def new_window(self):
        self.newWindow = tk.Toplevel(self.master)
        self.app = Enroll(self.newWindow)
        
    def close_windows(self):
        self.master.destroy()

class Enroll:
    def __init__(self, master, output_path = "./"):
        self.master = master
        self.frame = tk.Frame(self.master)
        self.master.title("Enroll")
        self.master.vs = cv2.VideoCapture(0)
        self.master.current_image = None
        self.panel = tk.Label(self.master)
        self.panel.grid(row=1, column=2, columnspan=2)
        
        self.labelFName = tk.Label(self.frame, text="First Name")
        self.labelFName.grid(row=2,column=1)
        self.textFname = tk.Text(self.frame, height=1, width=25)
        self.textFname.grid(row=2,column=2)
        self.labelLName = tk.Label(self.frame, text="Last Name")
        self.labelLName.grid(row=3,column=1)
        self.textLname = tk.Text(self.frame, height=1, width=25)
        self.textLname.grid(row=3,column=2)
        self.labelClass = tk.Label(self.frame, text="Class")
        self.labelClass.grid(row=4,column=1)
        self.textClass = tk.Text(self.frame, height=1, width=25)
        self.textClass.grid(row=4,column=2)
        self.labelRoll = tk.Label(self.frame, text="Roll")
        self.labelRoll.grid(row=5,column=1)
        self.textRoll = tk.Text(self.frame, height=1, width=25)
        self.textRoll.grid(row=5,column=2)
        self.btn = tk.Button(self.frame, text="Snapshot!", width = 25, command=self.take_snapshot)
        self.btn.grid(row=6,column=1)
        self.quitButton = tk.Button(self.frame, text = 'Quit', width = 25, command = self.close_windows)
        self.quitButton.grid(row=6,column=2)
        self.frame.grid(row=2,column=2)
        self.video_loop()
        
    def video_loop(self):
      ok, frame = self.master.vs.read()
      if ok:
        key = cv2.waitKey(1000)
        self.cv2image = frame[:, :, ::-1]
        self.current_image = Image.fromarray(self.cv2image)
        imgtk = ImageTk.PhotoImage(image=self.current_image) 
        self.panel.imgtk = imgtk
        self.panel.config(image=imgtk)
      self.master.after(1, self.video_loop)
    
    def take_snapshot(self):
      matchLoc = face_recognition.face_locations(self.cv2image)
      matchEncodes = face_recognition.face_encodings(self.cv2image, matchLoc)
      headers = {"Content-Type": "application/json"}
      enrollData = {
      "fname" : self.textFname.get("1.0","end-1c"), 
      "lname" : self.textLname.get("1.0","end-1c"), 
      "class" : self.textClass.get("1.0","end-1c"),
      "roll"  : self.textRoll.get("1.0","end-1c"),
      "image" : matchEncodes[0].tolist()
      }
      URL = "http://localhost/enroll"
      res = requests.post(url=URL, data=json.dumps(enrollData), headers=headers)
      if res.status_code == 200:
        showinfo("Window", res.text)

    def close_windows(self):
      self.master.vs.release()
      self.master.destroy()

def main(): 
    root = tk.Tk()
    app = Home(root)
    root.mainloop()

if __name__ == '__main__':
    main()
