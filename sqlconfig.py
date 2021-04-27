import pymysql

# def commit():
#     connection.commit()

def connect():
    connection = pymysql.connect(host="localhost", user="root", passwd="", database="book_my_vaccine")
    return connection

# def disconnect_database():
#     connection.close()