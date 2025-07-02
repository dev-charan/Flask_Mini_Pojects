users = ["charan","rahul","sneha"]

print(users[0])
users.append('ajay')
print(len(users))

names = [u.upper() for u in users if u.startswith("c")]
print(names)  # ['CHARAN']
