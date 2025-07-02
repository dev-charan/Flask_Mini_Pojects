user = input(str('enter the user type'))

if user == 'admin':
    print(f'welcome {user}')
elif user == 'user':
    print('welcome user')
else:
    print('access denied')