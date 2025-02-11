# Main.py
from tkinter import *
from tkinter import ttk, filedialog
import os
import pandas as pd
import webbrowser
import json

filepath = "/home/auttieb/Documents/college/TA/211LSP25/120251-PHYS-211-labs-1.csv"
submitpath = "/home/auttieb/Documents/college/TA/211LSP25/submissions/lab1/L3E"

pd.options.mode.copy_on_write = True

rubric = {"1":{"1_1":"fail", "2_1":"ish", "3_1":"pass"}, "2":{"1_3":"fail", "2_2":"ish", "3_2":"pass"}}



class MainWindow:

    def __init__(self):
        
        self.gbLoad=False
        self.assignmentsLoaded = True

        self.studentGrade = {}


        self.root = Tk()
        self.root.title("Grading Program!")
        self.root.geometry("600x600")
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)

        self.frm = ttk.Frame(self.root)
        self.frm.grid(column=0,row=0,sticky="nsew")
        self.frm.grid_rowconfigure(0, weight=1)
        self.frm.grid_columnconfigure(0,weight=1)
        # Everything is laid out in a tabbed config
        self.tabs = ttk.Notebook(self.frm)
        # Makes the window work, no clue why I need this
        self.tabs.grid(column=0, row=0,sticky=(N,E,S,W))

        # Each tab is a frame
        self.grade = ttk.Frame(self.tabs)
        self.grade.grid(column=0,row=0,sticky="nsew")
        self.grade.grid_rowconfigure(0, weight=1)
        self.grade.grid_columnconfigure(0,weight=1)

        self.config = ttk.Frame(self.tabs)
        
        self.config.grid(column=0,row=0,sticky="n")
        self.config.grid_rowconfigure(0, weight=1)
        self.config.grid_columnconfigure(0,weight=1)

        self.tabs.add(self.config, text="Configure")

        self.tabs.add(self.grade, text="Grader", state="disable")

        # Generates the configuration tab to make the code a bit nicer
        self.configureTab(self.config)
        #self.gradeTab(self.grade)

        

    def run(self):
        self.root.mainloop()


    def configureTab(self, tab:ttk.Frame):
        # File Input! Yay!
        ttk.Label(text="Gradebook CSV Path")
        self.gbook_path = StringVar(value=os.getcwd())
        ttk.Entry(tab, textvariable=self.gbook_path, width=50).grid(row=0, column=0)
        ttk.Button(tab, text="Open File", command=lambda: self.getPaths(self.gbook_path)).grid(column=1, row=0)
        ttk.Button(tab, text="Load Gradebook", command=self.loadGradeBook).grid(column=0, row=1)
            
        ttk.Label(text="Assignment Dirs")
        self.submission_path = StringVar(value=os.getcwd())
        ttk.Entry(tab, textvariable=self.submission_path, width=50).grid(row=2, column=0)
        ttk.Button(tab, text="Open Directory", command=lambda: self.getPaths(self.submission_path, mode="dir")).grid(column=1, row=2)
        ttk.Button(tab, text="Load Assignments", command=self.loadSubmissions).grid(column=0, row=3)

        ttk.Label(text="Group Import")
        self.groups_path = StringVar(value=os.getcwd())
        ttk.Entry(tab, textvariable=self.submission_path, width=50).grid(row=4, column=0)
        ttk.Button(tab, text="Open Directory", command=lambda: self.getPaths(self.groups_path, mode="csv")).grid(column=1, row=4)
        ttk.Button(tab, text="Load Assignments", command=self.importGroups).grid(column=0, row=5)

        ttk.Button(tab, text="Start Grading", command=self.enableGrading).grid(column=1, row=6)

        

    def gradeTab(self, tab:ttk.Frame):
        # Going to be a grid of frames here!
        self.rubricFrame = ttk.Labelframe(tab, text="rubric")
        self.rubricFrame.grid(row=0, column=0, sticky="w")
        self.rubricFrame.grid_rowconfigure(0, weight=1)
        self.rubricFrame.grid_columnconfigure(0,weight=1)
        # Create the rubric section
        self.displayRubric(self.rubricFrame)

        self.infoFrame = ttk.Labelframe(tab, text="Student Info")
        self.infoFrame.grid(row=0, column=1, sticky="w")
        self.infoFrame.grid_rowconfigure(0, weight=1)
        self.infoFrame.grid_columnconfigure(0,weight=1)

        self.groupFrame = ttk.Labelframe(tab, text="Groups")
        self.groupFrame.grid(row=0, column=2, sticky="w")
        self.groupFrame.grid_rowconfigure(0, weight=1)
        self.groupFrame.grid_columnconfigure(0,weight=1)


        ttk.Label(self.infoFrame, text="test").grid(column=0, row=0, sticky="w")
        ttk.Label(self.groupFrame, text="this").grid(column=0, row=0)


        
    def displayRubric(self, contain):
        # Create UI elements
        # Thanks chatGPT!
        for col, (outer_key, inner_dict) in enumerate(self.rubric.items()):
            ttk.Label(contain, text=f"{outer_key}:").grid(row=0, column=col, sticky="w")
            # Variable to store selected option for this category
            self.studentGrade[outer_key] = StringVar(value="")
            for row, (inner_key, value) in enumerate(inner_dict.items(), start=1):
                rb = ttk.Radiobutton(contain, text=value, variable=self.studentGrade[outer_key], value=inner_key)
                rb.grid(row=row, column=col, sticky="w")
                        




    
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
        pass

    def enableGrading(self):
        if self.gbLoad and self.assignmentsLoaded:
            self.gradeTab(self.grade)
            self.tabs.tab(1,state="normal")
            print("setState")



class Groups:
    def __init__(self, groupFile=None):
        if groupFile:
            self.readGroupJson()
            return
        self.grps = {}

    def addStudent(self, group, netID):
        self.grps[group].append(netID)

    def initGroup(self, group:int, netID:list):
        self.grps[group]=netID


    def readGroupJson(self):
        pass


class Grader:
    def __init__(self, gradebookPath:str, submitPath:str):

        self.gradebookPath = gradebookPath
        self.submitPath = submitPath
        # Import the gradebook from MyPhysics
        self.gradebook  = pd.read_csv(gradebookPath, dtype=str)
        self.rubric = self.GenRubric()
        self.GenSubmitList()

    def GenSubmitList(self):
        """Sorts submissions by timestamp and netID for easy indexing 

        Args:
            submitpth (str): path tp submissions, should be a dir

        Raises:
            RuntimeError: path supplied is not a directory

        Returns:
            dict: {NetID:[ordered list of submissions of form [timestamp, path]]}
        """
        if not os.path.isdir(self.submitPath):
            raise RuntimeError("Not a directory and/or does not exist")
        submitlist = []
        for i in os.listdir(self.submitPath):
            if os.path.isdir(os.path.join(self.submitPath,i)): 
                continue
            split = i.split("_")
            #print(split)
            submitlist.append([split[0],int(split[1].split(".")[0]), i])
        submitlist = pd.DataFrame(submitlist,columns=["NetID","timestamp","path"])
        self.submitList = {netid:submitlist[submitlist["NetID"] == netid][["timestamp", "path"]].sort_values(by="timestamp").values.tolist() for netid in submitlist.NetID.unique()}

    def GenRubric(self):
        crit = self.gradebook[pd.notna(pd.to_numeric(self.gradebook["Rubric Section"], errors="coerce"))]
        # Extract the rucric chriteria from the assignment gradebook
        return {i : crit[crit["Rubric Section"] == i][["Version", "Student Section"]].set_index("Version").to_dict() for i in crit["Rubric Section"].unique()}

    def gradeClass(self):
        if input("start? ") == "n":
            print("nope")
            return
        for netid in self.submitList.keys():
            try:
                print(f"NetID: {netid}, Name: {self.gradebook.loc[self.gradebook["Student NetID"] == netid,"Student First Name"].values[0]}")
            except:
                print(f"NetID {netid} not in gradebook, skipping...")
                continue
            webbrowser.open(os.path.join(self.submitPath,self.submitList[netid][-1][1]))
            gradeIn = input("Enter Assigned Grade for contract (1/0 pass fail): ") 
            while True:
                if gradeIn == "1":
                    grade = "2_1"
                    break
                elif gradeIn == "0":
                    grade = "1_1"
                    break
                elif gradeIn == 'x':
                    raise RuntimeError("lol fuck you")
                else:
                    gradeIn = input("Enter Assigned Grade for contract u bitch (1/0 pass fail): ")
            comment = input("Comments?: ")
            self.gradebook.loc[self.gradebook["Student NetID"] == netid,"Q#1: The contract..."] = grade
            self.gradebook.loc[self.gradebook["Student NetID"] == netid, "Q#1 Comments"] = comment

    
    def exportGrades(self):
        self.gradebook.to_csv(str(self.gradebookPath[:-4]+"mod.csv"))



mw = MainWindow()
mw.run()

