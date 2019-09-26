from flaskext.mysql import MySQL


class Database:
    def __init__(self, app):
        self._app = app
        mysql = MySQL()
        # MySQL configurations
        app.config['MYSQL_DATABASE_USER'] = 'root'
        app.config['MYSQL_DATABASE_PASSWORD'] = 'Neydel3112'
        app.config['MYSQL_DATABASE_DB'] = 'flask'
        app.config['MYSQL_DATABASE_HOST'] = 'localhost'
        mysql.init_app(app)

        self._conn = mysql.connect()
        self.cur = self._conn.cursor()

    def list_check(self):
        self.cur.execute("SELECT id, task_name, completed, date_created, creatorId FROM `todolist`")
        pre_check = self.cur.fetchall()

        for w in pre_check:
            self.cur.execute("SELECT sid, task_id, subtask_name, sub_complited FROM subtask WHERE task_id = %s" % w[0])
            sub_list = self.cur.rowcount
            if sub_list > 0 and w[2] == 0:
                self.cur.execute("UPDATE `todolist` SET `completed` = 1 WHERE id=%s" % w[0])
                pre_check = self.cur.fetchall()
                self.commintMe()
                continue
            elif sub_list > 0 and w[2] != 0:
                self.cur.execute(
                    "SELECT sid, task_id, subtask_name, sub_complited FROM subtask WHERE task_id = %s AND sub_complited = 0" %
                    w[0])
                sub_count_list = self.cur.rowcount
                if sub_count_list == 0:
                    self.cur.execute("UPDATE `todolist` SET `completed` = 2 WHERE id=%s" % w[0])
                    self.cur.fetchall()
                    self.commintMe()
                    continue
                else:
                    self.cur.execute("UPDATE `todolist` SET `completed` = 1 WHERE id=%s" % w[0])
                    self.cur.fetchall()
                    self.commintMe()
                    continue
            elif sub_list == 0 and w[2] > 0:
                self.cur.execute("UPDATE `todolist` SET `completed` = 0 WHERE id=%s" % w[0])
                self.cur.fetchall()
                self.commintMe()
                continue

        return pre_check

    def list_task(self):
        self.cur.execute(
            "SELECT todolist.id, task_name, completed, users.username, date_created FROM `todolist` INNER JOIN users ON users.id=todolist.creatorId ORDER BY id DESC, completed ASC")
        resp = self.cur.fetchone()
        return resp

    def list_subtask(self, task_id):
        self.cur.execute(
            "SELECT sid, subtask_name, sub_complited  FROM subtask WHERE task_id=%s ORDER BY sub_complited ASC, date_created DESC" % task_id)
        result = self.cur.fetchall()
        return result

    def newTask(self, taskname, u_id):
        self.cur.execute("INSERT INTO `todolist`(`task_name`, `completed`, `creatorId`) VALUES ('{}','0','{}')".format(taskname, u_id))
        result = self.cur.fetchall()
        return result

    def newSubTask(self, task_id, subtaskname):
        self.cur.execute(
            "INSERT INTO `subtask`(`task_id`, `subtask_name`, `sub_complited`) VALUES ('{}', '{}', '0')".format(
                task_id, subtaskname))
        result = self.cur.fetchall()
        return result

    def completeSubTask(self, subId):
        self.cur.execute('UPDATE `subtask` SET `sub_complited` = 1 WHERE sid=%s' % subId)
        result = self.cur.fetchall()
        return result

    def removeTask(self, task_id):

        self.cur.execute('DELETE FROM `todolist` WHERE id=%s' % task_id)
        resultTask = self.cur.fetchall()
        self.commintMe()

        self.cur.execute('DELETE FROM `subtask` WHERE task_id=%s' % task_id)
        resultSub = self.cur.fetchall()
        return resultTask

    def removeSubTask(self, s_id):
        self.cur.execute('DELETE FROM `subtask` WHERE sid=%s' % s_id)
        result = self.cur.fetchall()
        return result

    def u_auth(self, uhash, username, ip):
        auth = self.is_auth(uhash)
        if auth:
            self.cur.execute(
                "SELECT username, uhash, ip_address, id FROM `users` WHERE uhash = '{}'".format(uhash))
            result = self.cur.fetchall()
            return result
        else:
            self.cur.execute(
                "INSERT INTO `users`(`username`, `ip_address`, `uhash`) VALUES ('{}','{}','{}')".format(
                    username, ip, uhash))
            result = self.cur.fetchall()
            self.commintMe()
            return result

    def is_auth(self, uhash):
        self.cur.execute(
            "SELECT * FROM `users` WHERE uhash = '{}'".format(uhash))
        count = self.cur.rowcount
        if count == 0:
            return False
        else:
            return True

    def commintMe(self):
        self._conn.commit()
        return

    def closeMe(self):
        self.cur.close()
        self._conn.close()
        return
