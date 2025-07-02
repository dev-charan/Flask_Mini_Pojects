# users =["charan","rahul","sneha"]

# for user in users:
#     print(F"Welcome {user}")

# retry = 3

# while retry > 0:
#     print('trying to connect')
#     retry -=1

# usernames= ["charan","","ajay"]

# for username in usernames:
#     if not usernames:
#         continue
#     print('processing',username)

# tasks= ["login","fetch data","save to db"]

# for i , task in enumerate(tasks,start=1):
#     print(f"{i+1}.{task}")

# print(enumerate(tasks))

# a = ['charan','rai','bs']
# b= enumerate(a)

# nextvalue = next(b)
# print(nextvalue)

# Given list of users with their active status:
users = [
    {"name": "Charan", "active": True},
    {"name": "Ravi", "active": False},
    {"name": "Sneha", "active": True}
]

# Write a loop that prints only active users
for user in users:
    if user['active']:
        print(user['name'])
        