import sqlite3
import datetime
from DBResources import *

conn = sqlite3.connect('countdown_test.db')

c = conn.cursor()

c.execute('''CREATE TABLE users
            (id INT NOT NULL, username, password, creation_date DATETIME, PRIMARY KEY (id))''')
c.execute('''CREATE TABLE tasks
            (id INT NOT NULL, name, description, duedate DATETIME, priority, tag, backgroundhex, foregroundhex,
             datecreated DATETIME, lastmodified DATETIME, completed, completiontime DATETIME, PRIMARY KEY (id))''')
c.execute('''CREATE TABLE hastask
            (userid INT NOT NULL, taskid INT NOT NULL, PRIMARY KEY(userid, taskid), FOREIGN KEY (userid) REFERENCES users(id),
             FOREIGN KEY (taskid) REFERENCES tasks(id))''')

c.execute('''INSERT INTO users
             VALUES (1, "user_1", "password_1", datetime.datetime(2016,9,1,0,0,0))''')
c.execute('''INSERT INTO users
             VALUES (2, "user_2", "password_2", datetime.datetime(2016,9,2,0,0,0))''')
c.execute('''INSERT INTO users
             VALUES (3, "user_3", "password_3", datetime.datetime(2016,9,3,0,0,0))''')

c.execute('''INSERT INTO tasks
             VALUES (11, "task_1", "description_1", datetime.datetime(2016,11,1,10,0,0), "1", "tag_1", "AAAAAA", "BBBBBB",
                     datetime.datetime(2016,10,1), datetime.datetime(2016,10,26), "true",
                     datetime.datetime(2016,10,26))''')
c.execute('''INSERT INTO tasks
             VALUES (12, "task_2", "description_2", datetime.datetime(2016,11,15,12,30,0), "2", "tag_1", "FFFFFF", "BBBBBB",
                     datetime.datetime(2016,10,1), datetime.datetime(2016,10,1), "false", null)''')
c.execute('''INSERT INTO tasks
             VALUES (13, "task_3", "description_3", datetime.datetime(2016,11,1), "1", "tag_2", "AAAAAA", "BBBBBB",
                     datetime.datetime(2016,10,1), datetime.datetime(2016,10,1), "false", null)''')
c.execute('''INSERT INTO tasks
             VALUES (14, "task_4", "description_4", datetime.datetime(2016,11,1,15,0,0), "3", "tag_2", "AAAAAA", "DDDDDD",
                     datetime.datetime(2016,10,1), datetime.datetime(2016,10,1), "false", null)''')
c.execute('''INSERT INTO tasks
             VALUES (15, "task_5", "description_5", datetime.datetime(2016,10,14), "2", "tag_3", "AAAAAA", "BBBBBB",
                    datetime.datetime(2016,10,1), datetime.datetime(2016,10,15), "true", datetime.datetime(2016,10,15))''')
c.execute('''INSERT INTO tasks
             VALUES (16, "task_6", "description_6", datetime.datetime(2016,11,1,10,0,0), "1", "tag_1", "CCCCCC", "BBBBBB",
                    datetime.datetime(2016,10,1), datetime.datetime(2016,10,1), "false", null)''')
c.execute('''INSERT INTO tasks
             VALUES (17, "task_7", "description_7", datetime.datetime(2016,11,1,7,30,0), "2", "tag_4", "AAAAAA", "BBBBBB",
                     datetime.datetime(2016,10,1), datetime.datetime(2016,10,1), "false", null)''')

c.execute('''INSERT INTO hastask
             VALUES (1, 11)''')
c.execute('''INSERT INTO hastask
             VALUES (1, 12)''')
c.execute('''INSERT INTO hastask
             VALUES (1, 13)''')
c.execute('''INSERT INTO hastask
             VALUES (1, 14)''')
c.execute('''INSERT INTO hastask
             VALUES (2, 15)''')
c.execute('''INSERT INTO hastask
             VALUES (2, 16)''')
c.execute('''INSERT INTO hastask
             VALUES (3, 17)''')


c.execute
conn.commit()
