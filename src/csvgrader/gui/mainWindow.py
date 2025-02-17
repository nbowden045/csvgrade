from tkinter import *
from tkinter import ttk, filedialog, simpledialog
import os
import webbrowser
from dataforms.teams import Groups

import pandas as pd

pd.options.mode.copy_on_write = True

rubric = {"1":{"1_1":"fail", "2_1":"ish", "3_1":"pass"}, "2":{"1_3":"fail", "2_2":"ish", "3_2":"pass"}}

grp = {1:["jim", "bob"], 2:"carl,sam,jill".split(",")}



class MainWindow:




    ###################################################################
    #######   UI Definitions and Generators (including init)    #######
    ###################################################################

    def __init__(self):
        # State variables used 
        self.gbLoad=False
        self.assignmentsLoaded = True # This is True for testing 
        self.newGroups = False
        self.groupsLoaded = False
        self.groupGrade = True


        # Vairables used in grading loops 
        self.studentGrade = {}
        self.groups = Groups()
        self.currentNetID = ""


        self.root = Tk()
        self.root.title("Grading Program!")
        self.root.geometry("900x600")
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)

        self.frm = ttk.Frame(self.root)
        self.frm.grid(column=0,row=0,sticky=(N,E,S,W))       
        self.frm.grid_rowconfigure(0, weight=1)
        self.frm.grid_columnconfigure(0,weight=1)

        
        # Everything is laid out in a tabbed config
        self.tabs = ttk.Notebook(self.frm)

        self.tabs.grid(column=0, row=0, sticky=(N,E,S,W), padx=10, pady=10)

        # Each tab is a frame
        self.grade = ttk.Frame(self.tabs)
        self.grade.grid(column=0,row=0,sticky=(N,E,S,W))
        self.grade.grid_rowconfigure(0, weight=1)
        self.grade.grid_columnconfigure(0,weight=1)


        self.config = ttk.Frame(self.tabs)
        
        self.config.grid(column=0,row=0,sticky=(N,E,S,W))
        self.config.grid_rowconfigure(0, weight=1)
        self.config.grid_columnconfigure(0, weight=1)

        
        self.tabs.add(self.config, text="Configure")

        self.tabs.add(self.grade, text="Grader", state="disable")

        # Generates the configuration tab to make the code a bit nicer
        self.configureTab(self.config)
        #self.gradeTab(self.grade)

        



    def configureTab(self, tab:ttk.Frame):
        # File Input! Yay!


        gbFrame = ttk.Frame(tab)
        gbFrame.grid(row=0, column=0,sticky="NEW")
        tab.grid_rowconfigure(0, weight=1)
        tab.grid_columnconfigure(0,weight=1)

        ttk.Label(gbFrame, text="Gradebook CSV Path").grid(row=1, column=2, sticky="NWE")
        self.gbook_path = StringVar(value=os.getcwd())
        ttk.Entry(gbFrame, textvariable=self.gbook_path, width=50).grid(row=2, column=1, columnspan = 4, sticky="NWE")
        ttk.Button(gbFrame, text="Select File", command=lambda: self.getPaths(self.gbook_path)).grid(row=2, column=6, sticky=(N,W))
        ttk.Button(gbFrame, text="Load Gradebook", command=self.loadGradeBook).grid(row=3, column=2, columnspan=2, sticky="N")

        aFrame = ttk.Frame(tab)
        aFrame.grid(row=1, column=0, sticky=(N,W))
        tab.grid_rowconfigure(1, weight=1)


        ttk.Label(aFrame, text="Assignment Dirs").grid(row=1, column=2, sticky="NWE")
        self.submission_path = StringVar(value=os.getcwd())
        ttk.Entry(aFrame, textvariable=self.submission_path, width=50).grid(row=2, column=1, columnspan = 4, sticky="NWE")
        ttk.Button(aFrame, text="Select Directory", command=lambda: self.getPaths(self.submission_path, mode="dir")).grid(row=2, column=6, sticky=(N,W))
        ttk.Button(aFrame, text="Load Submissions", command=self.loadSubmissions).grid(row=3, column=2, columnspan=2, sticky="N")

        grFrame = ttk.Frame(tab)
        grFrame.grid(row=2, column=0, sticky="NEW")
        tab.grid_rowconfigure(2, weight=1)

        ttk.Label(grFrame, text="Group Import").grid(row=1, column=2, sticky="NWE")
        self.groups_path = StringVar(value=os.getcwd())
        ttk.Entry(grFrame, textvariable=self.groups_path, width=50).grid(row=2, column=1, columnspan = 4, sticky="NWE")
        ttk.Button(grFrame, text="Open CSV File", command=lambda: self.getPaths(self.groups_path, mode="csv")).grid(row=2, column=6, sticky=(N,W))
        ttk.Button(grFrame, text="Load Groups", command=self.genGroups).grid(row=3, column=2, sticky="NEW")
        ttk.Button(grFrame, text="New Groups", command=self.genGroups).grid(row=3, column=3, sticky="NEW")


        ttk.Button(tab, text="Start Grading", command=self.enableGrading).grid(row=3, column=0, sticky="NW")
        tab.grid_rowconfigure(3, weight=1)

        

    def gradeTab(self, tab:ttk.Frame):

        # Going to be a grid of frames here!
        # First the rubric Section !
        rFrame = ttk.Labelframe(tab, text="rubric")
        rFrame.grid(row=0, column=0, sticky="NSWE")
        rFrame.grid_columnconfigure(0, weight=1)
        rFrame.grid_columnconfigure(1, weight=2)
        
        self.displayRubric(rFrame)
        # Then display student info
        iFrame = ttk.Labelframe(tab, text="Student Info")
        iFrame.grid(row=0, column=1, sticky="NSWE")
        tab.grid_columnconfigure(1,weight=1)
        iFrame.grid_columnconfigure(0, weight=1)
        iFrame.grid_columnconfigure(1, weight=1, minsize=100)     

        self.studentName = StringVar(value="N/A")
        ttk.Label(iFrame, text="Name:").grid(row=0, column=0, sticky='ne')
        ttk.Label(iFrame, textvariable=self.studentName).grid(row=0, column=1, sticky='nw')
        
        self.netID = StringVar(value="N/A")
        ttk.Label(iFrame, text="NetID:").grid(row=1, column=0, sticky='ne')
        ttk.Label(iFrame, textvariable=self.netID).grid(row=1, column=1, sticky='nw')
       
        self.studentSection = StringVar(value="N/A")
        ttk.Label(iFrame, text="Section:").grid(row=2, column=0, sticky="NE")
        ttk.Label(iFrame, textvariable=self.studentSection).grid(row=2, column=1, sticky="NW")

        gFrame = ttk.Labelframe(tab, text="Groups")
        gFrame.grid(row=0, column=2, sticky="NSWE")
        tab.grid_columnconfigure(2,weight=1)
        gFrame.grid_columnconfigure(0,weight=1)
        gFrame.grid_rowconfigure(0,weight=1)

        self.groupTree = ttk.Treeview(gFrame))

        self.genGroupTree(self.groupTree)

        #self.displayStudentInfo()

        self.groupTree.grid(row=0, column=0, sticky="NSWE")
        
        self.addCurSelB = ttk.Button(gFrame, text="Assign Current", command=self.assignToGroup, state='disabled')
        self.addCurSelB.grid(row=1, column=0, sticky="N")
        ttk.Button(gFrame, text="New Group", command=self.newGroup).grid(row=3, column=0, sticky="N")

        self.addNetCurB = ttk.Button(gFrame, text="Add NetID", command=self.addByNet, state='disabled')
        self.addNetCurB.grid(row=2, column=0, sticky="N")

        ttk.Button(tab,text="prev", command=self.gradePrev).grid(row = 1, column=0, sticky=W)
        ttk.Button(tab, text="next", command=self.gradeNext).grid(row=1, column=2, sticky=E)

        self.currentSubmission = StringVar(value="?/?")
        ttk.Label(tab, textvariable=self.currentSubmission).grid(row=1, column = 1, sticky=N)
 
        # ttk.Label(iFrame, text="test").grid(column=0, row=0, sticky="w")
        # ttk.Label(gFrame, text="this").grid(column=0, row=0)


        
    def displayRubric(self, root):
        # Create UI elements
        # Thanks chatGPT!
        row = 0
        for (outer_key, inner_dict) in self.rubric.items():
            
            ttk.Label(root, text=f"{outer_key}:").grid(row=row, column=0, sticky=W)
            row+=1
            # Variable to store selected option for this category {cat:[grade:comment]}
            self.studentGrade[outer_key] = [StringVar(value=""), StringVar(value="")]
            for (inner_key, value) in inner_dict.items():
                ttk.Radiobutton(root, text=value, variable=self.studentGrade[outer_key][0], value=inner_key).grid(row=row, column=0, sticky=W)
                row+= 1

            ttk.Label(root, text="Comments?").grid(row=row+1, column=0, columnspan=2, sticky="w")
            ttk.Entry(root, textvariable=self.studentGrade[outer_key][1], width=50).grid(row=row+2, column=0, columnspan=2, sticky=W)
            row += 3
            

    def selectGroup(self):
        pass

    def genGroupTree(self, tree:ttk.Treeview, groups:dict=grp):
        for gid, netids in groups.values():
            tree.insert('', tk.END, text=str(gid), iid)





    ###########################################
    ####### Getter and setter functions #######
    ###########################################

    def assignToGroup(self, groupID:int, netID:str):
        self.groups.addStudent(groupID, netID)

    def assignToNew(self, netID:str):
        self.groups.addGroup(students=[netID])

    def addByNet(self, netID:str, groupID:int):
        netID = ttk.di



    
    def getPaths(self, stvar:StringVar, mode:str="csv"):
        allowedFiles=(("Comma Seperated Value", "*.csv"), ("all files", "*.*"))
        if mode == "csv":
            stvar.set(filedialog.askopenfilename(filetypes=allowedFiles, initialdir=os.getcwd()))
        elif mode == "dir":
            stvar.set(filedialog.askdirectory(initialdir=os.getcwd()))

    def loadGradeBook(self):
        self.rubric = rubric
        #self.displayRubric()
        self.gbLoad = True

    def loadSubmissions(self):
        pass

    def importGroups(self):
        self.groups.importGroups(self.groups_path.get())


    ###############################
    ###### Driver functions #######
    ###############################

    def run(self):
        self.root.mainloop()


    def enableGrading(self):
        if self.gbLoad and self.assignmentsLoaded:
            self.gradeTab(self.grade)
            self.tabs.tab(1,state="normal")


            print("setState")

    def gradeNext(self):
        pass

    def gradePrev(self):
        pass

    def updateGrades(self):
        pass

    def genGroups(self, path:str=None):
        if path:
            self.importGroups(path)
        self.newGroups = True

    def saveGroups(self):
        pass


    def processErrors(self, level, msg):
        pass 

    def displayError(self, msg, title:str="Attention!"):
        pass
