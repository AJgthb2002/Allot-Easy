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

stud_menu_img = open('images\student_menu_img.jpg', 'rb').read()
header_img = open('images\header_new.jpg', 'rb').read()

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
                style(put_text(f"Allotment result for {branch} engineering"),"color:darkgreen")
                df = pd.read_csv('datasheet.csv')
                # filter the result table for the inputted branch and display rank wise (rank, name, surname, email, marks, allotment)
                fa_table_df= df[["NAME","SURNAME","EMAIL_ID","MARKS", "ALLOTMENT"]]
                fa_table_cond= fa_table_df[fa_table_df["ALLOTMENT"]==branch]
                fa_table_cond.head()
                fa_table_cond = fa_table_cond.sort_values('MARKS', ascending = False)
                fa_table= fa_table_cond.values.tolist()
                
                put_table(fa_table,header=["NAME","SURNAME","EMAIL_ID","MARKS", "ALLOTMENT"])

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
                            ["Marks",f"{row[3]}"],
                            ["Preference 1 code",f"{row[4]}"],
                            ["Preference 2 code",f"{row[5]}"],
                            ["Preference 3 code",f"{row[6]}"],
                            ])
                        
                            if mymachine.allotment_done== True:
                                put_success(f"\nYour alloted branch: {row[7]} Engineering")
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
                        if(row[4] == '-1' and row[5] == '-1' and row[6] == '-1'):
                            with use_scope("main", clear=True):
                                put_error("Application is incomplete")
                            return    
                        else:
                            
                            with use_scope("main", clear=True):    
                                style(put_text("Applicant details: "), "color: darkblue")
                            
                                put_table([["Name", f"{row[0]} {row[1]}"],
                                ["Email",f"{row[2]}"],
                                ["Marks",f"{row[3]}"],
                                ["Preference 1 code",f"{row[4]}"],
                                ["Preference 2 code",f"{row[5]}"],
                                ["Preference 3 code",f"{row[6]}"],
                                ])
                            
                                if mymachine.allotment_done== True:
                                    if (row[7]!="--"):
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
                    put_info("Cannot edit the application now.")
                    with open("datasheet.csv",'r') as f:
                        reader_object = reader(f)
                        for row in reader_object:
                            if(row[0]==name) and row[8]==pwd:
                                style(put_text("Applicant details: "), "color: darkblue")
                        
                                put_table([["Name", f"{row[0]} {row[1]}"],
                                ["Email",f"{row[2]}"],
                                ["Marks",f"{row[3]}"],
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
                        input('CET Marks', name='marks', type=NUMBER, required=True, help_text="Enter score out of 200.",validate=check_cet),
                        ],)

                        surname=(lines[row_to_edit-1]).split(",")[1]
                        email = data1["email"]
                        marks = data1["marks"]

                        data2 = input_group("Enter your branch preference",[
                        select('1st Preference:', name='pref1', options=[("Computer (pref code:0)",0),("IT (pref code:1)",1),("Mechanical (pref code:2)",2), ("Electronics (pref code:3)",3)], required=True),
                        select('2nd Preference:', name='pref2', options=[("Computer (pref code:0)",0),("IT (pref code:1)",1),("Mechanical (pref code:2)",2), ("Electronics (pref code:3)",3)], required=True),
                        select('3rd Preference:', name='pref3', options=[("Computer (pref code:0)",0),("IT (pref code:1)",1),("Mechanical (pref code:2)",2), ("Electronics (pref code:3)",3)], required=True),
                        ],)
                        pref1 = data2["pref1"]
                        pref2 = data2["pref2"]
                        pref3 = data2["pref3"]
                        allotment = "--"
                        lines[row_to_edit-1]=f"{name},{surname},{email},{marks},{pref1},{pref2},{pref3},'--',{pwd}"
                    
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
                put_info("Cannot withdraw the application now. Your registered details: ")
                with open("datasheet.csv",'r') as f:
                    reader_object = reader(f)
                    for row in reader_object:
                        if(row[0]==name) and row[8]==pwd:
                            for i in range(0,7):
                                put_text(row[i], end="   ")
                            put_info(f"\nYour alloted branch: {row[7]}")  
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
                put_info(f"{len(no_allot_list)} Student(s) were not alloted any seat:")
            
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
                    {"Branch": "Elecronics Engineering", "Vacancies": self.vacancies[3]},
                ],header=["Branch", "Vacancies"])

            data = input_group("Press button to return to menu",[actions('', [ {'label': 'Back', 'value': 1},], name='action', help_text=None),])
        clear('ROOT')    
            
    
    def student_sign_up(self):
        signup_img = open('images\sign_up_img.jpg', 'rb').read()
        with use_scope("main", clear=True):
            put_image(signup_img,width='150%',height='400px')
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
            pswd = input("Set your password: ", type=PASSWORD, required=True)
        with open('datasheet.csv', 'a+', newline='') as f_object: 
            writer_object = writer(f_object) 
            email = "--"
            marks = 0
            pref1 = -1
            pref2 = -1
            pref3 = -1
            allotment = "--"
            record = [data['name'], data['surname'], email, marks, pref1, pref2, pref3, allotment,pswd]
            writer_object.writerow(record) 
            f_object.close()
        with use_scope("main"):    
            put_success("\nYou have signed up successfully!")
        time.sleep(2)
        clear("main")
        
    def check_pswd(self, name):
        password = input("Enter your password: ", type=PASSWORD)
        with open("datasheet.csv",'r') as f:
            reader_object = reader(f)
            for row in reader_object:
                if(row[0]==name) and row[8]==password:
                    global pwd
                    pwd= password
                    return(1)
        return 0 
    
    
    def view_full_allotment(self):
        with use_scope('ROOT'):
                put_image(header_img, width='100%', height='40px', position=0)
        
        
        df = pd.read_csv('datasheet.csv')   
        if (mymachine.allotment_done== True):
            with use_scope("main", clear=True) :
                # print table of all records (name, surname, email, marks)
                fa_table_df= df[["NAME","SURNAME","EMAIL_ID","MARKS", "ALLOTMENT"]]
                fa_table_df.head()
                fa_table_df = fa_table_df.sort_values('MARKS', ascending = False)
                fa_table= fa_table_df.values.tolist()
                
                style(put_text("Full Allotment Result"), "color: darkblue" )
                put_table(fa_table,header=["NAME","SURNAME","EMAIL_ID","MARKS", "ALLOTMENT"])
                data = input_group("Press button to return to menu",[actions('', [ {'label': 'Back', 'value': 1},], name='action', help_text=None),])
            clear('ROOT')
        else:
            with use_scope("main", clear=True) :
                put_info("Allotment not yet done... Please visit the page later for result.")
                
                fa_table_df= df[["NAME","SURNAME","EMAIL_ID","MARKS"]]
                fa_table_df.head()
                fa_table_df = fa_table_df.sort_values('MARKS', ascending = False)
                fa_table= fa_table_df.values.tolist()
                style(put_text("Registrations:"), "color: darkblue" )
                put_table(fa_table,header=["NAME","SURNAME","EMAIL_ID","MARKS"])
                data = input_group("Press button to return to menu",[actions('', [ {'label': 'Back', 'value': 1},], name='action', help_text=None),])
            clear('ROOT')
        
        

    student_options=[view_seatmatrix, edit_record, search_student, delete_record, view_cutoff_marks,vacancies_left]
    admin_options=[mymachine.run_allotment, view_full_allotment, view_branchwise_allotment, search_student, students_without_allotment, vacancies_left]   
    

    