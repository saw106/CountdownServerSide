import sqlite3
from DBResources import *

conn = sqlite3.connect('countdown.db')

c = conn.cursor()

c.execute('''CREATE TABLE users
            (id INT NOT NULL, username, password, creation_date DATETIME, PRIMARY KEY (id))''')
c.execute('''CREATE TABLE tasks
            (id INT NOT NULL, name, description, duedate DATETIME, priority, tag, backgroundhex, foregroundhex, datecreated DATETIME, lastmodified DATETIME, completed, completiontime DATETIME, PRIMARY KEY (id))''')
c.execute('''CREATE TABLE hastask
            (userid INT NOT NULL, taskid INT NOT NULL, PRIMARY KEY(userid, taskid), FOREIGN KEY (userid) REFERENCES users(id), FOREIGN KEY (taskid) REFERENCES tasks(id))''')
c.execute
conn.commit()

