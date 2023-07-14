"""
用于垃圾分类题库的数据库插入
"""

import pymysql

db = pymysql.connect(
    host='localhost',
    port=3306,
    user='root',
    password='123456',
    charset='utf8mb4',
    database='qa'
)

with open(r'C:\Users\13763\Desktop\题目返回.txt', mode='r', encoding='utf-8') as f:
    lines = f.read().split('\n\n')
for i in range(len(lines)):
    lines[i] = lines[i].split(',')

try:
    with db.cursor() as cursor:
        # 创建插入数据的SQL语句
        sql = "INSERT INTO question_bank (url, answer) VALUES (%s,%s)"

        for i in range(len(lines)):
            # 要插入的数据
            data = (lines[i][0], lines[i][1])
            print(data)
            # 执行插入操作
            cursor.execute(sql, data)

    # 提交事务
    db.commit()
    print("数据插入成功！")

finally:
    # 关闭数据库连接
    db.close()
