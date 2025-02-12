import json
import os
import os.path as osp

from common import ClassDef, GradeClass

def renameFile(invTeams: dict, dir: str, newFormat = "{team}_{netId}_{data}"):
    files = os.listdir(dir)
    for file in files:
        if not osp.isfile(osp.join(dir, file)):
            continue
        
        _, netId, data = file.split("_")
        team = invTeams.get(netId, "Error")
        newName = newFormat.format(
            netId=netId,
            team=team,
            data=data
        )
        os.rename(osp.join(dir, file), osp.join(dir, newName))
        
def createTeamGrade(dir: str, labName: str, teams: list[str], cols: list[list[str]]):
    with open(osp.join(dir, labName + ".csv"), "w") as file:
        header = ["Team Name"] + cols
        file.write(", ".join(header) + "\n")
        for team in teams:
            file.write(team + ','*len(cols) + "\n")

if __name__ == "__main__":
    lab: GradeClass = ClassDef.L2J.value
    labNum = "2"
    sourceLoc = osp.join(lab.sourceDir, lab.sourceForm.format(labNum))
    
    #Getting the official grades columns and people
    with open(sourceLoc, "r") as file:
        gData = []
        qCols = []
        people = []
        netIds = []

        name2netid = {}

        fiter = iter(file)
        #Getting people info
        for idx, line in enumerate(fiter):
            currLine = line.strip("\n").strip()
            if len(currLine) == 0:
                continue
            if currLine == "---EOF---":
                break
            if idx == 1:
                qCols.extend(currLine.split(',')[7:])
            else:
                gData.append(currLine.split(','))
                people.append(f"{gData[-1][5]} {gData[-1][4]}")
                netIds.append(gData[-1][6])
                name2netid[f"{gData[-1][5]} {gData[-1][4]}"] = gData[-1][6]
            
        
        #Getting key info
        validScores = []
        for idx, line in enumerate(fiter):
            currLine = line.strip("\n").strip()
            if len(currLine) == 0:
                continue
        # for i in range(len(gradeData)):
        #     currLine = gradeData[i]
        #     currLine.strip('\n').strip()
        #     if currLine == "---EOF---":
        #         pass
        #     gradeData[i] = gradeData[i].strip('\n').strip()
        #     gradeData[i] = gradeData[i].split(",")
        #     pName = f"{gradeData[i][5]} {gradeData[i][4]}"
        #     people.append(pName)
        # cols = gradeData[0][6:]
    
    #Getting the team info
    with open(lab.teamsLoc, "r") as file:
        teams: dict = json.load(file)

    invTeams = {}
    for tName, data in teams.items():
        members = data['members']
        for mem in members:
            invTeams[mem] = tName

    renameFile(invTeams, osp.join(lab.recordLoc, f"L{labNum}"))
    createTeamGrade(lab.gradesDir, f"lab{labNum}", teams.keys(), qCols)