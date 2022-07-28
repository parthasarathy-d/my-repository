import re
import time

def getUserList():
    with open("USERS_DATA.txt", "r") as usersData:  
        for userData in usersData:
            userName, userCredential = userData.split("||")
            userCredential = userCredential.rstrip("\n")
            yield (userName, userCredential)

def isUserExits(name):
    return any(name == userName for userName, userCredential in getUserList())


def isCredentialsCheck(name, credentials):
    return any(user == (name, credentials) for user in getUserList())

def updatePassword(name, newCredentials):
    
    with open("USERS_DATA.txt", "r") as usersData:
        userDataLines = usersData.readlines()
    
    with open("USERS_DATA.txt", "w") as usersData:
        for userDataLine in userDataLines:
            userName, userCredentials = userDataLine.split("||")
            if userName != name:
                usersData.write(userName)
                usersData.write("||")
                usersData.write(userCredentials)
            else:
                usersData.write(userName)
                usersData.write("||")
                usersData.write(newCredentials)
                usersData.write("\n")
        print("Your Password is Updated Succesfully, You can login with New password")

    return

def createUser(accountName, accountCredentials):
    
    if not isUserExits(accountName):
        with open("USERS_DATA.txt", "a") as usersData:
            usersData.write(accountName)
            usersData.write("||") 
            usersData.write(accountCredentials)
            usersData.write("\n") 
            print("Your Account is Created Succesfully!, You can Login Now")
    else:
        print("Username exits already")

    return

def userLogin(loginName, loginCredentials):

    if isUserExits(loginName):
        if isCredentialsCheck(loginName, loginCredentials):
            print("Your are Succesfully Logged in!")
            time.sleep(5)
            print("Logging Out")
            time.sleep(3)
        else:
            print("Invalid Credentials")
    else:
        print("Username Dosent't Exists")

    return

if __name__ == "__main__":
    
    print("Welcome User")

    while True:
        
        print("Please select a Choice to Proceed:")
        
        choice = ""
        
        print("1 : Login If Existng User")
        print("2 : Create a New Account if New user")
        print("3 : Change Password with Username")
        print("4 : Exit")
        
        choice = input("Your Choice: ")
        
        
        if choice == "1":
            print("Enter Account Info: ")
            inpName = input("UserName: ")
            inpCredentials = input("Password: ")
            userLogin(inpName, inpCredentials)
            
        elif choice == "2":
            
            regx = "^[A-Za-z]+@[A-Za-z]+\.[A-Za-z]{1,}$"

            print("Enter Account Details: ")
            inpName = input("UserName: ")
            inpCredentials = input("Password: ")
            
            if re.match(regx, inpName):
                if len(inpCredentials) > 5 and len(inpCredentials) < 16:
                    createUser(inpName, inpCredentials)
                else:
                    print("Please Enter a Password with minimum 5 character and Maximum of 16 Character")
            else:
                print("Please Enter a valid Username in the format of 'username@mail.com'")
            

        elif choice == "3":
            print("Enter Account Details: ")
            inpName = input("UserName: ")
            
            
            if isUserExits(inpName):
                inpCredentials = input("New Password: ")
                
                if len(inpCredentials) > 5 and len(inpCredentials) < 16:
                        updatePassword(inpName, inpCredentials)
                else:
                    print("Please Enter a Password with minimum 5 character and Maximum of 16 Character")
                    
            else:
                print("Username Dosent't Exists")
                    
            
        elif choice == "4":
            print("Have a Nice Day, Bye!")
            break
        
        print("\n\n")
        

    