# try:
#     result = 10 /0
# except ZeroDivisionError:
#     print("you cont divide by zero")

# try:
#     user_input = int('abc')
# except Exception as e:
#     print("something went wrong")

try:
    f = open("file.txt", "r")
except FileNotFoundError:
    print("File not found.")
finally:
    print("Cleanup done.")
