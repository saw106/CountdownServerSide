import sqlite3

conn = sqlite3.connect('countdown_test.db')

c = conn.cursor()

c.execute("DROP TABLE IF EXISTS users")
c.execute("DROP TABLE IF EXISTS tasks")
c.execute("DROP TABLE IF EXISTS hastask")

c.execute('''CREATE TABLE users
            (id INT NOT NULL, username, password, creation_date DATETIME, PRIMARY KEY (id))''')

c.execute('''CREATE TABLE tasks
            (id INT NOT NULL, name, description, duedate DATETIME, priority, tag, backgroundhex, 
            foregroundhex, datecreated DATETIME, lastmodified DATETIME, completed, completiontime DATETIME, 
            subtaskof INT, PRIMARY KEY (id), FOREIGN KEY (subtaskof) REFERENCES tasks(id))''')
c.execute('''CREATE TABLE hastask
            (userid INT NOT NULL, taskid INT NOT NULL, PRIMARY KEY(userid, taskid), FOREIGN KEY (userid) REFERENCES users(id),
             FOREIGN KEY (taskid) REFERENCES tasks(id))''')

c.execute('''INSERT INTO users
             VALUES (0, "user_1", "password_1", "2016-1-9T00:00Z")''')
c.execute('''INSERT INTO users
             VALUES (1, "user_2", "password_2", "2016-2-9T00:00Z")''')
c.execute('''INSERT INTO users
             VALUES (2, "user_3", "password_3", "2016-3-9T00:00Z")''')

c.execute('''INSERT INTO tasks
             VALUES (11, "task_1", "description_1", "11-12016T00:00Z", "1", "tag_1", "AAAAAA", "BBBBBB",
                     "2016-1-10T00:00Z", "2016-26-10T00:00Z", "true",
                     "2016-26-10T00:00Z", NULL)''')
c.execute('''INSERT INTO tasks
             VALUES (12, "task_2", "description_2", "11/15/2016T12:30Z 12:30PM", "2", "tag_1", "FFFFFF", "BBBBBB",
                     "2016-1-10T00:00Z", "2016-1-10T00:00Z", "false", null, NULL)''')
c.execute('''INSERT INTO tasks
             VALUES (13, "task_3", "description_3", "2016-1-11T00:00Z", "1", "tag_2", "AAAAAA", "BBBBBB",
                     "2016-1-10T00:00Z", "2016-1-10T00:00Z", "false", null, NULL)''')
c.execute('''INSERT INTO tasks
             VALUES (14, "task_4", "description_4", "2016-1-11T15:00Z", "3", "tag_2", "AAAAAA", "DDDDDD",
                     "2016-1-10T00:00Z", "2016-1-10T00:00Z", "false", null, NULL)''')
c.execute('''INSERT INTO tasks
             VALUES (15, "task_5", "description_5", "2016-14-10T00:00Z", "2", "tag_3", "AAAAAA", "BBBBBB",
                    "2016-1-10T00:00Z", "2016-15-10T00:00Z", "true", "2016-15-10T00:00Z", NULL)''')
c.execute('''INSERT INTO tasks
             VALUES (16, "task_6", "description_6", "2016-1-11T00:00Z", "1", "tag_1", "CCCCCC", "BBBBBB",
                    "2016-1-10T00:00Z", "2016-1-10T00:00Z", "false", null, NULL)''')
c.execute('''INSERT INTO tasks
             VALUES (17, "task_7", "description_7", "2016-1-11T07:30Z", "2", "tag_4", "AAAAAA", "BBBBBB",
                     "2016-1-10T00:00Z", "2016-1-10T00:00Z", "false", null, NULL)''')

c.execute('''INSERT INTO hastask
             VALUES (0, 11)''')
c.execute('''INSERT INTO hastask
             VALUES (0, 12)''')
c.execute('''INSERT INTO hastask
             VALUES (0, 13)''')
c.execute('''INSERT INTO hastask
             VALUES (0, 14)''')
c.execute('''INSERT INTO hastask
             VALUES (1, 15)''')
c.execute('''INSERT INTO hastask
             VALUES (1, 16)''')
c.execute('''INSERT INTO hastask
             VALUES (2, 17)''')


c.execute
conn.commit()
