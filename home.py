import sqlconfig
import slots
from datetime import datetime,timedelta,date
import os

def patient(user):
    connection = sqlconfig.connect()
    cursor = connection.cursor()

    select1 = "SELECT * FROM profile WHERE user_id={};".format(user[0])
    cursor.execute(select1)
    user_details = cursor.fetchall()[0]
    columns = ['Profile ID', 'admin', 'User ID', 'First Name','Last Name','E-Mail','Age','MobileNumber','Address']
    os.system('cls')
    for col,det in zip(columns,user_details):
        if col != 'admin':
            print(col + " :" , det)
    print()
    select2 = "SELECT * FROM vaccine_info WHERE user_id = {};".format(user[0])

    cursor.execute(select2)
    vaccine_details = cursor.fetchall()

    if len(vaccine_details)==2:

        select4 = "SELECT status FROM vaccine_info WHERE user_id = {} and status <> 'Vaccinated' ; ".format(vaccine_details[0][1])
        cursor.execute(select4)
        curr_status = cursor.fetchall()[0][0]
        
        if len(curr_status)==0:
            print('Congrats on your 2nd Dose')

        elif curr_status == 'Pending':
            print('Wait for Approval')
        
        elif curr_status == 'Booked':
            select5 = "SELECT * FROM slots WHERE slot_id={};".format(vaccine_details[0][2])
            cursor.execute(select5)
            slot_det = cursor.fetchall()[0]
            print("This slot {} has been booked for you".format(slot_det[1].strftime("%d/%m/%Y")))
    
    
    elif len(vaccine_details)==1:

        select4 = "SELECT status FROM vaccine_info WHERE user_id = {}".format(vaccine_details[0][1])
        cursor.execute(select4)
        curr_status = cursor.fetchall()[0][0]
        
        if curr_status == 'Pending':
            print('Waiting for Approval on your 1st Dose')
        
        elif curr_status == 'Booked':
            select5 = "SELECT * FROM slots WHERE slot_id={};".format(vaccine_details[0][2])
            cursor.execute(select5)
            slot_det = cursor.fetchall()[0]
            print("This slot {} has been booked for you".format(slot_det[1].strftime("%d/%m/%Y")))
        
        elif curr_status == 'Vaccinated':
            print('Congrats on your 1st Dose, make sure to get your 2nd Dose on or after 28 days')

            select11 = "SELECT time_slot FROM slots INNER JOIN vaccine_info ON slots.slot_id = vaccine_info.slot_id WHERE vaccine_info.user_id = {} AND vaccine_info.status = \'Vaccinated\'".format(vaccine_details[0][1])
            cursor.execute(select11)
            VaccDate = cursor.fetchall()[0][0]

            print(VaccDate+timedelta(days = 28))

            slots.getSlots(VaccDate+timedelta(days = 28))
            slot_select=int(input('Enter the slot to choose : '))
            select6 = "SELECT * FROM slots WHERE slot_id={};".format(slot_select)
            cursor.execute(select6)
            
            if cursor.fetchall():
                insert2 = "INSERT INTO vaccine_info(user_id, slot_id, status) VALUES ({},{},\"Pending\")".format(user[0] ,slot_select)
                cursor.execute(insert2)
                connection.commit()
                print("Your Request is Submitted")
            
            else:
                print('No such slot found, Try again')

    else:
        print("You need to get your 1st dose\n")

        slots.getSlots(date.today())
        print()
        slot_select=int(input('Enter the slot to choose : '))
        select3 = "SELECT * FROM slots WHERE slot_id={};".format(slot_select)
        cursor.execute(select3)
        
        if cursor.fetchall():
            insert1 = "INSERT INTO vaccine_info(user_id, slot_id, status) VALUES ({},{},\"Pending\")".format(user[0] ,slot_select)
            cursor.execute(insert1)
            connection.commit()
            print("Your Request is Submitted")
        
        else:
            print('No such slot found, Try again')

    connection.close()


def admin():
    
    connection = sqlconfig.connect()
    cursor = connection.cursor()
    
    os.system('cls')
    print()
    print('1. Update Patients who got vaccinated today\n')
    print('2. Create Vacant Slots\n')
    print('3. Print all Slots\n')
    print('4. Delete Slots\n')
    print('5. Print All Pending Patients\n')
    print('6. Approve/Reject Requests\n')
    print('7. Generate Report\n')
    ch=int(input('Enter a Choice : '))

    if ch == 1:

        select9 = "SELECT user_id FROM vaccine_info WHERE status = \'Booked\'"
        cursor.execute(select9)
        val = cursor.fetchall()

        if not val:
            print("No ID's are pending")
            return
        else:
            print("The ID's pending are : ")
            for IDs in val:
                print(*IDs)
        
        print('Enter the User ID of the patient who got vaccinated today as a Space Seperated Values')
        toUpdate = list(map(int,input().split()))
        for ID in toUpdate:
            if ID in [i[0] for i in val]:
                select12 = "SELECT slot_id from vaccine_info WHERE user_id = {} AND status = \'Booked\'".format(ID)
                cursor.execute(select12)
                currSlotID = cursor.fetchall()[0][0]

                update1 = "UPDATE vaccine_info SET status =\'Vaccinated\' WHERE user_id = {}".format(ID)
                cursor.execute(update1)
                connection.commit()

                update2 = "UPDATE slots SET vaccine_count = vaccine_count-1 WHERE slot_id = {}".format(currSlotID)
                cursor.execute(update2)
                connection.commit()
            else:
                print("No such ID exist")
            
    elif ch == 2:
        print("Enter the number of Slots to be added")
        n=int(input())
        for i in range(n):
            print('Enter the Slot Date in yyyy-mm-dd format and number of vaccines available at that slot')
            slot_entered = input().split()
            insert3 = "INSERT INTO slots (time_slot, vaccine_count) VALUES (\"{}\",{});".format(slot_entered[0], int(slot_entered[1]))
            cursor.execute(insert3)
            connection.commit()
            
        
    elif ch == 3:
        
        os.system('cls')
        print("\nAll the Slots Available are\n")
        select7 = "SELECT * FROM slots"
        cursor.execute(select7)
        
        for slot_available in cursor.fetchall():
            if slot_available[-1]>0:
                print(*slot_available)
        
    elif ch == 4:

        print("\nAll the Slots Available are\n")
        select7 = "SELECT * FROM slots"
        cursor.execute(select7)
        
        slt_fetch = cursor.fetchall()

        for slot_available in slt_fetch:
            if slot_available[-1]>0:
                print(*slot_available)
        print()

        print("Enter the Slot ID of the slots to be deleted as Space seperated Values")
        delSlot = list(map(int,input().split()))
        for slt in delSlot:
            if slt in [i[0] for i in slt_fetch]:
                update2 = "UPDATE slots SET vaccine_count = 0 WHERE slot_id = {}".format(slt)
                cursor.execute(update2)
                connection.commit()
            else:
                print("No such slot exists")

    elif ch == 5:
        select8 = "SELECT profile.user_id, firstname, lastname, email, age, mobileNumber, address FROM profile INNER JOIN vaccine_info ON vaccine_info.user_id = profile.user_id WHERE vaccine_info.status = \'Pending\'"
        cursor.execute(select8)
        val = cursor.fetchall()
        print()

        if not val:
            print("No Pending Requests")
        else:
            print("Pending Requests are : ")
            for i in val:
                print(*i)
    
    elif ch == 6:
        select8 = "SELECT profile.user_id, firstname, lastname, email, age, mobileNumber, address FROM profile INNER JOIN vaccine_info ON vaccine_info.user_id = profile.user_id WHERE vaccine_info.status = \'Pending\'"
        cursor.execute(select8)
        val = cursor.fetchall()

        if not val:
            print("No Pending Requests")
            return
        else:
            print("Pending Patients are : ")
            for i in val:
                print(*i)
        print()
        print('Enter the User ID of the patient to be accepted')
        toAccept = list(map(int,input().split()))
        for ID in toAccept:
            if ID in [i[0] for i in val]:
                update1 = "UPDATE vaccine_info SET status =\'Booked\' WHERE user_id = {}".format(ID)
                cursor.execute(update1)
                connection.commit()
            else:
                print('The ID {} doesnt exist'.format(ID))
    
    elif ch == 7:
        print('1. User ID\n2. Slot ID\n')
        ch=int(input('Enter your choice : '))
        if ch == 1:
            genID = int(input('Enter the User ID : '))
            select13 = "SELECT profile.user_id, slot_id, firstname, lastname, age, status FROM vaccine_info INNER JOIN profile ON vaccine_info.user_id = profile.user_id AND vaccine_info.user_id = {}".format(genID)
            cursor.execute(select13)

            file1 = open('ReportFile.txt','a')
            file1.write("Report Based on User ID\n")

            for i in cursor.fetchall():
                file1.write(str(i)+'\n')

            file1.write('\n')
            file1.write('\n')
            file1.close()
        elif ch == 2:
            slotID = int(input('Enter the Slot ID : '))
            file1 = open('ReportFile.txt','a')
            file1.write("Report Based on Slot ID\n")
            
            select14 = "SELECT time_slot FROM slots WHERE slots.slot_id = {}".format(slotID)
            cursor.execute(select14)
            file1.write('The Slot Date is {}\n'.format(cursor.fetchall()[0][0]))

            select15 = "SELECT user_id, status FROM vaccine_info WHERE vaccine_info.slot_id = {}".format(slotID)
            cursor.execute(select15)

            for i in cursor.fetchall():
                file1.write(str(i)+'\n')

            file1.write('\n')
            file1.write('\n')
            file1.close()




def options(user):
    if user[0]==1:
        while True:
            admin()
            ch = input('Do you want to continue (Y/N): ')
            
            if ch.lower()=='n':
                return
    
    else:
        patient(user)