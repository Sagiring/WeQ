import sqlite3

def sqlRegister(accounts):
    username = accounts[0]
    password = accounts[1]
    email = accounts[2]


    sql = '''select username
            from accounts
            where username = ?'''

    connection  = sqlite3.connect('WeQ.db')
    toSql = connection.cursor()
    try:
        toSql.execute(sql,(username,))
    except Exception as e:
        print(e)
        return False
    result = toSql.fetchall()
    if result == []:
        toSql.execute('insert into accounts values(?,?,?)',(username,password,email))
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
            where username = ?'''
    connection  = sqlite3.connect('WeQ.db')
    toSql = connection.cursor()
    try:
        toSql.execute(sql,(username,))
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
 
def sql_add_friend(username,friend_id):
    if username < friend_id:
        username,friend_id = friend_id,username
    sql = '''INSERT INTO friends VALUES(?,?)'''
    connection  = sqlite3.connect('WeQ.db')
    toSql = connection.cursor()
    try:
        toSql.execute(sql,(username,friend_id))
    except Exception as e:
        print(e)
        return False
    toSql.close()
    connection.commit()
    connection.close()
    return True

def sql_get_friend(username):
    sql = '''SELECT friend_id
            From friends
            WHERE username = ?
            UNION ALL
            SELECT username
            From friends
            WHERE friends = ?'''
    connection  = sqlite3.connect('WeQ.db')
    toSql = connection.cursor()
    try:
        toSql.execute(sql,(username,username))
    except Exception as e:
        print(e)
        return False
    result = toSql.fetchall()
    toSql.close()
    connection.close()
    return result

def sql_delete_friend(username,friend_id):
    if username < friend_id:
        username,friend_id = friend_id,username
    sql = '''delete from friends where username = ? and friend_id = ?'''
    connection  = sqlite3.connect('WeQ.db')
    toSql = connection.cursor()
    try:
        toSql.execute(sql,(username,friend_id))
    except Exception as e:
        print(e)
        return False
    toSql.close()
    connection.commit()
    connection.close()
    return True
