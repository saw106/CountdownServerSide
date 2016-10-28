import unittest
from DBResources import *
import sqlite3

test_db_conn = sqlite3.connect('countdown_test.db')
test_user_name = "test_user_123"
test_password = "test_password_123"

class TestDBResources(unittest.TestCase):

    def testGetNumUsers(self):
        self.assertEqual(3, getNumUsers(test_db_conn))

    def testGetNumTasks(self):
        self.assertEquals(7, getNumTasks(test_db_conn))

    def testCreateNewUser(self):
        createUser(test_user_name, test_password, test_db_conn)
        test_conn = test_db_conn
        test_conn.row_factory = sqlite3.Row
        c = test_conn.cursor()
        r = c.execute('''SELECT * FROM users U WHERE U.username='{}' AND U.password='{}' '''.format(test_user_name, test_password)).fetchone()
        self.assertIsNotNone(r)
        self.assertEquals(test_user_name, r['username'])
        self.assertEquals(test_password, r['password'])
        c.execute('''DELETE FROM users WHERE users.username='{}' AND users.password='{}' '''.format(test_user_name, test_password)).fetchone()

    def testCreateNewTask(self):
        test_task_name = "test_name_123"
        user_1_username = "user_1"
        user_1_id = 0
        createNewTask(user_1_id, test_task_name, test_db_conn)
        conn = test_db_conn
        conn.row_factory = sqlite3.Row
        c = conn.cursor()
        r = c.execute('''SELECT * FROM tasks T WHERE T.name=\'{}\''''.format(test_task_name)).fetchone()
        self.assertIsNotNone(r)
        self.assertEquals(test_task_name, r['name'])
        task_id = r['id']
        r2 = c.execute('''SELECT * FROM hastask H WHERE H.userid={} AND H.taskid={}'''.format(user_1_id, task_id)).fetchone()
        self.assertIsNotNone(r2)
        c.execute('''DELETE FROM tasks WHERE tasks.name='{}' '''.format(test_task_name))
        c.execute('''DELETE FROM hastask WHERE hastask.userid={} AND hastask.taskid={}'''.format(user_1_id, task_id))
