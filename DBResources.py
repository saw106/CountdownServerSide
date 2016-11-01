import sqlite3


class DBResource:
    TASK_COLUMNS = ['id', 'name', 'description', 'duedate', 'priority', 'tag', 'backgroundhex', 'foregroundhex', 'datecreated', 'lastmodified', 'completed', 'completiontime']

    def __init__(self, user_info=None, conn=None) :
        self.user_info = user_info
        if conn is None:
            self.conn = sqlite3.connect('countdown.db')
        else:
            self.conn = conn
        self.cursor = conn.cursor()

    def checkUserCredentials(self, func):
        def func_wrapper(*args, **kwargs):
            if (verifyPassword):
                return fun(*args, **kwargs)
            return {'Error': 'User {} given with invalid password.'}
        return func_wrapper

    def verifyPassword(self):
        rows = self.cursor.execute('''select * from users where username='{}' and password='{}' '''.format(self.user_info['username', self.user_info['password']]))
        for row in rows:
            return True
        return False

    def getNumUsers(conn=None):
        rows = self.cursor.execute('''select count(*) from users''')
        for row in rows:
            return row[0]

    def getNumTasks(conn=None):
        rows = self.cursor.execute('''select count(*) from tasks''')
        for row in rows:
            return row[0]

    def createUser(username, password):
        self.cursor.execute('''INSERT INTO users VALUES ({}, '{}', '{}', DATETIME('now'))'''.format(getNumUsers(conn), username, password))
        print "Created new User {}".format(username)
        self.conn.commit()

    def doesUserExist(username):
        rows = self.cursor.execute('''select * from users where username='{}' '''.format(username))
        for row in rows:
            return True
        return False

    def getUserId(username):
        rows = self.cursor.execute('''select * from users where username='{}' '''.format(username))
        for row in rows:
            return row[0]
        return -1


    @checkUserCredentials
    def createTask(name):
        newTaskID = self.getNumTasks()
        self.cursor.execute('''INSERT INTO tasks (id, name, completed) VALUES ({}, '{}', 'f')'''.format(newTaskID, name))
        self.cursor.execute('''INSERT INTO hastask VALUES ({},{})'''.format(userid, newTaskID))
        print "Created New task for {}".format(userid)
        self.conn.commit()

    @checkUserCredentials
    def getActiveTasksForUser(self):
        tasks = []
        for row in self.cursor.execute('''select * from tasks where completed='f' and id in (select taskid from hastask where userid={})'''.format(userid)):
            task = {}
            i = 0
            for column_name in TASK_COLUMNS:
                task[column_name] = row[i]
                i += 1
            tasks.append(task)
        return tasks

    @checkUserCredentials
    def getNextCountdown(self):
        rows = self.cursor.execute('''select * from tasks T where T.id in (select taskid from hastask where userid={})'''.format(userid))
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