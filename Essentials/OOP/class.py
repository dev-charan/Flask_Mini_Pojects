class User:
    def __init__(self,name,email):
        self.name = name
        self.email = email
    
    def greet(self):
        return f"Hello, {self.name}"
    
u1 = User("Charan", "charan@example.com")
print(u1.greet())  # Hello, Charan!
print(u1.email)    # charan@example.com
