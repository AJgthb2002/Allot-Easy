from allotment_mechanism import * 
from csv import * 
import pandas as pd
import time
from pywebio.input import *
from pywebio.output import *

mymachine= Allotment_mechanism() #obj of class Allotment_machanism

# details of the user who is currently logged in. Initially set to Null.
user= None
name=""
pwd=None

stud_menu_img = open('images/student_menu_img.jpg', 'rb').read()
header_img = open('images/header_new.jpg', 'rb').read()
privacy_policy_img = open('images/PrivacyPolicy.jpg','rb').read()

def check_cet(user_inp):
    if (user_inp > 200 or user_inp < 0):
        return ("Invalid score. Please enter your score out of 200.") 

class Data:
      
    def __init__(self):
        self.flag = 0  # flag=1: user has withdrawn his application, record is deleted from datasheet.
    
        self.vacancies={"Computer": mymachine.vacancies[0], "IT": mymachine.vacancies[1], "Mechanical": mymachine.vacancies[2], "Electronics": mymachine.vacancies[3]}
        
        self.available_branches = ["Computer", "IT", "Mechanical", "Electronics"]

        # initially cutoffs for all branches are 0. These mks will be updated after entire allotment process is completed.
        self.cutoff_marks={"Computer": 0, "IT": 0, "Mechanical": 0, "Electronics": 0}

        self.seat_matrix_table= [["1.", "Computer", "120"],["2.", "IT", "60"],["3.", "Mechanical", "60"],["4.", "Electronics", "120"]]
        

    def set_userinfo(self, usr, usrnm):
        # sets the info of the currently logged-in user in global variables user and name.
        global user, name
        user = usr
        name = usrnm
        self.flag=0 # set flag to 0 whenever a user logs in.

    def view_seatmatrix(self):
        # print total no. of seats available in each branch of college.
        with use_scope('ROOT'):
            put_image(header_img, width='100%', height='40px', position=0)

        with use_scope("main", clear=True):
        
            put_text("SEAT MATRIX"),
            put_table(self.seat_matrix_table,header=["Sr.", "Branch", "Vacancies"]) 
            data = input_group("Press button to return to menu",[actions('', [ {'label': 'Back', 'value': 1},], name='action', help_text=None),])
        clear('ROOT')        
        
    def find_record(self, name, pswd= None):
        with open("datasheet.csv",'r') as f:
            reader_object = reader(f)
            if pswd== None:
                for row in reader_object:
                    if(row[0]==name):
                        # return the row no. where record is found, password of that record
                        return reader_object.line_num, row[8]
            else:
                for row in reader_object:
                    if(row[0]==name) and row[8]==pswd:
                        # return the row no. where record is found
                        return reader_object.line_num
        # if record not found, return 0            
        return 0 
              

    def view_branchwise_allotment(self):
        # if allotment_done is T, input the branch name, print branchwise result list, else say that allotment is yet to be done.
        if mymachine.allotment_done== False:
            with use_scope('ROOT'):
                put_image(header_img, width='100%', height='40px', position=0)
            with use_scope("main", clear=True):
                put_info("Allotment is not yet done. Please check again later.")
                data = input_group("Press button to return to menu",[actions('', [ {'label': 'Back', 'value': 1},], name='action', help_text=None),])
            clear('ROOT')
            
        else:
            with use_scope('ROOT'):
                put_image(header_img, width='100%', height='40px', position=0)
            with use_scope("main", clear=True):
                branch= select("Select a branch",options=[{"label": "Computer Engineering", "value":"Computer", "selected":True},{"label": "IT Engineering", "value":"IT"},{"label": "Mechanical Engineering", "value":"Mechanical"},{"label": "Electronics Engineering", "value":"Electronics"}])
                #style(put_text(f"Allotment result for {branch} engineering"),"color:darkgreen")
                df = pd.read_csv('datasheet.csv')
                # filter the result table for the inputted branch and display rank wise (rank, name, surname, email, marks, allotment)
                fa_table_df= df[["NAME","SURNAME","GENDER","EMAIL_ID","MARKS", "ALLOTMENT"]]
                fa_table_cond= fa_table_df[fa_table_df["ALLOTMENT"]==branch]
                fa_table_cond.head()
                fa_table_cond = fa_table_cond.sort_values('MARKS', ascending = False)
                fa_table= fa_table_cond.values.tolist()
                style(put_text(f"Allotment result: {len(fa_table)} students were alloted a seat in {branch} engineering: "),"color:darkgreen")
                put_table(fa_table,header=["NAME","SURNAME","GENDER","EMAIL_ID","MARKS", "ALLOTMENT"])

                data = input_group("Press button to return to menu",[actions('', [ {'label': 'Back', 'value': 1},], name='action', help_text=None),])
            clear('ROOT')
            

    def search_student(self):
        if user==2:
            # for user= student, show only his record.(all columns)
            global name,pwd
            with open("datasheet.csv",'r') as f:
                reader_object = reader(f)
                for row in reader_object:
                    if(row[0]==name) and row[8]==pwd:
                        if(row[4] == '-1' and row[5] == '-1' and row[6] == '-1'):
                            put_error("Your Application is incomplete, please fill all the required details.")
                            
                        with use_scope('ROOT'):
                            put_image(header_img, width='100%', height='40px', position=0)
                        with use_scope("main", clear=True):    
                            style(put_text("Applicant details: "), "color: darkblue")
                        
                            put_table([["Name", f"{row[0]} {row[1]}"],
                            ["Email",f"{row[2]}"],
                            ["Gender", f"{row[9]}"],
                            ["Marks",f"{row[3]}"],
                            ["Preference 1 code",f"{row[4]}"],
                            ["Preference 2 code",f"{row[5]}"],
                            ["Preference 3 code",f"{row[6]}"],
                            ])
                        
                            if mymachine.allotment_done== True:
                                if (row[7]!="-"):
                                        put_success(f"\nCongratulations! Your alloted branch: {row[7]} Engineering") 
                                else:
                                        put_info("Sorry! No seat alloted in this round.")  
                            else:
                                put_info("Allotment is not yet done.")
                            data = input_group("Press button to return to menu",[actions('', [ {'label': 'Back', 'value': 1},], name='action', help_text=None),])
                        clear('ROOT')    
                        return             
            put_error("Sorry! No record found.")            
            
        if user==3:
            # for user= admin, show details of any student
            data = input_group("Search a student record",[input('Enter student name', type=TEXT, name='name',required=True), input('Enter student surname', name='srname', type=TEXT, required=True)])
            name = data["name"]
            srname= data["srname"]
            with open("datasheet.csv",'r') as f:
                reader_object = reader(f)
                for row in reader_object:
                    if(row[0]==name) and row[1]==srname:
                        with use_scope('ROOT'):
                            put_image(header_img, width='100%', height='40px', position=0)
                            # if(int(row[4]) == -1) and (int(row[5]) == -1) and (int(row[6]) == -1):  
                            #     with use_scope("main", clear=True):
                            #         put_error("Application is incomplete")
                            #     time.sleep(2)
                            #     clear('ROOT')
                            #     return    
                            #else:
                            
                        with use_scope("main", clear=True):    
                            style(put_text("Applicant details: "), "color: darkblue")
                    
                        put_table([["Name", f"{row[0]} {row[1]}"],
                        ["Email",f"{row[2]}"],
                        ["Marks",f"{row[3]}"],
                        ["Gender", f"{row[9]}"],
                        ["Preference 1 code",f"{row[4]}"],
                        ["Preference 2 code",f"{row[5]}"],
                        ["Preference 3 code",f"{row[6]}"],
                        ])
                        if(int(row[4]) == -1) and (int(row[5]) == -1) and (int(row[6]) == -1):   
                            put_error("Application is incomplete")
                            
                        if mymachine.allotment_done== True:
                            if (row[7]!="-"):
                                put_success(f"\nAlloted branch: {row[7]} Engineering") 
                            else:
                                put_info("No seat alloted in this round.")     
                        else:
                            put_error("Allotment not done yet")
                        data = input_group("Press button to return to menu",[actions('', [ {'label': 'Back', 'value': 1},], name='action', help_text=None),])
                        clear('ROOT')     
                        return
            put_error("Sorry! No record found")            
            

    def set_cutoff_marks(self):
        
        self.cutoff_marks["Computer"]= mymachine.get_cutoffs("comp")
        self.cutoff_marks["IT"]= mymachine.get_cutoffs("it")
        self.cutoff_marks["Mechanical"]= mymachine.get_cutoffs("mech")
        self.cutoff_marks["Electronics"]= mymachine.get_cutoffs("entc")
    

    def view_cutoff_marks(self):
        # if allotment is done, display this table
        if mymachine.allotment_done== False:
            with use_scope('ROOT'):
                put_image(header_img, width='100%', height='40px', position=0)
            with use_scope("main", clear=True):
                put_info("Allotment is not yet done. Please check again later.")
                data = input_group("Press button to return to menu",[actions('', [ {'label': 'Back', 'value': 1},], name='action', help_text=None),])
            clear('ROOT')
            
        else:
            self.set_cutoff_marks()
            with use_scope('ROOT'):
                put_image(header_img, width='100%', height='40px', position=0)
            with use_scope("main", clear=True):
                style(put_text("Branchwise Cutoff Marks"), "color: darkblue")
                put_table([
                    {"Branch": "Computer Engineering", "Cutoff marks": self.cutoff_marks["Computer"]},
                    {"Branch": "IT Engineering", "Cutoff marks": self.cutoff_marks["IT"]},
                    {"Branch": "Mechanical Engineering", "Cutoff marks": self.cutoff_marks["Mechanical"]},
                    {"Branch": "Elecronics Engineering", "Cutoff marks": self.cutoff_marks["Electronics"]},
                ],header=["Branch", "Cutoff marks"])

                data = input_group("Press button to return to menu",[actions('', [ {'label': 'Back', 'value': 1},], name='action', help_text=None),])
            clear('ROOT')

    def edit_record(self):
        #allow only if allotment is not yet done
        global name, pwd
        row_to_edit = self.find_record(name, pwd)
        if row_to_edit>0:
            if mymachine.allotment_done== True:
                with use_scope('ROOT'):
                    put_image(header_img, width='100%', height='40px', position=0)
                with use_scope("main", clear=True):
                    put_info("Sorry! You cannot edit the application now.")
                    with open("datasheet.csv",'r') as f:
                        reader_object = reader(f)
                        for row in reader_object:
                            if(row[0]==name) and row[8]==pwd:
                                style(put_text("Applicant details: "), "color: darkblue")
                        
                                put_table([["Name", f"{row[0]} {row[1]}"],
                                ["Email",f"{row[2]}"],
                                ["Marks",f"{row[3]}"],
                                ["Gender", f"{row[9]}"],
                                ["Preference 1 code",f"{row[4]}"],
                                ["Preference 2 code",f"{row[5]}"],
                                ["Preference 3 code",f"{row[6]}"],
                                ])
                                put_info(f"\nYour alloted branch: {row[7]}") 
                    data = input_group("Press button to return to menu",[actions('', [ {'label': 'Back', 'value': 1},], name='action', help_text=None),])
                clear('ROOT')             
            else:
                with use_scope('ROOT'):
                    put_image(header_img, width='100%', height='40px', position=0)
                
                with open("datasheet.csv",'r') as f:
                    lines= f.read().splitlines()
                    with use_scope("main", clear=True):
                        data1 = input_group("Fill your application details",[
                        input('Email address', name='email', type=TEXT, required=True),
                        radio(label="Gender", name='Gender', options=[("Male",1),("Female",2)], required=True, inline=True, value=None),
                        input('CET Marks', name='marks', type=NUMBER, required=True, help_text="Enter score out of 200.",validate=check_cet),
                        file_upload(label="CET Scorecard", accept=".pdf", name='cet_score_file',max_size='10M', placeholder="choose a file")
                        ],)

                        surname=(lines[row_to_edit-1]).split(",")[1]
                        email = data1["email"]
                        gender= 'M' if (data1["Gender"]==1) else 'F'
                        marks = data1["marks"]
                        cet_scorecard = data1["cet_score_file"]

                        data2 = input_group("Enter your branch preference",[
                        select('1st Preference:', name='pref1', options=[("Computer (pref code:0)",0),("IT (pref code:1)",1),("Mechanical (pref code:2)",2), ("Electronics (pref code:3)",3)], required=True),
                        select('2nd Preference:', name='pref2', options=[("Computer (pref code:0)",0),("IT (pref code:1)",1),("Mechanical (pref code:2)",2), ("Electronics (pref code:3)",3)], required=True),
                        select('3rd Preference:', name='pref3', options=[("Computer (pref code:0)",0),("IT (pref code:1)",1),("Mechanical (pref code:2)",2), ("Electronics (pref code:3)",3)], required=True),
                        ],)
                        pref1 = data2["pref1"]
                        pref2 = data2["pref2"]
                        pref3 = data2["pref3"]
                        allotment = "-"
                        lines[row_to_edit-1]=f"{name},{surname},{email},{marks},{pref1},{pref2},{pref3},'-',{pwd},{gender}"
                    
                    with open("datasheet.csv",'w') as f:
                        # overwrite
                        for line in lines:
                            f.write(line+"\n")

                    put_success("Details saved successfully!") 
                    time.sleep(1)
                    clear('ROOT')
                    clear("main")   
        else:
            with use_scope('ROOT'):
                    put_image(header_img, width='100%', height='40px', position=0)
            with use_scope("main", clear=True):
                put_error("Error: Student Record not found. Try registering on the website again.")           
                data = input_group("Press button to return to menu",[actions('', [ {'label': 'Back', 'value': 1},], name='action', help_text=None),])
            clear('ROOT')


    def delete_record(self):
        #allow only if allotment is not yet done
        if mymachine.allotment_done== True:
            with use_scope('ROOT'):
                put_image(header_img, width='100%', height='40px', position=0)
            with use_scope("main", clear=True):
                put_info("Sorry! You cannot withdraw the application now. Your registered details: ")
                with open("datasheet.csv",'r') as f:
                    reader_object = reader(f)
                    for row in reader_object:
                        if(row[0]==name) and row[8]==pwd:
                            put_table([["Name", f"{row[0]} {row[1]}"],
                                ["Email",f"{row[2]}"],
                                ["Marks",f"{row[3]}"],
                                ["Gender", f"{row[9]}"],
                                ["Preference 1 code",f"{row[4]}"],
                                ["Preference 2 code",f"{row[5]}"],
                                ["Preference 3 code",f"{row[6]}"],
                                ])
                            put_info(f"\nYour alloted branch: {row[7]}") 
                data = input_group("Press button to return to menu",[actions('', [ {'label': 'Back', 'value': 1},], name='action', help_text=None),])
            clear('ROOT') 
        else:
            with use_scope('ROOT'):
                put_image(header_img, width='100%', height='40px', position=0)
            with use_scope("main", clear=True): 
                confirmation = input_group("Confirmation: Do you wish to remove your record permanently?",
                [actions("",[
                    {"label":"YES","value":"y"}, {"label":"NO", "value":"n"}
                    ],name="action", help_text="On selecting yes, you will get logged out automatically")])
                if confirmation["action"]=="y":
                    row_to_edit = self.find_record(name, pwd)
                    if row_to_edit>0:
            
                        with open("datasheet.csv",'r') as f:
                            lines= f.read().splitlines()
                            del lines[row_to_edit-1]
                        with open("datasheet.csv",'w') as f:
                        # overwrite
                            for line in lines:
                                f.write(line+"\n")
                        put_info("Your application was removed.")
                        self.flag=1
                        time.sleep(1)
                        clear('ROOT')
                        return
                    else: 
                        put_error("Error: Student Record not found. Please register yourself.")
                else:
                    clear('ROOT')
                    clear("main")
                    return    
            
            
    def students_without_allotment(self):
        # allow only after allotment is done
        with use_scope('ROOT'):
                put_image(header_img, width='100%', height='40px', position=0)
        if mymachine.allotment_done== False:
            with use_scope("main", clear=True) :
                put_info("Allotment is not yet done. Please check again later.")
                data = input_group("Press button to return to menu",[actions('', [ {'label': 'Back', 'value': 1},], name='action', help_text=None),])
   
        else:   
            no_allot_list= mymachine.get_no_allotment_data() 
            with use_scope("main", clear=True) :
                put_info(f"{len(no_allot_list)} Student(s) with complete applications were not alloted any seat:")
            
                put_table([[f"{person[0]}",f"{person[1]}"] for person in no_allot_list], header=["NAME", "SURNAME"])
                data = input_group("Press button to return to menu",[actions('', [ {'label': 'Back', 'value': 1},], name='action', help_text=None),])
        clear('ROOT') 
        clear("main")

    def vacancies_left(self):
        with use_scope('ROOT'):
                put_image(header_img, width='100%', height='40px', position=0)
        with use_scope("main", clear=True) :        
            style(put_text("Branchwise Vacancies left"), "color: darkblue" )
            self.vacancies= mymachine.vacancies
            put_table([
                    {"Branch": "Computer Engineering", "Vacancies": self.vacancies[0]},
                    {"Branch": "IT Engineering", "Vacancies": self.vacancies[1]},
                    {"Branch": "Mechanical Engineering", "Vacancies": self.vacancies[2]},
                    {"Branch": "Electronics Engineering", "Vacancies": self.vacancies[3]},
                ],header=["Branch", "Vacancies"])

            data = input_group("Press button to return to menu",[actions('', [ {'label': 'Back', 'value': 1},], name='action', help_text=None),])
        clear('ROOT')    
            
    def encrypt(self,plaintext, offset=14):
        ciphertext=""
        for char in plaintext:
            if (char.isupper()):  
                ciphertext += chr((ord(char) + offset - 64) % 26 + 65)  
        
            elif(char.islower()):  
                ciphertext += chr((ord(char) + offset - 96) % 26 + 97)
            else:
                ciphertext += char 
        return ciphertext             
    

    
    def student_sign_up(self):
        
        signup_img = open('images/sign_up_img.jpg', 'rb').read()
        with use_scope("main", clear=True):
            put_image(signup_img,width='150%',height='400px')
            put_image(privacy_policy_img, width='70%', height= '200px')
            data = input_group("Student sign up info",[input('Enter your Name', type=TEXT, name='name',required=True), input('Enter your Surname', name='surname', type=TEXT, required=True)])

        #check whether the person has already signed up
        with open ('datasheet.csv', 'r') as f_object: 
            reader_obj= reader(f_object)
            for row in reader_obj:
                if row[0]==data['name'] and row[1]==data['surname']:
                    with use_scope("main"):
                        put_error(f"Account already exists for {data['name']} {data['surname']}.")
                    time.sleep(2)
                    clear("main")
                    return

        # if they havent signed up already, ask them to set password and add a new record. 
        with use_scope("main"):
            pswd_1="def1"
            pswd_2="def2"
            while(pswd_1!=pswd_2):
                pswd_data= input_group("",[
                    input("Set your password: ", type=PASSWORD, required=True, name="pswd_1"),
                    input("Confirm password: ", type=PASSWORD, required=True, name="pswd_2"),
                ])
                pswd_1= pswd_data["pswd_1"]
                pswd_2= pswd_data["pswd_2"]
                if(pswd_1!=pswd_2):
                    put_error("Passwords do not match, please try again!")
                    time.sleep(1)
        
        cipher_pwd = self.encrypt(pswd_2)
        with open('datasheet.csv', 'a+', newline='') as f_object: 
            writer_object = writer(f_object) 
            email = "-"
            gender="Not specified"
            marks = 0
            pref1 = -1
            pref2 = -1
            pref3 = -1
            allotment = '-'
            record = [data['name'], data['surname'], email, marks, pref1, pref2, pref3,allotment,cipher_pwd,gender]
            writer_object.writerow(record) 
            f_object.close()
        with use_scope("main"):    
            put_success("\nYou have signed up successfully!")
        time.sleep(2)
        clear("main")
        
    def check_pswd(self, name):
        password = input("Enter your password: ", type=PASSWORD)
        cipher_pwd = self.encrypt(password)
        with open("datasheet.csv",'r') as f:
            reader_object = reader(f)
            for row in reader_object:
                if(row[0]==name) and row[8]==(cipher_pwd):
                    global pwd
                    pwd= cipher_pwd
                    return(1)
        return 0 
    
    def change_password(self):
        global pwd
        row_to_edit = self.find_record(name, pwd)
        clear("main")
        with use_scope('ROOT'):
                put_image(header_img, width='100%', height='40px', position=0)
        with use_scope("main", clear=True) :       
            pswd_data= input_group("",[
                    input("Current password: ", type=PASSWORD, required=True, name="pswd_cur"),
                    input("Set your new password: ", type=PASSWORD, required=True, name="pswd_new1"),
                    input("Confirm password: ", type=PASSWORD, required=True, name="pswd_new2"),
                ])
            if (pwd == self.encrypt(pswd_data["pswd_cur"])) and (pswd_data["pswd_new1"]== pswd_data["pswd_new2"]):
                changed_pwd= self.encrypt(pswd_data["pswd_new2"]) 
                print("reached here")
                with open("datasheet.csv",'r') as f:
                    lines= f.read().splitlines()
                    fields=[]
                    fields=lines[row_to_edit-1].split(',')
                    lines[row_to_edit-1]= f"{fields[0]},{fields[1]},{fields[2]},{fields[3]},{fields[4]},{fields[5]},{fields[6]},{fields[7]},{changed_pwd},{fields[9]}"
                print("reached after line split")
                with open("datasheet.csv",'w') as f:
                    # overwrite
                    for line in lines:
                        f.write(line+"\n")   

                pwd= changed_pwd 
            
                put_success("Password changed successfully!")
            else:
                put_error("Error. Passwords do not match. Please try again!")
        time.sleep(2)
        clear('ROOT')
        clear("main")                    

    def view_full_allotment(self):
        with use_scope('ROOT'):
                put_image(header_img, width='100%', height='40px', position=0)
        
        
        df = pd.read_csv('datasheet.csv')   
        if (mymachine.allotment_done== True):
            with use_scope("main", clear=True) :
                # print table of all records (name, surname, email, marks)
                fa_table_df= df[["NAME","SURNAME","GENDER","EMAIL_ID","MARKS", "ALLOTMENT"]]
                fa_table_df.head()
                fa_table_df = fa_table_df.sort_values('MARKS', ascending = False)
                fa_table= fa_table_df.values.tolist()
                
                style(put_text("Full Allotment Result: "), "color: darkblue" )
                put_table(fa_table,header=["NAME","SURNAME","GENDER","EMAIL_ID","MARKS", "ALLOTMENT"])
                data = input_group("Press button to return to menu",[actions('', [ {'label': 'Back', 'value': 1},], name='action', help_text=None),])
            clear('ROOT')
        else:
            with use_scope("main", clear=True) :
                put_info("Allotment not yet done... Please visit the page later for result.")
                
                fa_table_df= df[["NAME","SURNAME","GENDER","EMAIL_ID","MARKS"]]
                fa_table_df.head()
                fa_table_df = fa_table_df.sort_values('MARKS', ascending = False)
                fa_table= fa_table_df.values.tolist()
                style(put_text(f" {len(fa_table)} Registrations found :"), "color: darkblue" )
                put_table(fa_table,header=["NAME","SURNAME","GENDER","EMAIL_ID","MARKS"])
                data = input_group("Press button to return to menu",[actions('', [ {'label': 'Back', 'value': 1},], name='action', help_text=None),])
            clear('ROOT')
        
        

    student_options=[view_seatmatrix, edit_record, search_student, delete_record, view_cutoff_marks,vacancies_left,change_password]
    admin_options=[mymachine.run_allotment, view_full_allotment, view_branchwise_allotment, search_student, students_without_allotment, vacancies_left]   
    

    
