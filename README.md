mysql table

mysql>create table attend (rn INT not null, class varchar(100) NOT NULL, time datetime not null default CURRENT_TIMESTAMP);

mysql>CREATE TABLE student (rn INT PRIMARY KEY, fname VARCHAR(100) NOT NULL, lname VARCHAR(100) NOT NULL, image BLOB NOT NULL, class VARCHAR(100) NOT NULL);

Start Server
>sudo python server.py

Enroll Student
>python admin.py

Detect Face
>python detect.py
