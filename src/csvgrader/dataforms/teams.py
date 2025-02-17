import json
import csv
from dataclasses import dataclass, field
from enum import Enum
import os.path as osp

@dataclass
class Groups:
    """Groups object. Stores 

    Raises:
        RuntimeError: _description_
        RuntimeError: _description_
        RuntimeError: _description_

    Returns:
        _type_: _description_
    """

    groupPath:str = None
    _studentList:dict[str, int] = field(default_factory=dict)
    _groupList:dict[int, list[str]] = field(default_factory=dict)
    
    def __post_init__(self):
        if self.groupPath:
            self.importGroups(inpath=self.groupPath)


    def importGroups(self, inpath:str):
        """Imports student group assignment from 

        Args:
            inpath (str): filepath to read from 

        Raises:
            RuntimeError: File doesn't exist
            RuntimeError: Incorrect formatting 
        """
        # Ensures file exists, if not raises error
        if not osp.isfile(inpath):
            raise RuntimeError("Invalid Path")
        
        with open(inpath, 'r') as f:
            reader = csv.reader(f)
            header = next(reader) # Extracts the header of the CSV to ensure formatting
            if header[0] != "NetID" or header[1] != "Group":
                raise RuntimeError("CSV File not of correct format")
            # Itterates over the list and generates the groups
            for line in reader:
                self.addStudent(line[1], line[0])



    def exportGroups(self, outpath:str):
        """Exports the group assignment to CSV. THIS WILL OVERWRITE ANYTHING AT outpath YOU HAVE BEEN WARNED
        Args:
            outpath (str): File path to write out 
        """

        with open(outpath, "w", encoding="UTF-8") as f:
            writer = csv.writer(f)
            writer.writerow(["NetID", "Group"]) # header
            for netID, group in self._studentList.items():
                writer.writerow([netID, group])
    
    def students(self, groupID:int):
        """Get students in a group

        Args:
            groupID (int): group  

        Returns:
            list or None: List of NetID's in group or None
        """
        try:
            return self._groupList[groupID]
        except KeyError:
            return None

    def group(self, netID:str):
        """Get group student is assigned to 

        Args:
            netID (str): Student NetID

        Returns:
            int: groupID of student
        """
        try:
            return self._studentList[netID]
        except KeyError:
            return None

    def addGroup(self, groupID:int=None, students:list=None, groupDict:dict=None, overwrite:bool=False):
        """Create a new group with population given by list of students

        Args:
            groupID (int, optional): ID for group, if left empty it will default to the current max group +1. Defaults to None.
            students (list, optional): list of students to add to the group. Defaults to None.
            groupDict (dict, optional): dictionary of {groupID:[NetID]}. Defaults to None.
            overwrite (bool, optional): if set, If students contains a netID already assigned it will reassign to the new group. Defaults to False.
        """

        # If not specified it will have default value 1 higher than the max. Groups are numbered sequentially
        if not groupID:
            groupID = max(self._groupList.keys())+1

        self._groupList[groupID] = []

        if students:
            for s in students:
                self.addStudent(groupID, s, overwrite=overwrite)

    def addStudent(self, groupID:int, netID:str, overwrite:bool=False):
        """Add student to an existing group and create the group if it doesn't already exist

        Args:
            groupID (int): ID of the group to add to/create 
            netID (str): student NETID
            overwrite (bool, optional): if student is already assigned will move them to the specified group. Defaults to False.

        Raises:
            RuntimeError: if overwrite==false and student already in group 
        """


        # See if student is already in a group
        if self.group(netID):
            # Remove student from old group before reassigning value later
            # if overwrite false this will error 
            if overwrite:
                oldgrp = self.group(netID)
                self._groupList[oldgrp].remove(netID)
            else:
                raise RuntimeError(f"Student {netID} already assigned to group {self.group(netID)}")

        # Check if group exists and if not create a new one
        if groupID not in self._groupList.keys():
            self.addGroup(groupID=groupID)
        # assign group to student and vise versa 
        self._studentList[netID] = groupID
        self._groupList[groupID].append(netID)
        












@dataclass
class GradeClass:
    sourceDir: str
    gradesDir: str
    teamsLoc: str
    recordLoc: str
    gradesForm: str = "lab{}.csv"
    sourceForm: str = "120248-PHYS-211-labs-{}.csv"

def buildStandard(loc: str) -> GradeClass:
    """Builds a class descriptor according to the standard structure

    Args:
        loc (str): The directory with the standard structure in it

    Returns:
        GradeClass: The generated class descriptor
    """
    return GradeClass(
        sourceDir=str(osp.join(loc, "official_grades")),
        gradesDir=str(osp.join(loc, "grades")),
        teamsLoc=str(osp.join(loc, "teams.json")),
        recordLoc=str(osp.join(loc, "to_grade")),
        gradesForm="lab{}.csv",
        sourceForm="120251-PHYS-211-labs-{}.csv"
        )

class ClassDef(Enum):
    """An enum for all of the classes you are grading"""
    # L4E: GradeClass = GradeClass("./official_grades/", "./grades", "./teams.json","lab{}.csv", "120248-PHYS-211-labs-{}.csv")
    L2J: GradeClass = buildStandard("./records/2025/L2J")
    L3M: GradeClass = buildStandard("./records/2025/L3M")
    L5E: GradeClass = buildStandard("./records/2025/L5E")

def genInvTeams(cls: GradeClass) -> dict[str, list[str]]:
    """Generates the inverse member name to team name map

    Args:
        cls (GradeClass): A descriptor of where to find information about the class

    Returns:
        dict[str, list[str]]: The inverse member map for a team. Goes from member name to team name
    """
    with open(cls.teamsLoc, "r") as file:
        teams = json.load(file)
    
    invTeams = {}
    for tName, data in teams.items():
        members = data['members']
        for mem in members:
            invTeams[mem] = tName
    return invTeams

officialGradesSource = "120248-PHYS-211-labs-{}.csv"
officialDir = "./official_grades/"
gradesDir = "./grades"
gradesSource = "lab{}.csv"

teamsLoc = "./teams.json"