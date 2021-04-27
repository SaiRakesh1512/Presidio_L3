import sqlconfig


def authenticate(credentials):
    connection = sqlconfig.connect()
    cursor = connection.cursor()
    select1 = "SELECT * FROM users WHERE email=\"{}\" AND password=\"{}\";".format(credentials['email'],credentials['password'])
    cursor.execute(select1)
    try:
        User = cursor.fetchall()[0]
        connection.close()
        return User
    except:
        print("USER NOT FOUND, TRY AGAIN")
        connection.close()
        return None
