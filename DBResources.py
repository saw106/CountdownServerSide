import sqlite3

def getNumUsers(conn=None):
    c = None;
    if conn is None:
        conn = sqlite3.connect('countdown.db')
    c = conn.cursor()
    rows = c.execute('''select count(*) from users''')
    for row in rows:
        return row[0]

def getNumTasks(conn=None):
    c = None;
    if conn is None:
        conn = sqlite3.connect('countdown.db')
    c = conn.cursor()
    rows = c.execute('''select count(*) from tasks''')
    for row in rows:
        return row[0]

def createUser(username, password, conn=None):
    c = None
    if conn is None:
        conn = sqlite3.connect('countdown.db')
    c = conn.cursor()

    c.execute('''INSERT INTO users VALUES ({}, '{}', '{}', DATETIME('now'))'''.format(getNumUsers(conn), username, password))
    conn.commit()

def createNewTask(userid, name, conn=None):
    c = None
    if conn is None:
        conn = sqlite3.connect('countdown.db')
    c = conn.cursor()

    newTaskID = getNumTasks()
    c.execute('''INSERT INTO tasks (id, name) VALUES ({}, '{}')'''.format(newTaskID, name))
    c.execute('''INSERT INTO hastask VALUES ({},{})'''.format(userid, newTaskID))
    conn.commit()

def getNextCountdown(userid, conn=None):
    c = None
    if conn is None:
        conn = sqlite3.connect('countdown.db')
    c = conn.cursor()

    rows = c.execute('''select * from tasks T where T.id in (select taskid from hastask where userid={})'''.format(userid))
    retarray = []
    for row in rows:
        retarray.append(row)
    return retarray

#used for testing
if __name__ == "__main__":
    conn = sqlite3.connect('countdown.db')
    # createUser('testuser', 'pw', conn=conn)
    # createNewTask(0, 'sometask1', conn=conn)
    print getNextCountdown(0, conn=conn)