import pymysql

# def commit():
#     connection.commit()

def connect():
    connection = pymysql.connect(host="localhost", user="root", passwd="", database="book_my_vaccine")
    return connection

# def disconnect_database():
#     connection.close()

# COMMANDS TO CREATE TABLES
# CREATE TABLE users (user_id int NOT NULL AUTO_INCREMENT, username varchar(55) NOT NULL, password varchar(55) NOT NULL, email varchar(55) NOT NULL, PRIMARY KEY (id));
# CREATE TABLE profile (prof_id int NOT NULL AUTO_INCREMENT, admin varchar(10) NOT NULL,  user_id int NOT NULL, firstname varchar(55) NOT NULL, lastname varchar(55) NOT NULL, email varchar(55) NOT NULL, age int NOT NULL, mobileNumber varchar(15) NOT NULL, address varchar(100) NOT NULL, PRIMARY KEY (prof_id), FOREIGN KEY(user_id) REFERENCES users(user_id));
# CREATE TABLE vaccine_info (vaccine_id int NOT NULL AUTO_INCREMENT, user_id int NOT NULL, slot_id int NOT NULL, PRIMARY KEY (vaccine_id), FOREIGN KEY(slot_id) REFERENCES slots(slot_id));
# CREATE TABLE slots (slot_id int NOT NULL AUTO_INCREMENT, time_slot DATETIME NOT NULL, vaccine_count int NOT NULL, PRIMARY KEY (slot_id));
