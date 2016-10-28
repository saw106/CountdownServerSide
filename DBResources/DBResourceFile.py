import sqlite3

TASK_COLUMNS = ['id', 'name', 'description', 'duedate', 'priority', 'tag', 'backgroundhex', 'foregroundhex', 'datecreated', 'lastmodified', 'completed', 'completiontime']

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
    print "Created new User {}".format(username)
    conn.commit()

def doesUserExist(username, conn=None):
    c = None
    if conn is None:
        conn = sqlite3.connect('countdown.db')
    c = conn.cursor()

    rows = c.execute('''select * from users where username='{}' '''.format(username))
    for row in rows:
        return True
    return False

def getUserId(username, conn=None):
    if conn is None:
        conn = sqlite3.connect('countdown.db')
    c = conn.cursor()
    
    rows = c.execute('''select * from users where username='{}' '''.format(username))
    for row in rows:
        return row[0]
    return -1


def createTask(userid, name, conn=None):
    c = None
    if conn is None:
        conn = sqlite3.connect('countdown.db')
    c = conn.cursor()

    newTaskID = getNumTasks(conn)
    c.execute('''INSERT INTO tasks (id, name, completed) VALUES ({}, '{}', 'f')'''.format(newTaskID, name))
    c.execute('''INSERT INTO hastask VALUES ({},{})'''.format(userid, newTaskID))
    print "Created New task for {}".format(userid)
    conn.commit()

def getActiveTasksForUser(userid, conn=None):
    if conn is None:
        conn = sqlite3.connect('countdown.db')
    c = conn.cursor()
    tasks = []
    for row in c.execute('''select * from tasks where completed='f' and id in (select taskid from hastask where userid={})'''.format(userid)):
        task = {}
        i = 0
        for column_name in TASK_COLUMNS:
            task[column_name] = row[i]
            i += 1
        tasks.append(task)
    return tasks


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
    print getActiveTasksForUser(0)