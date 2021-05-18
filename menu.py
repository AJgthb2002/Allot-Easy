from database import *
import time
from pywebio.input import *
from pywebio.output import *
from allotment_mechanism import *


mydata= Data() #object of class Data
mymachine= Allotment_mechanism()
welm_img = open('images/Welcome to AllotEasy.jpg', 'rb').read()  
header_img = open('images/header_new.jpg', 'rb').read()
aboutus_img = open('images/Aboutus_img.jpg', 'rb').read()

#def check_student_admin_choice(user_inp):
#     if (user_inp > 7 or user_inp < 1):
#         return ("Invalid choice number. Select a choice from 1 to 7") 
    

class Menu:
  def __init__(self): 
    self.user= None


  def about_us(self):
    clear('ROOT')  
    with use_scope("main", clear=True):
        put_image(aboutus_img, width='150%', height='400px')
        data = input_group("Press button to return to menu",[actions('', [ {'label': 'Back', 'value': 1},], name='action', help_text=None),])
    clear('ROOT')

  def login(self):
    with use_scope("main",clear=True):
        put_image(src=welm_img, width='150%', height='400px')  #put welcome screen
   
    login_choice = input_group('Get Started', [
    actions('', [ 
        {'label': 'Sign Up', 'value': 1}, 
        {'label': 'Login (Student)', 'value': 2}, 
        {'label': 'Login (Admin)', 'value': 3}, 
        {'label': 'About Us', 'value': "Aboutus"},
        {'label': 'Exit', 'value': 4}, 
        ], name='action', help_text=None),
    ])
    
    user_inp= login_choice["action"]
    if user_inp=="Aboutus":
        self.user=None
        clear("main")
        self.about_us()
        return
    else:    
    # store who is the current user in class var- user.   
        self.user = user_inp
        if user_inp==1:
            # signup for students is selected
            clear("main")
            mydata.student_sign_up()
        
        if user_inp==2 :
            # login as student is selected
            name_surname = input("Enter full name (name surname): ", type=TEXT, required=True)
            name= (name_surname.split())[0]
            mydata.set_userinfo(2,name) # send user info to database file
            is_correct_pswd = mydata.check_pswd(name)
            if(is_correct_pswd==1):  # name and password match
                with use_scope("main"):
                    put_success(f"\n Welcome, {name.capitalize()}!")
                time.sleep(2)
                return
            else:
                # Username or password or both do not match
                with use_scope("main"):
                    put_error("Sorry! Incorrect credentials. ", closable= True) 
                time.sleep(2)
                self.login()
            
        if user_inp ==3:
            # login as admin is selected
            # (pwd for admin is secretadmin)
            pwd= input("Enter password:", type=PASSWORD, required=True)
            if (pwd =="secretadmin"):
                with use_scope("main"):
                    put_success("Welcome, Admin!")
                mydata.set_userinfo(3,"admin") # send user info to database file
                time.sleep(2)
            else:
                with use_scope("main"):
                    put_error("Sorry! Incorrect password entered. ",closable=True)
                time.sleep(2)
                self.login()

  def menu_for_student(self):
    stud_menu_img = open('images/student_menu_img.jpg', 'rb').read()
    
    choice= None 
    
    while(choice!=8): # breaks out of loop when 7 i.e. logout is selected
        if mydata.flag==0: 
            # flag=0 indicates user has not withdrawn his application.
            
            with use_scope("main", clear=True):
                put_image(stud_menu_img,width='80%',height='300px')
            data= input_group("Student Menu", [
                radio(label="", name='menu', options=[("View Seat Matrix",1),("Fill Application details",2),("Check your application status",3),("Withdraw application",4),("View Branchwise cutoff marks",5),("View data of vacancies left",6),("Change Password",7),("Logout",8)], required=True, inline=False, value=None)    
            ])
            choice= data['menu']
            #choice= input("Enter your choice: ", type=NUMBER, validate=check_student_admin_choice, help_text='Enter your choice number', required=True)
        else: 
            # flag=1 is the case where user has withdrawn the application. So we do not show him any other option and force him to logout.
            choice=8
        if choice!=8:
            # when any choice other than logout is selected, call the corresponding function from the functions list in database.py
            clear("main")
            mydata.student_options[choice-1](mydata) 
            
    return


  def menu_for_admin(self):
    clear('ROOT') 
    admin_menu_img = open('images/admin_menu_img.jpg', 'rb').read()
    mymachine.flag=0
    choice= None 
    while(choice!=7):  # breaks out of loop when 7 i.e. logout is selected

        if mymachine.flag==0:
            with use_scope("main", clear=True):
                    put_image(admin_menu_img,width='80%',height='300px')
            data= input_group("Admin Menu", [
                radio(label="", name='menu', options=[("Run Seat allotment process",1),("View full allotment result",2),("View branch-wise allotment result",3),("Search a student",4),("Get list of students without allotment",5),("View data of vacancies left",6),("Logout",7)], required=True, inline=False, value=None)    
            ])
            choice= data['menu']        
            #choice= input("Enter your choice: ", type=NUMBER, validate=check_student_admin_choice, help_text='Enter your choice number', required=True)
        else:
            choice=7

        if choice!=7:
            # when any choice other than logout is selected, call the corresponding function from the functions list in database.py
            clear()
            if choice!=1:
                # all functions other than 'run allotment' are present in class Data. They require an object of this class to be passed as parameter.
                clear("main")
                mydata.admin_options[choice-1](mydata)   
            else:
                # if choice 1 is selected, this run allotment function is present in a diff class than other functions and hence does not require the object of class Data to be passed as paramenter.
                clear("main")
                mydata.admin_options[0]()      
    return
