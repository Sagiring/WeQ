import sqlite3

def sqlRegister(accounts):
    username = accounts[0]
    password = accounts[1]


    sql = '''select username
            from accounts
            where username = "?"'''

    connection  = sqlite3.connect('WeQ.db')
    toSql = connection.cursor()
    try:
        toSql.execute(sql,[username])
    except Exception as e:
        print(e)
        return False
    result = toSql.fetchall()
    if result == []:
        toSql.execute('insert into accounts values("?","?")',[username,password])
        connection.commit() 
        toSql.close()
        connection.close()
        return True
    else:
        toSql.close()
        connection.close()
    return False
 
def sqlLogin(accounts):
    username = accounts[0]
    password = accounts[1]
    sql = '''select password
            from accounts 
            where username = "?"'''
    connection  = sqlite3.connect('WeQ.db')
    toSql = connection.cursor()
    try:
        toSql.execute(sql,[username])
    except Exception as e:
        print(e)
        return False
    result = toSql.fetchall()
    toSql.close()
    connection.close()
    if result == []:
        return False
    else:
        if result[0][0] == password:
            return True
        else:
            return False
 
