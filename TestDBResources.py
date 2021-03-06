import unittest
from DBResources import *
import sqlite3

# Common fields
test_db_conn = sqlite3.connect('countdown_test.db')
test_user_info = {'username': "test_user_123", 'password': 'test_password_123'}

# Tests functions in DBResources
class TestDBResources(unittest.TestCase):

    def setUp(self):
        self.db = DBResource(conn=test_db_conn)

    def tearDown(self):
        pass

    def testGetNewUserID(self):
        self.assertEqual(2, self.db.getMaxUserId())

    def testGetNewTaskID(self):
        self.assertEquals(18, self.db.getMaxTaskId())

    def testVerifyPassword(self):
        self.db.user_info = {'username': 'user_1', 'password': 'password_1'}
        self.assertTrue(self.db.verifyPassword())

    def testCreateNewUser(self):
        self.db.user_info = test_user_info
        self.db.createUser()
        test_user_name = test_user_info['username']
        test_password = test_user_info['password']
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
        test_conn.commit()

    def testDoesUserExist(self):
        # user_1 was created in setUpTestDB
        self.db.user_info = {'username': 'user_1', 'password': 'doesnt matter'}
        self.assertTrue(self.db.doesUserExist())
        self.db.user_info['username'] = 'some_random_user_123456'
        self.assertFalse(self.db.doesUserExist())

    def testGetUserId(self):
        # user_1 and user_2 were created in setUpTestDB
        self.assertEquals(0, self.db.getUserId("user_1"))
        self.assertEquals(1, self.db.getUserId("user_2"))

    def testGetMaxTaskId(self):
        self.assertEquals(18, self.db.getMaxTaskId())

    def testGetMaxUserId(self):
        self.assertEquals(2, self.db.getMaxUserId())

    def testCreateNewTask(self):
        self.db.user_info = test_user_info
        test_task = {'name': 'test_name_123',
                    'description': 'this is a task and it will be done',
                    'duedate': '2016-10-1T00:00Z',
                    'priority': 'omega',
                    'tag': 'things I hate to do',
                    'backgroundhex': '#000000',
                    'foregroundhex': '#000000'}
        self.db.createUser()
        self.db.createTask(test_task)
        test_conn = self.db.conn
        test_conn.row_factory = sqlite3.Row
        c = test_conn.cursor()
        # Check that the task was actually created in tasks
        r = c.execute('''SELECT * FROM tasks T WHERE T.name='{}' '''.format(test_task['name'])).fetchone()
        self.assertIsNotNone(r)
        self.assertEquals(test_task['name'], r['name'])
        task_id = r['id']
        user_1_id = self.db.getCurrentUserId()
        # Check that the task was actually created in hastask with correct userid and taskid
        r2 = c.execute('''SELECT * FROM hastask H WHERE H.userid={} AND H.taskid={}'''.format(user_1_id, task_id)).fetchone()
        self.assertIsNotNone(r2)
        # Delete the test task
        c.execute('''DELETE FROM tasks WHERE tasks.name='{}' '''.format(test_task['name']))
        c.execute('''DELETE FROM hastask WHERE hastask.userid={} AND hastask.taskid={}'''.format(user_1_id, task_id))
        test_conn.commit()

    def testGetActiveTasksForUser(self):
        # Users with ids 0 and 1 were created in setUpTestDB with 3 and 1 active tasks, respectively
        self.db.user_info = {'username': 'user_1', 'password': 'password_1'}
        tasks_for_0 = self.db.getActiveTasksForUser()
        self.assertEquals(3, len(tasks_for_0))
        self.db.user_info = {'username': 'user_2', 'password': 'password_2'}
        tasks_for_1 = self.db.getActiveTasksForUser()
        self.assertEquals(1, len(tasks_for_1))

    def testUnarchiveTask(self):
        self.db.user_info = {'username': 'user_1', 'password': 'password_1'}
        self.db.completeTask(12)
        self.db.unarchiveTask(12)
        task = self.db.getTask(12)
        self.assertFalse(task['completed'])

    def testCompleteTask(self):
        self.db.user_info = {'username': 'user_1', 'password': 'password_1'}
        self.db.completeTask(12)
        task = self.db.getTask(12)
        self.assertTrue(task['completed'])
        self.db.unarchiveTask(12)

    def testHasAccessToTask(self):
        self.db.user_info = {'username': 'user_1', 'password': 'password_1'}
        self.assertTrue(self.db.hasAccessToTask(11))
        self.assertFalse(self.db.hasAccessToTask(17))

    def testDeleteTask(self):
        self.db.user_info = {'username': 'user_1', 'password': 'password_1'}
        test_task = {'name': 'test_name_123',
                    'description': 'this is a task and it will be done',
                    'duedate': '2016-10-1T00:00Z',
                    'priority': 'omega',
                    'tag': 'things I hate to do',
                    'backgroundhex': '#000000',
                    'foregroundhex': '#000000'}
        task_id = self.db.createTask(test_task)
        self.db.deleteTask(task_id)
        task = self.db.getTask(task_id)
        self.assertEquals(task, None)

    def testGetTask(self):
        self.db.user_info = {'username': 'user_1', 'password': 'password_1'}
        task_from_db = self.db.getTask(11)
        self.assertEquals(task_from_db['name'], 'task_1')

    def testEditTask(self):
        self.db.user_info = {'username': 'user_1', 'password': 'password_1'}
        test_task = {'name': 'test_name_123',
                    'description': 'this is a task and it will be done',
                    'duedate': '2016-10-1T00:00Z',
                    'priority': 'omega',
                    'tag': 'things I hate to do',
                    'backgroundhex': '#000000',
                    'foregroundhex': '#000000'}
        task_id = self.db.createTask(test_task)
        test_task['name'] = "new test_name"
        test_task['id'] = task_id
        self.db.editTask(test_task)
        task_from_db = self.db.getTask(task_id)
        self.db.deleteTask(task_id)
        self.assertEquals(task_from_db['name'], 'new test_name')

    def testTimeConversion(self):
        self.db.user_info = {'username': 'user_1', 'password': 'password_1'}
        goodly_formatted_string = "2016/10/4T12:30Z"
        new_date_string = self.db.turnTimeIntoISO8601Time("2016/10/4 12:30")
        self.assertEquals(goodly_formatted_string, new_date_string)

    def testGetArchivedTasksForUser(self):
        # Users with ids 0, 1, 2 were created in setUpTestDB with 1, 1, and 0 active tasks, respectively
        self.db.user_info = {'username': 'user_1', 'password': 'password_1'}
        tasks_for_0 = self.db.getArchivedTasksForUser()
        self.assertEquals(1, len(tasks_for_0))
        self.db.user_info = {'username': 'user_2', 'password': 'password_2'}
        tasks_for_1 = self.db.getArchivedTasksForUser()
        self.assertEquals(1, len(tasks_for_1))
        self.db.user_info = {'username': 'user_3', 'password': 'password_3'}
        tasks_for_2 = self.db.getArchivedTasksForUser()
        self.assertEquals(0, len(tasks_for_2))

    def testGetSubtasksForTask(self):
        self.db.user_info = {'username': 'user_1', 'password': 'password_1'}
        subtasks_for_11 = self.db.getSubTasksForTask(11)
        self.assertEquals(0, len(subtasks_for_11))
        self.db.user_info = {'username': 'user_3', 'password': 'password_3'}
        subtasks_for_17 = self.db.getSubTasksForTask(17)
        self.assertEquals(1, len(subtasks_for_17))

    def testGetNextCountdown(self):
        self.db.user_info = {'username': 'user_1', 'password': 'password_1'}
        countdown_1 = self.db.getNextCountdown()
        self.assertEquals(13, countdown_1['id'])
        self.db.user_info = {'username': 'user_3', 'password': 'password_3'}
        countdown_3 = self.db.getNextCountdown()
        self.assertEquals(17, countdown_3['id'])

if __name__ == '__main__':
    unittest.main()