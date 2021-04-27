import os
import register
import login
import home

print('\nWelcome to Book My Vaccine')

print("\n1.Register\n2.Login\n3.Exit\n")
ch = int(input('Enter your choice : '))

while ch!=3:

    if ch == 1:

        user={}
        os.system('cls')

        print('Enter the Required User Details')
        user['username'] = input('Enter your UserName : ')
        user['password'] = input('Enter your Password : ')
        user['email'] = input('Enter your Email : ')
        user['firstname'] = input('Enter your First Name : ')
        user['lastname'] = input('Enter your Last Name : ')
        user['age'] = int(input('Enter your Age : '))
        user['mobilenumber'] = input('Enter your Mobile Number : ')
        user['address'] = input('Enter your Address : ')

        register.createUser(user)

    elif ch == 2:

        credentials={}
        os.system('cls')

        print('Enter Your Credentials')
        credentials['email'] = input('Enter your Email : ')
        credentials['password'] = input('Enter your Password : ')
        user = login.authenticate(credentials)
        if user:
            home.options(user)

    elif ch != 3:
        print('Provide a Valid Input')

    print("\n1.Register\n2.Login\n3.Exit\n")
    ch = int(input('Enter your choice : '))