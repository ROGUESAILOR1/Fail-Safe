from File_vault import vault
fl=vault()
fl.register = fl.json_loader()

print("""Welcome to File vault
        Please select an option:
        1. Register as a new user
        2. Log in as an existing user
        3. Exit""")
while True:
    x=input("Enter your choice: ")
    if x == "1":
        fl.enter_registry()
    elif x== "2":
        print("""State your purpose User: 
                1. Encrypt a file
                2. Decrypt a file
                3. Exit""")
        while True:
            y= input("Enter your choice: ")
            if y=="1":
                fl.username = input("Enter your username: ")
                fl.password = input("Enter your password: ")
                fl.encrypter()
            elif y=="2":
                fl.username = input("Enter your username: ")
                fl.password = input("Enter your password: ")
                fl.decrypter()
            elif y=="3":
                break
    elif x == "3":
        print("Exiting the program.")
        break