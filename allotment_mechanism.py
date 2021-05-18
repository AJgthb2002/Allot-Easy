import time
import pandas as pd
from csv import *
from pywebio.input import *
from pywebio.output import *

header_img = open('images/header_new.jpg', 'rb').read()  
success_image= open("images/success.png", 'rb').read()  
comp_allotment=[]
IT_allotment=[]
mech_allotment=[]
elec_allotment=[]
all_allotments=[comp_allotment, IT_allotment, mech_allotment, elec_allotment]
no_allotment = []
    
class Allotment_mechanism:
    
    
    def __init__(self):
        self.allotment_done= False
        self.vacancies={0: 120, 1: 60, 2: 60, 3: 120}
        self.flag=0

    def run_allotment(self):
        global comp_allotment, IT_allotment, mech_allotment, elec_allotment, all_allotments, no_allotment
        if self.allotment_done== True:
            with use_scope('ROOT'):
                put_image(header_img, width='100%', height='40px', position=0)
            with use_scope("main", clear=True):
                put_success("Allotment process already done!")
                data = input_group(
                    "Reset Allotment or return to menu",[actions('', [ {'label': 'Back', 'value': 1},{'label': 'Reset', 'value': 2}], name='action', help_text=None),])
                if data["action"]==2:
                    confirmation = input_group("Confirmation: Do you wish to reset all the allotments?",
                                    [actions("",[
                                    {"label":"YES","value":"y"}, {"label":"NO", "value":"n"}
                                    ],name="action")])
                    if confirmation["action"]=="y":
                        self.flag=1
                        self.allotment_done=False 
                        self.vacancies={0: 120, 1: 60, 2: 60, 3: 120}
                        comp_allotment.clear()
                        IT_allotment.clear()
                        mech_allotment.clear()
                        elec_allotment.clear()
                        no_allotment.clear()
                        lines=[]
                        with open("datasheet.csv",'r') as f:
                            lines= f.read().splitlines()
                            for i in range(1, len(lines)):
                                fields=[]
                                fields=lines[i].split(',')
                                lines[i]= f"{fields[0]},{fields[1]},{fields[2]},{fields[3]},{fields[4]},{fields[5]},{fields[6]},-,{fields[8]},{fields[9]}"

                        with open("datasheet.csv",'w') as f:
                            # overwrite
                            for line in lines:
                                f.write(line+"\n")        
                #data = input_group("Press button to return to menu",[actions('', [ {'label': 'Back', 'value': 1},], name='action', help_text=None),])
            clear('ROOT')
        else:
            with use_scope('ROOT'):
                put_image(header_img, width='100%', height='40px', position=0)
            with use_scope("main", clear=True):    
                put_text("Running allotment process.. please wait") 
            
            df = pd.read_csv("datasheet.csv")
                
            allotment_pre = df[(df.PREF1>=0) & (df.PREF2>=0) & (df.PREF3>=0)]
            allotment = allotment_pre.sort_values('MARKS', ascending = False)

            #dict1 = {}
            
            for i in range(len(allotment)):
                nm = allotment.iloc[i][0]
                surname= allotment.iloc[i][1]
                marks= allotment.iloc[i][3]
                pref1= allotment.iloc[i][4]
                pref2= allotment.iloc[i][5]
                pref3= allotment.iloc[i][6]
                
                
               # dict1[f"{i}"]= (nm,surname,marks,pref1,pref2,pref3)
                
                if(self.vacancies[pref1]>0):
                    self.vacancies[pref1]-=1
                    all_allotments[pref1].append((nm, surname))
                elif(self.vacancies[pref2]>0):
                    self.vacancies[pref2]-=1
                    all_allotments[pref2].append((nm, surname))
                elif(self.vacancies[pref3]>0):
                    self.vacancies[pref3]-=1
                    all_allotments[pref3].append((nm, surname))
                else:
                    no_allotment.append((nm, surname))
            
            #****************Allotment done***********************************
            self.update_allotments()
            self.allotment_done= True
            
            with use_scope("main"):
                put_processbar('bar')
                for i in range(1, 11):
                    set_processbar('bar', i / 10)
                    time.sleep(0.1)
                put_image(success_image, width='20%', height='20%')    
                put_success("Allotment process completed.") 
                data = input_group("Press button to return to menu",[actions('', [ {'label': 'Back', 'value': 1},], name='action', help_text=None),])
            clear('ROOT')

    def get_no_allotment_data(self):
        return no_allotment

    def get_row(self, person):
        with open("datasheet.csv",'r') as f: 
            reader_object= reader(f)
            for row in reader_object:
                if(row[0]==person[0]) and row[1]==person[1]:
                    # return the row no. where record is found
                    return reader_object.line_num

    def update_allotments(self):
        global comp_allotment, IT_allotment, mech_allotment, elec_allotment
        row_to_edit =-1
        lines=[]
        with open("datasheet.csv",'r') as f:
            lines= f.read().splitlines()
    
            for person in comp_allotment:
                row_to_edit= self.get_row(person)
                all_fields= lines[row_to_edit-1].split(",")
                lines[row_to_edit-1]=f"{all_fields[0]},{all_fields[1]},{all_fields[2]},{all_fields[3]},{all_fields[4]},{all_fields[5]},{all_fields[6]},Computer,{all_fields[8]},{all_fields[9]}"
            
            for person in IT_allotment:
                row_to_edit= self.get_row(person)
                all_fields= lines[row_to_edit-1].split(",")
                lines[row_to_edit-1]=f"{all_fields[0]},{all_fields[1]},{all_fields[2]},{all_fields[3]},{all_fields[4]},{all_fields[5]},{all_fields[6]},IT,{all_fields[8]},{all_fields[9]}"

            for person in mech_allotment:
                row_to_edit= self.get_row(person)
                all_fields= lines[row_to_edit-1].split(",")
                lines[row_to_edit-1]=f"{all_fields[0]},{all_fields[1]},{all_fields[2]},{all_fields[3]},{all_fields[4]},{all_fields[5]},{all_fields[6]},Mechanical,{all_fields[8]},{all_fields[9]}"


            for person in elec_allotment:
                row_to_edit= self.get_row(person)
                all_fields= lines[row_to_edit-1].split(",")
                lines[row_to_edit-1]=f"{all_fields[0]},{all_fields[1]},{all_fields[2]},{all_fields[3]},{all_fields[4]},{all_fields[5]},{all_fields[6]},Electronics,{all_fields[8]},{all_fields[9]}"
        
        
        with open("datasheet.csv",'w') as f:
            # overwrite
            for line in lines:
                f.write(line+"\n")    
    
    def get_cutoffs(self, branch):
        with open("datasheet.csv",'r') as f:
            reader_object= reader(f)
            if branch=="comp":
                last_person = comp_allotment[-1]
            elif branch =="it":
                last_person = IT_allotment[-1] 
            elif branch =="mech":
                last_person = mech_allotment[-1]  
            elif branch =="entc":
                last_person = elec_allotment[-1]   

            for row in reader_object:
                if row[0]==last_person[0] and row[1]== last_person[1]:
                        # return the marks
                        return row[3]
        
