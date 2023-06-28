import sqlite3

# 连接到数据库
conn = sqlite3.connect('WeQ.db')
cursor = conn.cursor()



cursor.execute('''delete from accounts where username = "Ming";''')


conn.commit()
conn.close()
