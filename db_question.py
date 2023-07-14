"""
用于连接数据库，并且随机查询10条题目
"""

import pymysql


class Database:
    def __init__(self, host, port, user, password, database):
        self.host = host
        self.port = port
        self.user = user
        self.password = password
        self.database = database
        self.connection = None

    def connect(self):
        self.connection = pymysql.connect(
            host=self.host,
            port=self.port,
            user=self.user,
            password=self.password,
            charset='utf8mb4',
            database=self.database
        )

    def close(self):
        if self.connection:
            self.connection.close()

    def execute_query(self, sql):
        try:
            with self.connection.cursor() as cursor:
                cursor.execute(sql)
                results = cursor.fetchall()
                return results
        except (pymysql.OperationalError, pymysql.InterfaceError):
            # 连接异常，尝试重新连接
            try:
                self.connect()
                with self.connection.cursor() as cursor:
                    cursor.execute(sql)
                    results = cursor.fetchall()
                    return results
            except:
                return []

    def get_random_questions(self, limit=10):
        sql = f"SELECT url, answer FROM question_bank ORDER BY RAND() LIMIT {limit}"
        results = self.execute_query(sql)
        data = []
        for row in results:
            item = {
                'image_url': row[0],
                'answer': row[1]
            }
            data.append(item)
        return data

#
# db = Database('localhost', 3306, 'root', '123456', 'qa')
# db.connect()
#
# try:
#     results = db.get_random_questions()
#     print('results:', results)
#
# finally:
#     db.close()
