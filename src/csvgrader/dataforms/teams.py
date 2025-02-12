import json
from dataclasses import dataclass
from enum import Enum
import os.path as osp

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