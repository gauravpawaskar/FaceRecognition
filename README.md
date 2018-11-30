mysql table
mysql>CREATE TABLE student (rn INT PRIMARY KEY, fname VARCHAR(100) NOT NULL, lname VARCHAR(100) NOT NULL, image BLOB NOT NULL, class VARCHAR(100) NOT NULL);

Start Server
>sudo python server.py

Enroll Student
>python admin.py

Detect Face
>python detect.py
