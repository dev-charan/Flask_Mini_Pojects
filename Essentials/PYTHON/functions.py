# def log(*args):
#     for msg in args:
#         print("Log:",len(msg))

# log(["User logged in", "IP: 192.0.0.1"],["User logged in", "IP: 192.0.0.1"])

def show_info(**kwargs):
    for key, vlaue in kwargs.items():
        print(key,vlaue)
    
show_info(name='charan',age=22,active=True)
