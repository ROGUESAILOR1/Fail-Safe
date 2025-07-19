import base64
import hashlib as hl
import json
import os

class vault:
    def __init__(self,filename="vault.json"):
        self.username =None
        self.password =None
        self.register = self.json_loader(filename)
        self.filename=filename
        self.filepath = ""
        try:
            self.json_loader(filename)
        except (FileNotFoundError, json.JSONDecodeError):
            print("No previous inventory found, starting with an empty inventory.")
            self.register = {}
    def check_created_password(self):
        import re
        while True:
            self.password = input("Enter your password: ")
            if len(self.password)<8:
                print("Password must be more than or equal to 8 characters")
            elif re.search(r'[A-Z]', self.password) is None:
                print("Password must contain at least one uppercase letter")
            elif re.search(r"[!@|~`#$%+*?<>=]",self.password) is None:
                print("Password must contain at least one special character")
            elif re.search(r'\d', self.password) is None:
                print("Password must contain at least one digit")
            else:
                print("Password is Valid\nAre you sure you want to create this password?\n")
                choice=input("Y/N: ").strip().lower()
                if choice == "y":
                    print("Password is set")
                    return hl.sha256(self.password.encode()).digest()
                    break
                elif choice == "n":
                    print("Please enter a new password")
                    continue
    def enter_registry(self,filename="vault.json"):
        while True:
            self.username = input("Enter your username: ")
            if self.username in self.register:
                print("Username already exists. Please choose a different username.")
            else:
                break
        self.check_created_password()
        ch_password = self.check_created_password()
        hashed_pw = base64.b64encode(ch_password).decode()
        key = base64.urlsafe_b64encode(ch_password).decode()

        self.register[self.username]={
            "Password":hashed_pw,
            "Key":key,
            "en_files":[self.filepath]
            }
        self.json_saver(filename)
    def is_file_owned_by_another_user(self, filepath):
        for user, data in self.register.items():
            if filepath in data.get("en_files", []):
                if user != self.username:
                    return user
        return None

    def json_saver(self,filename="vault.json"):
        with open(filename, "w") as f:
            json.dump(self.register,f,indent=4, separators=(", ", ": "))
            print("User credentials saved successfully")

    def json_loader(self,filename="vault.json"):
        if filename in os.listdir():
            with open(filename, "r") as f:
                content = f.read().strip()
                if content:
                    self.register = json.loads(content)
                else:
                    self.register = {}

        else:
            f= open(filename, "x")
            f.close()
            self.register = {}
        return self.register

    def encrypter(self):
        hashed_input = base64.b64encode(hl.sha256(self.password.encode()).digest()).decode()

        if self.username in self.register and hashed_input == self.register[self.username]["Password"]:
            from cryptography.fernet import Fernet
            key_str=self.register[self.username]["Key"]
            key=key_str.encode()
            f=Fernet(key)
            try:
                self.filepath = input("Enter the name or filepath to encrypt: ")
                owner=self.is_file_owned_by_another_user(self.filepath)
                if owner:
                    print(f"{self.filepath} is already owned by {owner}. You cannot encrypt it.")
                    return False
                else:
                    self.register[self.username]["en_files"].append(self.filepath)
                    with open(self.filepath,"rb") as tben_file:
                        data=tben_file.read()
                        en_data=f.encrypt(data)
                    with open(self.filepath ,"wb") as en_file:
                        en_file.write(en_data)
                        print("Encryption Successfull!")
                        self.json_saver(self.filename)
            except FileNotFoundError:
                print(f"{self.filepath} Not found!")
        else:
            print("Invalid password or username. Try again.")
    def decrypter(self):
        hashed_input = base64.b64encode(hl.sha256(self.password.encode()).digest()).decode()
        if self.username in self.register and hashed_input == self.register[self.username]["Password"]:
            from cryptography.fernet import Fernet
            key_str = self.register[self.username]["Key"]
            key = key_str.encode()
            f = Fernet(key)
            try:
                self.filepath = input("Enter the name or filepath to decrypt: ")
                owner=self.is_file_owned_by_another_user(self.filepath)
                if owner and owner != self.username:
                    print(f"{self.filepath} is owned by {owner}. You cannot decrypt it.")
                    return False
                elif owner == self.username:
                    self.register[self.username]["en_files"].remove(self.filepath)
                    self.json_saver(self.filename)
                else:
                    self.register[self.username]["en_files"].remove(self.filepath)
                    with open(self.filepath, "rb") as file:
                        en_data = file.read()
                        dec_data = f.decrypt(en_data)
                    with open(self.filepath, "wb") as dec_file:
                        dec_file.write(dec_data)
                        print(f"File '{self.filepath}' decrypted successfully")
            except FileNotFoundError:
                print(f"Encrypted file '{self.filepath}' not found.")
            except Exception as e:
                print("Decryption failed:", str(e))
        else:
            print("User not registered.")
