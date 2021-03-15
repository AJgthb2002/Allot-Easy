import time
from art import *

class Allotment_machanism:
    def __init__(self):
        self.allotment_done= False

    def run_allotment(self):
        if self.allotment_done== True:
            print("Allotment process done!")
        else:
            print("Running allotment process.. please wait") 
            # call functions reqd for allotment
            self.allotment_done= True
            #after 2 secs wait, print the allotment process completed.
            time.sleep(2)
            print("Allotment process completed.") 
            print(tickmark)  