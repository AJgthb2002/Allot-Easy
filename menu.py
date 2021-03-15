from os import system, name
from database import *

import time
import json

mydata= Data()

usernames=["dum","aj","aaj"]

def clear(): 
    # for windows 
    if name == 'nt': 
        _ = system('cls')


class Menu:
  def __init__(self):
    
    self.user= None
    # self.username= None

    self.student_menu = """
                                                         MENU
                                            ----------------------------------
                                            |  1. View Seat Matrix.          |
                                            |  2. Register.                  |
                                            |  3. Check application status   |
                                            |  4. Edit your application      |
                                            |  5. Withdraw application       |
                                            |  6. View cutoff marks          |
                                            |                                |
                                            |  7. Logout.                    |
                                            ----------------------------------
      """
    self.admin_menu= """
                                                        MENU
                                --------------------------------------------------------            
                                |  1. Run Seat Allotment Process.                      |
                                |  2. View all student registrations.                  |
                                |  3. View full allotment result.                      |
                                |  4. View branchwise allotment list.                  |
                                |  5. Search a student.                                |
                                |  6. View list of students left without allotment.    |
                                |  7. Get data of vacancies left.                      |
                                |                                                      |
                                |  8. Log out.                                         |
                                --------------------------------------------------------
      """
    self.login_menu= """
                                                      MENU
                                            --------------------------        
                                            |  1. Sign Up            |
                                            |  2. Login as Student   |
                                            |  3. Login as Admin     |
                                            |  4. Exit portal        |
                                            --------------------------
      """


  def login(self):
    clear()  
    print(self.login_menu)
    user_inp = int(input("Enter your choice: "))
    
    while (user_inp > 4 or user_inp < 1):
        user_inp = int(input("Invalid. Enter your choice again: "))
    self.user = user_inp

    if self.user==1:    # signup
        self.signup()

    if self.user==2:    #login as student
        username = input("Enter your username: ")
        pwd = input("Enter password: ")
        # if username and pwd match, set user=2 and user's name= find from file.
        with open("signup_data.json",'r') as datafile:
            try:
                data= json.load(datafile)
            except json.JSONDecodeError:
                print(f"Error: Username {username} not found! Please Sign up on the portal.") 
                time.sleep(2)
                self.login()     
            else:
                if username in data:
                    if pwd == data[username]["password"]:
                        mydata.set_userinfo(self.user, username, data[username]["name"])
                        print(f"\n Welcome, {username.capitalize()}!")
                        time.sleep(2)
                    else:
                        print("\nError: Incorrect Password. Please try again.")
                        time.sleep(2)
                        self.login()
                else:
                    print(f"\nError: Username {username} not found! Please Sign up on the portal.")
                    time.sleep(2) 
                    self.login()   


    if self.user==3:      # login as admin
        pwd = input("Enter password: ") 
        # admin password = 12345
        if pwd == "12345":
            print("\n Welcome, Admin!")
            mydata.set_userinfo(self.user, "admin", "admin")
            time.sleep(2)
        else:
            print("\nError: Incorrect Password. Please try again.") 
            time.sleep(2)
            self.login()                 


  def signup(self):
    clear()
    name= input("Enter your name: ")
    surname= input("Enter your surname: ")
    email= input("Enter your email id: ")
    username= input("Set a username: ")
    while(username in usernames):
        username= input("This username is not available. Enter another username: ")
    usernames.append(username)
    pwd= input("Set a password: ")
    new_data_dict={
        username:{
            "name": name,
            "surname" : surname,
            "email": email,
            "password": pwd,
        }
    }

    try:
        with open("signup_data.json",'r') as datafile:
            data= json.load(datafile)
            
    except :
        with open("signup_data.json",'w') as datafile:
            json.dump(new_data_dict, datafile, indent=4)
    else:
        data.update(new_data_dict)
        with open("signup_data.json",'w') as datafile:
            json.dump(data, datafile, indent=4)
    finally:
        print("Sign Up successful!")
        time.sleep(2)

        
  def menu_for_student(self):
    clear() 
    choice= None 
    while(choice!=7):
        print(self.student_menu)
        choice= int(input("Enter your choice: "))
        while(choice>7 or choice <1):
            choice = int(input("Invalid. Enter your choice again: "))

        
        if choice!=7:
            clear()
            mydata.student_options[choice-1](mydata)    
      
    return
    

  def menu_for_admin(self):
    clear() 
    choice= None 
    while(choice!=8):
        print(self.admin_menu)
        choice= int(input("Enter your choice: "))
        while(choice>8 or choice <1):
            choice = int(input("Invalid. Enter your choice again: "))

        if choice!=8:
            clear()
            if choice!=1:
                mydata.admin_options[choice-1](mydata)   
            else:
               mydata.admin_options[0]()    
        
    return
    # self.login() 


    