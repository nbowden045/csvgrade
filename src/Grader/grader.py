
    """This handles the 

    Raises:
        RuntimeError: _description_
        RuntimeError: _description_

    Returns:
        _type_: _description_
    
    @author Autumn Bauman 
    """


class Grader:
    def __init__(self, gradebookPath:str=None, submitPath:str=None):

        # STATE VARIABLES
        self.submissionsLoaded = False
        self.currentStudent = 0
        self.studentsSubmitted = []
        self.numStudents = 0

        
        # Holds objects useful to this code
        self.rubric = None
        self.gradebook = None
        self.gradebookPath = gradebookPath
        self.submitPath = submitPath
        self.submitList = None

        # Import the gradebook from MyPhysics
        self.gradebook  = pd.read_csv(gradebookPath, dtype=str)


    def GenSubmitList(self, submitPath:str=None, recursive:bool = False):
        """Sorts submissions by timestamp and netID for easy indexing 

        Args:
            submitpth (str): path tp submissions, should be a dir
            recursive (bool): Recursively loads submissions from subdirectories. This can only go one layer deep because I am lazy. Defaults to False

        Raises:
            RuntimeError: No submission path specified
            RuntimeError: path supplied is not a directory

        Returns:
            dict: {NetID:[ordered list of submissions of form [timestamp, path]]}
        """
        if submitPath: 
            self.submitPath = submitPath
        if not self.submitPath:
            raise RuntimeError("No submission directory provided")
        # Ensure we are pointed at a directory 
        if not os.path.isdir(self.submitPath):
            raise RuntimeError("Not a directory and/or does not exist")
        
        submitlist = [] # stores the list of strudent submissions 
        for f in os.listdir(self.submitPath):
            # Loads one dir deep (i.e. late submissions)
            if os.path.isdir(os.path.join(self.submitPath,f)) and resursive: 
                for i in os.listdir(os.path.join(self.submitPath,f)):
                    # Recusion stinky
                    if os.path.isdir:
                        continue

                    split = i.split("_")
                    #print(split)
                    submitlist.append([split[0],int(split[1].split(".")[0]), os.path.join(self.submitPath, f,i)])
                    
            elif os.path.isdir(os.path.join(self.submitPath,f)) and not resursive: 
                continue
            else:
                split = f.split("_")
                #print(split)
                submitlist.append([split[0],int(split[1].split(".")[0]), os.path.join(self.submitPath, f)])
        
        # converts to dataframe to make manipulation easier    
        submitlist = pd.DataFrame(submitlist,columns=["NetID","timestamp","path"])
        # Dictionary of netID:[list of submissions]. Most recent submission accessible at [-1]
        self.submitList = {netid:submitlist[submitlist["NetID"] == netid][["timestamp", "path"]].sort_values(by="timestamp").values.tolist() for netid in submitlist.NetID.unique()}
        
        # We use this to itterate over the class later on, helps keep it nice and encapsulated
        self.studentsSubmitted = self.submitList.keys()
        self.numStudents = len(self.studentsSubmitted)

    def GenRubricItems(self, gradebookPath:str=None):
        """Generate a rubric from the gradebook file as formatted by MyPhysics. 
        If you want this to be better you could add in the ability to specifiy arbitrary formatting
        but im a grad student and I ain't getting paid to use this

        Args:
            gradebookPath (str, optional): Path to gradebook csv file. Defaults to None.
        
        Raises: 
            RuntimeError: No path specified
        """
        # sets path if not specified at creation of class/want to update  
        if gradebookPath:
            self.gradebookPath = gradebookPath
        elif not self.gradebookPath:
            raise RuntimeError("No path to rubric specified")

        # Extracts the rubric information from the submissions 
        crit = self.gradebook[pd.notna(pd.to_numeric(self.gradebook["Rubric Section"], errors="coerce"))]
        # Extract the rucric chriteria from the assignment gradebook and makes a dictionary
        self.rubric = {i : crit[crit["Rubric Section"] == i][["Version", "Student Section"]].set_index("Version").to_dict()["Student Section"] for i in crit["Rubric Section"].unique()}

    def setRubricColumn(self, columnIndex:dict):
        # dictionary of <rubricitem>:<gradebook column> used when exporting
        self.columnIndex = columnIndex


    def getNextStudent(self):
        """Get submission and student information for the next student

        Returns:
            tuple: (netID, submissionsList, firstName, lastName, Section)
        """
        # Gives us wrapping 
        if self.currentStudent >= self.numStudents:
            self.currentStudent = 0
        netID = self.studentsSubmitted[self.currentStudent]
        submission = self.submitList[netID]
        first = self.gradebook.loc[self.gradebook["Student NetID"]==netID, "Student First Name"]
        last = self.gradebook.loc[self.gradebook["Student NetID"]==netID, "Student Last Name"]
        sec = self.gradebook.loc[self.gradebook["Student NetID"]==netID, "Student Section"]
        # Increment
        self.currentStudent += 1
        return (netID, submission, first, last, sec, self.currentStudent)

    def getPrevStudent(self):
            """Get submission and student information for the previous student

        Returns:
            tuple: (netID, submissionsList, firstName, lastName, Section)
        """
        # Gives us wrapping 
        if self.currentStudent <= 0 :
            self.currentStudent = self.numStudents-1
        netID = self.studentsSubmitted[self.currentStudent]
        submission = self.submitList[netID]
        first = self.gradebook.loc[self.gradebook["Student NetID"]==netID, "Student First Name"]
        last = self.gradebook.loc[self.gradebook["Student NetID"]==netID, "Student Last Name"]
        sec = self.gradebook.loc[self.gradebook["Student NetID"]==netID, "Student Section"]
        # decrement
        self.currentStudent -= 1
        return (netID, submission, first, last, sec, self.currentStudent)


"""
    def gradeClass(self):

        # THIS WILL BE REWRITTEN
        if input("start? ") == "n":
            print("nope")
            return
        for netid in self.submitList.keys():
            try:
                print(f"NetID: {netid}, Name: {self.gradebook.loc[self.gradebook['Student NetID'] == netid,'Student First Name'].values[0]}")
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
"""

    def assignGradeStudent(self, netID, grade:dict):

        #assigns a grade to a student across all categories
        for cat, grade in self.rubric.items():

            self.gradebook.loc[self.gradebook["Student NetID"] == netID,self.columnIndex[cat]] = grade[0]
            # Get the index of the gradebook comments column and then go back to column name because I hate pandas sometimes 
            idx = self.gradebook.columns[self.gradebook.columns.get_loc(self.columnIndex[cat])+1]
            self.gradebook.loc[self.gradebook["Student NetID"] == netID, idx] = grade[1]
            

    
    def exportGrades(self, inplace:bool=True, customPath:str=None):
        """Exports assigned grades to the file. If `inplace` it will overwrite the file and if customPath is set
        it will export to this.

        Args:
            inplace (bool, optional): Overwrites the file, if false it will strip the extension and append 'mod.csv' to the end. Defaults to True.
            customPath (str, optional): If you want to write it out . Defaults to gradebookPath.
        """
        
        outpath = self.gradebookPath
        if customPath:
            outpath=customPath

        if not inplace:
            outpath = str(outpath[outpath.rfind('.')]+"mod.csv")
            
        self.gradebook.to_csv(outpath)

