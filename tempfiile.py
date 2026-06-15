def printName(name):
    print("Welcome to Name Printer")
    username = input("Enter your username : ")
    year = int(input("Enter your year of birth : "))
    choice = input("where will you like in bed??")
    print(f"my name is {username}")
    print(f"my age is {calculateAge(year)}")
    print(f"my gender is {checkGender(choice)}")

def calculateAge(year):
    user_age = 2026 - year
    return userage

def checkGender(choice):
    if choice.lower() == "woman":
        return "Male"
    elif choice.lower() == "man":
        return "Female"
    else:
        return "Unknown"


def closeApp():
    print("closing app , Good bye!!!")
    exit()


printName()
closeApp()