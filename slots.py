import sqlconfig
from datetime import date

def getSlots(dateElement):
    connection = sqlconfig.connect()
    cursor = connection.cursor()
    select1 = "SELECT * FROM slots WHERE vaccine_count>0"
    cursor.execute(select1)
    rows = cursor.fetchall()
    for i in rows:
        if i[2]>0 and i[1]>dateElement:
            print(i[0],i[1].strftime("%d/%m/%Y"),i[2])
    connection.close()