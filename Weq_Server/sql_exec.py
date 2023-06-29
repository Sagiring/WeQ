import sqlite3

# 连接到数据库
conn = sqlite3.connect('WeQ.db')
cursor = conn.cursor()



cursor.execute('''ALTER TABLE friends_backup RENAME TO friends''')


conn.commit()
conn.close()
