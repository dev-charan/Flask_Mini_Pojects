try:
    with open("Essentials/FILES/message.txt", "r") as file:
        print(file.read())
except FileNotFoundError:
    print("File not found. Please check the filename or path.")
