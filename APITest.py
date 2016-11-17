import requests
import json
import unittest

#Tests API calls
class manualAPITest(unittest.TestCase):

    def test_01_CreateUser(self):
        r = requests.post('http://localhost:5000/create_user', data=json.dumps({'user_info': {'username': 'walter', 'password': 'wat'}}))
        self.assertEquals("true", get_status_result(r.content))

    def test_02_LoggingInWithGoodCredentials(self):
        r = requests.get('http://localhost:5000/login', data=json.dumps({'user_info': {'username': 'walter', 'password': 'wat'}}))
        self.assertEquals("true", get_status_result(r.content))

    def test_03_LoggingInWithBadCredentials(self):
        r = requests.get('http://localhost:5000/login', data=json.dumps({'user_info': {'username': 'walter', 'password': 'nowat'}}))
        self.assertEquals("false", get_status_result(r.content))

    def test_04_Create2Tasks(self):
        requests.post('http://localhost:5000/create_user',
                      data=json.dumps({'user_info': {'username': 'joe', 'password': 'wat'}}))
        r = requests.post('http://localhost:5000/create_task',
                          data=json.dumps({'user_info': {'username': 'joe', 'password': 'wat'}, 'task':
                                                         {'name': 'good task',
                                                          'description': 'this is a task and it will be done',
                                                          'duedate': '1092941466',
                                                          'priority': 'omega',
                                                          'tag': 'things I hate to do',
                                                          'backgroundhex': '#000000',
                                                          'foregroundhex': '#000000'}}))
        self.assertEquals("true", get_status_result(r.content))
        r = requests.post('http://localhost:5000/create_task',
                          data=json.dumps({'user_info': {'username': 'joe', 'password': 'wat'}, 'task':
                                                          {'name': 'good task',
                                                          'description': 'this is a task and it will be done',
                                                          'duedate': '1092901466',
                                                          'priority': 'omega',
                                                          'tag': 'things I hate to do',
                                                          'backgroundhex': '#000000',
                                                          'foregroundhex': '#000000'}}))

        self.assertEquals("true", get_status_result(r.content))

    def test_05_CreateSubtask(self):
        r = requests.post('http://localhost:5000/create_subtask', data=json.dumps(
            {'parentid': '0', 'user_info': {'username': 'joe', 'password': 'wat'}, 'task':
                                            {'name': 'I AM A SUBTASK',
                                            'description': 'I DO NOT BELONG WITH NORMAL TASKS',
                                            'duedate': '1092938466',
                                            'priority': 'omega',
                                            'tag': 'things I hate to do',
                                            'backgroundhex': '#000000',
                                            'foregroundhex': '#000000'}}))
        self.assertEquals("true", get_status_result(r.content))

    def test_06_SeeActiveTasks(self):
        r = requests.get('http://localhost:5000/get_active_tasks',
                         data=json.dumps({'user_info': {'username': 'joe', 'password': 'wat'}}))
        # I had to leave out the datetime values because those will be different
        expected1 = ("""{"tasks": [{"description": "this is a task and it will be done","""
                                      """ "backgroundhex": "#000000",""")
        expected2 = (""" "completed": "f","""
                     """ "id": 1,"""
                     """ "priority": "omega","""
                     """ "tag": "things I hate to do","""
                     """ "completiontime": null,""")

        expected3 = (""" "foregroundhex": "#000000","""
                                      """ "subtaskof": null,"""
                                      """ "duedate": "2004-08-19 18:51:06","""
                                      """ "name": "good task"},""")
        expected4 = ("""{"description": "this is a task and it will be done","""
                                      """ "backgroundhex": "#000000",""")
        expected5 = (""" "completed": "f","""
                                      """ "id": 1,"""
                                      """ "priority": "omega","""
                                      """ "tag": "things I hate to do","""
                                      """ "completiontime": null,""")
        expected6 = (""" "foregroundhex": "#000000","""
                                      """ "subtaskof": null,"""
                                      """ "duedate": "2004-08-19 07:44:26","""
                                      """ "name": "good task"}]}""")
        self.assertTrue(expected1 in r.content)
        self.assertTrue(expected2 in r.content)
        self.assertTrue(expected3 in r.content)
        self.assertTrue(expected4 in r.content)
        self.assertTrue(expected5 in r.content)
        self.assertTrue(expected6 in r.content)

    def test_07_SeeNextEndingTask(self):
        r = requests.get('http://localhost:5000/get_next_countdown',
                         data=json.dumps({'user_info': {'username': 'joe', 'password': 'wat'}}))
        expected1 = ("""{"description": "this is a task and it will be done","""
                     """ "backgroundhex": "#000000",""")
        expected2 = (""" "completed": "f","""
                     """ "id": 1,"""
                     """ "priority": "omega","""
                     """ "tag": "things I hate to do","""
                     """ "completiontime": null,""")
        expected3 = (""" "foregroundhex": "#000000","""
                     """ "subtaskof": null,"""
                     """ "duedate": "2004-08-19 07:44:26","""
                     """ "name": "good task"}""")
        self.assertTrue(expected1 in r.content)
        self.assertTrue(expected2 in r.content)
        self.assertTrue(expected3 in r.content)

    def test_08_SeeSubtasksOfTask0(self):
        r = requests.post('http://localhost:5000/get_subtasks',
                          data=json.dumps({'parentid': '0', 'user_info': {'username': 'joe', 'password': 'wat'}}))
        expected1 = ("""{"tasks": [{"description": "I DO NOT BELONG WITH NORMAL TASKS","""
                     """ "backgroundhex": "#000000",""")
        expected2 = (""" "completed": "f","""
                     """ "id": 2,"""
                     """ "priority": "omega","""
                     """ "tag": "things I hate to do","""
                     """ "completiontime": null,""")
        expected3 = (""" "foregroundhex": "#000000","""
                     """ "subtaskof": 0,"""
                     """ "duedate": "2004-08-19 18:01:06","""
                     """ "name": "I AM A SUBTASK"}]}""")
        self.assertTrue(expected1 in r.content)
        self.assertTrue(expected2 in r.content)
        self.assertTrue(expected3 in r.content)

    def test_09_CompleteSubtask(self):
        r = requests.post('http://localhost:5000/complete_task',
                          data=json.dumps({'taskid': '2', 'user_info': {'username': 'joe', 'password': 'wat'}}))
        self.assertEquals("true", get_status_result(r.content))

    def test_10_CheckStatusOfSubtask(self):
        r = requests.post('http://localhost:5000/get_subtasks',
                          data=json.dumps({'parentid': '0', 'user_info': {'username': 'joe', 'password': 'wat'}}))
        expected1 = ("""{"tasks": [{"description": "I DO NOT BELONG WITH NORMAL TASKS","""
                     """ "backgroundhex": "#000000",""")
        expected2 = (""" "completed": "t","""
                     """ "id": 2,"""
                     """ "priority": "omega","""
                     """ "tag": "things I hate to do","""
                     """ "completiontime": null,""")
        expected3 = (""" "foregroundhex": "#000000","""
                     """ "subtaskof": 0,"""
                     """ "duedate": "2004-08-19 18:01:06","""
                     """ "name": "I AM A SUBTASK"}]}""")
        self.assertTrue(expected1 in r.content)
        self.assertTrue(expected2 in r.content)
        self.assertTrue(expected3 in r.content)

    def test_11_CompleteTask1(self):
        r = requests.post('http://localhost:5000/complete_task',
                          data=json.dumps({'taskid': '1', 'user_info': {'username': 'joe', 'password': 'wat'}}))
        self.assertEquals("true", get_status_result(r.content))
        # Verify that it's not in active tasks
        r = requests.get('http://localhost:5000/get_active_tasks',
                         data=json.dumps({'user_info': {'username': 'joe', 'password': 'wat'}}))
        self.assertTrue(""" "id": 1""" not in r.content)
        # Verify that it is in inactive tasks
        r = requests.get('http://localhost:5000/get_inactive_tasks', data=json.dumps({'user_info' :{'username':'joe', 'password': 'wat'}}))
        self.assertTrue(""" "id": 1""" in r.content)

    def test_12_UnarchiveTask1(self):
        r = requests.post('http://localhost:5000/unarchive_task',
                          data=json.dumps({'taskid': '1', 'user_info': {'username': 'joe', 'password': 'wat'}}))
        self.assertEquals("true", get_status_result(r.content))
        # Verify that it is in active tasks
        r = requests.get('http://localhost:5000/get_active_tasks',
                         data=json.dumps({'user_info': {'username': 'joe', 'password': 'wat'}}))
        self.assertTrue(""" "id": 1""" in r.content)

    def test_13_DeleteTask0(self):
        r = requests.post('http://localhost:5000/delete_task',
                          data=json.dumps({'taskid': '0', 'user_info': {'username': 'joe', 'password': 'wat'}}))
        self.assertEquals("true", get_status_result(r.content))
        # Verify that it's not in active tasks
        r = requests.get('http://localhost:5000/get_active_tasks',
                         data=json.dumps({'user_info': {'username': 'joe', 'password': 'wat'}}))
        self.assertTrue(""" "id": 0""" not in r.content)

    def test_14_EditTask1(self):
        r = requests.post('http://localhost:5000/edit_task',
                          data=json.dumps({'user_info': {'username': 'joe', 'password': 'wat'}, 'task':
                                                        {'id': '1',
                                                        'name': 'better task',
                                                        'description': 'this is a task and it has been modified',
                                                        'duedate': '1092901466',
                                                        'priority': 'swag',
                                                        'tag': 'wow',
                                                        'backgroundhex': '#1111',
                                                        'foregroundhex': '#1111'}}))
        self.assertEquals("true", get_status_result(r.content))
        # Verify the updates
        r = requests.get('http://localhost:5000/get_active_tasks',
                         data=json.dumps({'user_info': {'username': 'joe', 'password': 'wat'}}))
        expected1 = ("""{"description": "this is a task and it has been modified","""
                     """ "backgroundhex": "#1111",""")
        expected2 = (""" "completed": "f","""
                     """ "id": 1,"""
                     """ "priority": "swag","""
                     """ "tag": "wow","""
                     """ "completiontime": null,""")
        expected3 = (""" "foregroundhex": "#1111","""
                     """ "subtaskof": null,"""
                     """ "duedate": "2004-08-19 07:44:26","""
                     """ "name": "better task"}""")
        self.assertTrue(expected1 in r.content)
        self.assertTrue(expected2 in r.content)
        self.assertTrue(expected3 in r.content)


def get_status_result(str):
    status_result = str.split(" ")[1]
    if status_result.endswith("}"):
        status_result = status_result[:-1]
    return status_result



if __name__ == "__main__":
    unittest.main()
