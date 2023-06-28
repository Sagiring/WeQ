import sqlite3

# 连接到数据库
conn = sqlite3.connect('WeQ.db')
cursor = conn.cursor()



cursor.execute('''CREATE TABLE friends (
                    username TEXT PRIMARY KEY,
                    friend_id TEXT
                );''')


conn.commit()
conn.close()
