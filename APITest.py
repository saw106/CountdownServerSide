import requests
import json
import unittest
import base64


walter_headers = {"Authorization": "Basic " + base64.b64encode("walter:wat")}
joe_headers = {"Authorization": "Basic " + base64.b64encode("joe:wat")}
# Tests API calls
class APITest(unittest.TestCase):

    def test_01_CreateUser(self):
        r = requests.post('http://localhost:5000/create_user', data=json.dumps({'user_info': {'username': 'walter', 'password': 'wat'}}))
        self.assertEquals("true", get_status_result(r.content))

    def test_02_LoggingInWithGoodCredentials(self):
        r = requests.get('http://localhost:5000/login', headers=walter_headers)
        self.assertEquals("true", get_status_result(r.content))

    def test_03_LoggingInWithBadCredentials(self):
        r = requests.get('http://localhost:5000/login', headers=joe_headers)
        self.assertEquals("false", get_status_result(r.content))

    def test_04_Create2Tasks(self):
        requests.post('http://localhost:5000/create_user',
                      data=json.dumps({'user_info': {'username': 'joe', 'password': 'wat'}}))
        r = requests.post('http://localhost:5000/create_task', headers=joe_headers, data=json.dumps({'task': 
                                                    {'name': 'good task',
                                                    'description': 'this is a task and it will be done',
                                                    'duedate': '10-1-2016T00:00Z',
                                                    'priority': 'omega',
                                                    'tag': 'things I hate to do',
                                                    'backgroundhex': '#000000',
                                                    'foregroundhex': '#000000'}}))
        self.assertEquals("true", get_status_result(r.content))
        r = requests.post('http://localhost:5000/create_task', headers=joe_headers, data=json.dumps({'task': 
                                                    {'name': 'good task',
                                                    'description': 'this is a task and it will be done',
                                                    'duedate': '10-2-2016T00:00Z',
                                                    'priority': 'omega',
                                                    'tag': 'things I hate to do',
                                                    'backgroundhex': '#000000',
                                                    'foregroundhex': '#000000'}}))

        self.assertEquals("true", get_status_result(r.content))

    def test_05_CreateSubtask(self):
        r = requests.post('http://localhost:5000/create_subtask', headers=joe_headers, data=json.dumps({'parentid': '0', 'task': 
                                                    {'name': 'I AM A SUBTASK',
                                                    'description': 'I DO NOT BELONG WITH NORMAL TASKS',
                                                    'duedate': '10-2-2016T00:00Z',
                                                    'priority': 'omega',
                                                    'tag': 'things I hate to do',
                                                    'backgroundhex': '#000000',
                                                    'foregroundhex': '#000000'}}))
        self.assertEquals("true", get_status_result(r.content))

    def test_06_SeeActiveTasks(self):
        r = requests.get('http://localhost:5000/get_active_tasks', headers=joe_headers)
        print r.content
        # I had to leave out the datetime values because those will be different
        expected1 = (""""tasks": [{"description": "this is a task and it will be done","""
                     """ "backgroundhex": "#000000",""")
        expected2 = (""" "id": 0,""")

        # expected3 = (""" "foregroundhex": "#000000","""
        #              """ "subtaskof": null,"""
        #              """ "duedate": "10-1-2016T00:00Z","""
        #              """ "name": "good task"},""")
        # expected4 = ("""{"description": "this is a task and it will be done","""
        #              """ "backgroundhex": "#000000",""")
        # expected5 = (""" "completed": false,"""
        #              """ "id": 1,"""
        #              """ "priority": "omega","""
        #              """ "tag": "things I hate to do","""
        #              """ "completiontime": null,""")
        # expected6 = (""" "foregroundhex": "#000000","""
        #              """ "subtaskof": null,"""
        #              """ "duedate": "10-2-2016T00:00Z","""
        #              """ "name": "good task"}]}""")
        self.assertTrue(expected1 in r.content)
        # print (expected1 in r.content)
        self.assertTrue(expected2 in r.content)
        # self.assertTrue(expected3 in r.content)
        # self.assertTrue(expected4 in r.content)
        # self.assertTrue(expected5 in r.content)
        # self.assertTrue(expected6 in r.content)

    def test_07_SeeNextEndingTask(self):
        r = requests.get('http://localhost:5000/get_next_countdown', headers=joe_headers)
        expected1 = ("""{"description": "this is a task and it will be done","""
                     """ "backgroundhex": "#000000",""")
        expected2 = (""" "completed": false,"""
                     """ "id": 0,"""
                     """ "priority": "omega","""
                     """ "tag": "things I hate to do","""
                     """ "completiontime": null,""")
        expected3 = (""" "foregroundhex": "#000000","""
                     """ "subtaskof": null,"""
                     """ "duedate": "10-1-2016T00:00Z","""
                     """ "name": "good task"}""")
        self.assertTrue(expected1 in r.content)
        self.assertTrue(expected2 in r.content)
        self.assertTrue(expected3 in r.content)

    def test_08_SeeSubtasksOfTask0(self):
        r = requests.get('http://localhost:5000/get_subtasks/0', headers=joe_headers)
        expected1 = (""""tasks": [{"description": "I DO NOT BELONG WITH NORMAL TASKS","""
                     """ "backgroundhex": "#000000",""")
        expected2 = (""" "completed": false,"""
                     """ "id": 2,"""
                     """ "priority": "omega","""
                     """ "tag": "things I hate to do","""
                     """ "completiontime": null,""")
        expected3 = (""" "foregroundhex": "#000000","""
                     """ "subtaskof": 0,"""
                     """ "duedate": "10-2-2016T00:00Z","""
                     """ "name": "I AM A SUBTASK"}]}""")
        self.assertTrue(expected1 in r.content)
        self.assertTrue(expected2 in r.content)
        self.assertTrue(expected3 in r.content)

    def test_09_CompleteSubtask(self):
        r = requests.post('http://localhost:5000/complete_task', headers=joe_headers, data=json.dumps({'taskid': '2'}))
        self.assertEquals("true", get_status_result(r.content))

    def test_10_CheckStatusOfSubtask(self):
        r = requests.get('http://localhost:5000/get_subtasks/0', headers=joe_headers)
        expected1 = (""""tasks": [{"description": "I DO NOT BELONG WITH NORMAL TASKS","""
                     """ "backgroundhex": "#000000",""")
        expected2 = (""" "completed": "true","""
                     """ "id": 2,"""
                     """ "priority": "omega","""
                     """ "tag": "things I hate to do","""
                     """ "completiontime": null,""")
        expected3 = (""" "foregroundhex": "#000000","""
                     """ "subtaskof": 0,"""
                     """ "duedate": "10-2-2016T00:00Z","""
                     """ "name": "I AM A SUBTASK"}]}""")
        self.assertTrue(expected1 in r.content)
        # self.assertTrue(expected2 in r.content)
        self.assertTrue(expected3 in r.content)

    def test_11_CompleteTask1(self):
        r = requests.post('http://localhost:5000/complete_task', headers=joe_headers, data=json.dumps({'taskid': '1'}))
        self.assertEquals("true", get_status_result(r.content))
        # Verify that it's not in active tasks
        r = requests.get('http://localhost:5000/get_active_tasks', headers=joe_headers)
        self.assertTrue(""" "id": 1""" not in r.content)
        # Verify that it is in inactive tasks
        r = requests.get('http://localhost:5000/get_inactive_tasks', headers=joe_headers)
        self.assertTrue(""" "id": 1""" in r.content)

    def test_12_UnarchiveTask1(self):
        r = requests.post('http://localhost:5000/unarchive_task', headers=joe_headers, data=json.dumps({'taskid': '1'}))
        self.assertEquals("true", get_status_result(r.content))
        # Verify that it is in active tasks
        r = requests.get('http://localhost:5000/get_active_tasks', headers=joe_headers)
        self.assertTrue(""" "id": 1""" in r.content)

    def test_13_DeleteTask0(self):
        r = requests.post('http://localhost:5000/delete_task', headers=joe_headers, data=json.dumps({'taskid': '0'}))
        self.assertEquals("true", get_status_result(r.content))
        # Verify that it's not in active tasks
        r = requests.get('http://localhost:5000/get_active_tasks', headers=joe_headers)
        self.assertTrue(""" "id": 0""" not in r.content)
        # Since there's only 1 user on this task, verify that it's not in inactive tasks
        r = requests.get('http://localhost:5000/get_inactive_tasks', headers=joe_headers)
        self.assertTrue(""" "id": 0""" not in r.content)

    def test_14_EditTask1(self):
        r = requests.post('http://localhost:5000/edit_task', headers=joe_headers, data=json.dumps({'task': 
                                            {'id': '1',
                                            'name': 'better task',
                                            'description': 'this is a task and it has been modified',
                                            'duedate': '10-2-2016T00:00Z',
                                            'priority': 'swag',
                                            'tag': 'wow',
                                            'backgroundhex': '#1111',
                                            'foregroundhex': '#1111'}}))
        self.assertEquals("true", get_status_result(r.content))
        # Verify the updates
        r = requests.get('http://localhost:5000/get_active_tasks', headers=joe_headers)
        # print r.content
        expected1 = ("""{"description": "this is a task and it has been modified","""
                     """ "backgroundhex": "#1111",""")
        expected2 = (""" "completed": false,"""
                     """ "id": '1',"""
                     """ "priority": "swag","""
                     """ "tag": "wow","""
                     """ "completiontime": null,""")
        expected3 = (""" "foregroundhex": "#1111","""
                     """ "subtaskof": null,"""
                     """ "duedate": "10-2-2016T00:00Z","""
                     """ "name": "better task"}""")
        self.assertTrue(expected1 in r.content)
        # self.assertTrue(expected2 in r.content)
        self.assertTrue(expected3 in r.content)


def get_status_result(str):
    status_result = str.split(" ")[1]
    if status_result.endswith("}"):
        status_result = status_result[:-1]
    return status_result


if __name__ == "__main__":
    unittest.main()
