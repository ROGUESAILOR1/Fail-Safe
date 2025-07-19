# Fail_safe.py


1. A Fail Safe using hashing for paasword and keys
2. logs keys in .json file name vault.json
3. uses hashed key and hashed password.
4. Gives ownership of the file to the one who encrypts it allowing only that person to decrypt the file
5. avoids over encryption
6. on file renaming or path change the file gets locked 
7. any other present users cannot decrypt the file
8. bruting resistance as the program breaks on several failed attempts

