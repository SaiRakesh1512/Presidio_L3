import sqlconfig

def createUser(user):
    connection = sqlconfig.connect()
    cursor = connection.cursor()
    insert1 = "INSERT INTO users(username, password, email) VALUES (\"{}\",\"{}\",\"{}\");".format(user['username'],user['password'],user['email'])
    try:
        cursor.execute(insert1)
    except:
        print('User Already Exists')
        connection.close()
        return
    connection.commit()
    select1 = "SELECT user_id FROM users WHERE username=\""+user['username']+"\";"
    cursor.execute(select1)
    rows = cursor.fetchall()
    # print(rows[0][0])
    insert2 = "INSERT INTO profile(admin, user_id, firstname, lastname, email, age, mobilenumber, address) VALUES (\"{}\",{},\"{}\",\"{}\",\"{}\",{},\"{}\",\"{}\");".format('false',rows[0][0],user['firstname'],user['lastname'],user['email'],user['age'],user['mobilenumber'],user['address'])
    cursor.execute(insert2)
    connection.commit()
    connection.close()
    

# user={'username':'akash_aarumugam','password':'aaruadi_aarumugam','email':'akash@gmail.com','firstname':'aakash','lastname':'aarumugam','age':20,'mobilenumber':'9191919191','address':'kuruku theru, saidapet, USA'}

# createUser(user)