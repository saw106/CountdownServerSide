import sqlite3

TASK_COLUMNS = ['id', 'name', 'description', 'duedate', 'priority', 'tag', 'backgroundhex', 'foregroundhex', 'datecreated', 'lastmodified', 'completed', 'completiontime']

class DBResource:

    def __init__(self, user_info=None, conn=None) :
        self.user_info = user_info
        if conn is None:
            self.conn = sqlite3.connect('countdown.db')
        else:
            self.conn = conn
        self.cursor = self.conn.cursor()

    def checkUserCredentials(func):
        def func_wrapper(*args, **kwargs):
            if (args[0].verifyPassword()):
                return func(*args, **kwargs)
            return {'Error': 'User {} given with invalid password.'.format(args[0].user_info['username'])}
        return func_wrapper

    def verifyPassword(self):
        rows = self.cursor.execute('''select * from users where username='{}' and password='{}' '''.format(self.user_info['username'], self.user_info['password']))
        for row in rows:
            return True
        return False

    def getNumUsers(self):
        rows = self.cursor.execute('''select count(*) from users''')
        for row in rows:
            return row[0]

    def getNumTasks(self):
        rows = self.cursor.execute('''select count(*) from tasks''')
        for row in rows:
            return row[0]

    def createUser(self):
        self.cursor.execute('''INSERT INTO users VALUES ({}, '{}', '{}', DATETIME('now'))'''.format(self.getNumUsers(), self.user_info['username'], self.user_info['password'])).fetchall()
        print "Created new User {}".format(self.user_info['username'])
        self.conn.commit()

    def doesUserExist(self):
        rows = self.cursor.execute('''select * from users where username='{}' '''.format(self.user_info['username']))
        for row in rows:
            return True
        return False

    def getUserId(self, username):
        for row in self.cursor.execute('''select * from users where username='{}' '''.format(username)):
            return row[0]
        return -1

    def getCurrentUserId(self):
        return self.getUserId(self.user_info['username'])

    @checkUserCredentials
    def createTask(self, task):
        task['id'] = self.getNumTasks()
        userid = self.getCurrentUserId()
        self.cursor.execute('''INSERT INTO tasks VALUES ({id}, '{name}', '{description}', DATETIME('{duedate}', 'unixepoch'), '{priority}', '{tag}', '{backgroundhex}', '{foregroundhex}', DATETIME('now'), DATETIME('now'), 'f', NULL)'''.format(**task))
        self.cursor.execute('''INSERT INTO hastask VALUES ({},{})'''.format(userid, task['id']))
        print "Created New task for {}".format(self.user_info['username'])
        self.conn.commit()

    @checkUserCredentials
    def getActiveTasksForUser(self):
        tasks = []
        userid = self.getCurrentUserId()
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