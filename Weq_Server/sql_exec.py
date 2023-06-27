import sqlite3

# 连接到数据库
conn = sqlite3.connect('WeQ.db')
cursor = conn.cursor()

# # 创建accounts表
# cursor.execute('''CREATE TABLE IF NOT EXISTS accounts (
#                     username TEXT,
#                     password TEXT,
#                     email TEXT
#                 );''')


cursor.execute('''CREATE TABLE IF NOT EXISTS friends (
                    username TEXT,
                    friend_id TEXT
                );''')


conn.commit()
conn.close()
