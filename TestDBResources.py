import unittest
from DBResources import *
import sqlite3

# Common fields
test_db_conn = sqlite3.connect('countdown_test.db')
test_user_name = "test_user_123"
test_password = "test_password_123"

# Tests functions in DBResources
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
        # Check that the user was actually created
        r = c.execute('''SELECT * FROM users U WHERE U.username='{}' AND U.password='{}' '''.format(test_user_name, test_password)).fetchone()
        self.assertIsNotNone(r)
        self.assertEquals(test_user_name, r['username'])
        self.assertEquals(test_password, r['password'])
        # Delete the test user
        c.execute('''DELETE FROM users WHERE users.username='{}' AND users.password='{}' '''.format(test_user_name, test_password)).fetchone()

    def testDoesUserExist(self):
        # user_1 was created in setUpTestDB
        self.assertTrue(doesUserExist("user_1", test_db_conn))
        self.assertFalse(doesUserExist("some_random_user_123456", test_db_conn))

    def testGetUserId(self):
        # user_1 and user_2 were created in setUpTestDB
        self.assertEquals(0, getUserId("user_1", test_db_conn))
        self.assertEquals(1, getUserId("user_2", test_db_conn))

    def testCreateNewTask(self):
        test_task_name = "test_name_123"
        user_1_id = 0
        createTask(user_1_id, test_task_name, test_db_conn)
        test_conn = test_db_conn
        test_conn.row_factory = sqlite3.Row
        c = test_conn.cursor()
        # Check that the task was actually created in tasks
        r = c.execute('''SELECT * FROM tasks T WHERE T.name=\'{}\''''.format(test_task_name)).fetchone()
        self.assertIsNotNone(r)
        self.assertEquals(test_task_name, r['name'])
        task_id = r['id']
        # Check that the task was actually created in hastask with correct userid and taskid
        r2 = c.execute('''SELECT * FROM hastask H WHERE H.userid={} AND H.taskid={}'''.format(user_1_id, task_id)).fetchone()
        self.assertIsNotNone(r2)
        # Delete the test task
        c.execute('''DELETE FROM tasks WHERE tasks.name='{}' '''.format(test_task_name))
        c.execute('''DELETE FROM hastask WHERE hastask.userid={} AND hastask.taskid={}'''.format(user_1_id, task_id))

    def testGetActiveTasksForUser(self):
        # Users with ids 0 and 1 were created in setUpTestDB with 3 and 1 active tasks, respectively
        tasks_for_0 = getActiveTasksForUser(0, test_db_conn)
        self.assertEquals(3, len(tasks_for_0))
        tasks_for_1 = getActiveTasksForUser(1, test_db_conn)
        self.assertEquals(1, len(tasks_for_1))

if __name__ == '__main__':
    unittest.main()