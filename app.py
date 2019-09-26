from db import Database
from user import UserNow
from flask import Flask, render_template, json, request, session
from operator import itemgetter

app = Flask(__name__)

app.secret_key = 'seASdwe123asdWqKmnn'

db = Database(app)

resultUser = {'is_auth': "FALSE", 'user': {}}


@app.route('/')
def main():
    try:
        if 'hash_me' in session:
            auth = db.is_auth(session['hash_me'])
            if auth:
                resultUser['is_auth'] = "TRUE"

        if resultUser['is_auth'] == "TRUE":
            user_query = db.u_auth(session['hash_me'], "", "")
            resultUser['user'] = {
                'username': user_query[0][0],
                'uhash': user_query[0][1],
                'ip_address': user_query[0][2],
                'u_id': user_query[0][3]
            }
            return render_template('app.html', user=resultUser['user'])
        else:
            return render_template('whoAreYou.html')

    except Exception as e:
        session.pop('hash_me', None)
        return json.dumps({'error': str(e)})


@app.route('/logout', methods=['GET'])
def logout():
    session.pop('hash_me', None)
    return render_template('whoAreYou.html')


@app.route('/signIn', methods=['POST'])
def signIn():
    try:
        _username = request.form['userName']
        if _username:
            user = UserNow(_username, request.environ.get('HTTP_X_REAL_IP', request.remote_addr))
            db.u_auth(user.get_hash(), user.get_name(), user.get_ip())
            session['hash_me'] = user.get_hash()

            return json.dumps(
                {
                    'message': "user: {}, hash: {}, ip: {}".format(user.get_name(), user.get_hash(), user.get_ip())
                }
            )
        else:
            return json.dumps({'html': '<span>Enter the required fields</span>'})

    except Exception as e:
        return json.dumps({'error': str(e)})


@app.route('/getTasks', methods=['GET'])
def getTasks():
    try:
        db.list_check()
        my_tasks = db.list_task()
        tasks = []
        for oneTask in my_tasks:
            print(oneTask)
            sublist = []
            for sub in db.list_subtask(oneTask[0]):
                if sub[2] == 1:
                    checked = 'checked=checked'
                    my_class = 'completed'
                else:
                    checked = '0'
                    my_class = ''

                sublist.append(
                    {
                        'id': sub[0],
                        'name': sub[1],
                        'sub_completed': checked,
                        'class': my_class
                    }
                )


            tasks.append(
                {
                    'taskId': oneTask[0],
                    'taskName': oneTask[1],
                    'completed': oneTask[2],
                    'creator': oneTask[3],
                    'dateCreated': oneTask[4],
                    'count_sub': len(sublist),
                    'sublist': sublist
                }
            )
            tasks = sorted(tasks, key=itemgetter('completed'))
        return render_template('tasklist.html', tasks=tasks)
    except Exception as e:
        session.pop('hash_me', None)
        return json.dumps({'error': str(e)})


@app.route('/addTask', methods=['POST'])
def addTask():
    try:
        # db = Database()
        _taskname = request.form['taskName']

        # validate the received values
        if _taskname:
            # All Good, let's call MySQL
            # cursor = conn.cursor()
            # cursor.callproc('sp_AddTask', (_taskname))
            # data = cursor.fetchall()
            if 'hash_me' in session:
                auth = db.is_auth(session['hash_me'])
                if auth:
                    resultUser['is_auth'] = "TRUE"

            if resultUser['is_auth'] == "TRUE":
                user_query = db.u_auth(session['hash_me'], "", "")
                resultUser['user'] = {
                    'username': user_query[0][0],
                    'uhash': user_query[0][1],
                    'ip_address': user_query[0][2],
                    'u_id': user_query[0][3]
                }

            data = db.newTask(_taskname, resultUser['user']['u_id'])

            if len(data) is 0:
                db.commintMe()
                return json.dumps({'message': 'Task created successfully !'})
            else:
                return json.dumps({'error': str(data[0])})
        else:
            return json.dumps({'html': '<span>Enter the required fields</span>'})

    except Exception as e:
        return json.dumps({'error': str(e)})


@app.route('/addSubTask', methods=['POST'])
def addSubTask():
    try:
        _taskId = request.form['taskIdForSubtask']
        _subtaskname = request.form['subTaskName']

        # validate the received values
        if _subtaskname and _taskId:
            # All Good, let's call MySQL
            data = db.newSubTask(_taskId, _subtaskname)

            if len(data) is 0:
                db.commintMe()
                db.list_check()
                return json.dumps({'message': 'Subtask created successfully !'})
            else:
                return json.dumps({'error': str(data[0])})
        else:
            return json.dumps({'html': '<span>Enter the required fields</span>'})

    except Exception as e:
        return json.dumps({'error': str(e)})


@app.route('/completeSubTask', methods=['POST'])
def completeSubTask():
    try:
        data = request.form['taskId']
        # db = Database()
        # return json.dumps({'message': data})
        # validate the received values
        if data:
            # All Good, let's call MySQL
            data = db.completeSubTask(data)

            if len(data) is 0:
                db.commintMe()
                db.list_check()
                return json.dumps({'message': 'Subtask completed successfully !'})
            else:
                return json.dumps({'error': str(data[0])})
        else:
            return json.dumps({'html': '<span>Enter the required fields</span>'})

    except Exception as e:
        return json.dumps({'error': str(e)})


@app.route('/removeTask', methods=['POST'])
def removeTask():
    try:
        data = request.form['taskId']
        if data:
            data = db.removeTask(data)
            if len(data) is 0:
                db.commintMe()
                db.list_check()
                return json.dumps({'message': 'Task removed successfully !'})
            else:
                return json.dumps({'error': str(data[0])})
        else:
            return json.dumps({'html': '<span>Enter the required fields</span>'})

    except Exception as e:
        return json.dumps({'error': str(e)})


@app.route('/removeSubTask', methods=['POST'])
def removeSubTask():
    try:
        data = request.form['taskId']
        if data:
            data = db.removeSubTask(data)
            if len(data) is 0:
                db.commintMe()
                db.list_check()
                return json.dumps({'message': 'Subtask removed successfully !'})
            else:
                return json.dumps({'error': str(data[0])})
        else:
            return json.dumps({'html': '<span>Enter the required fields</span>'})

    except Exception as e:
        return json.dumps({'error': str(e)})


if __name__ == "__main__":
    app.run()
