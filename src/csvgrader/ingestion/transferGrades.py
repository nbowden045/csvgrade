import json, os
import os.path as osp
import tempfile

from common import ClassDef, GradeClass, genInvTeams

if __name__ == "__main__":
    lab: GradeClass = ClassDef.L5E.value
    labNum = "1"

    sourceLoc = osp.join(lab.sourceDir, lab.sourceForm.format(labNum))
    gradesLoc = osp.join(lab.gradesDir, lab.gradesForm.format(labNum))
    invTeams = genInvTeams(lab)

    grades: dict[str, str] = {}
    with open(gradesLoc, "r") as file: #Reading grades
        for idx, line in enumerate(iter(file)):
            currLine = line.strip("\n").strip()
            if idx == 0 or len(currLine) == 0:
                continue
            if currLine == "---EOF---":
                break
            #Date reading

            vals = currLine.split(",")
            grades[vals[0]] = ",".join(vals[1:])

    with tempfile.TemporaryFile("r+") as save:
        with open(sourceLoc, "r") as source:
            sourceIter = iter(source)
            for idx, line in enumerate(sourceIter):
                currLine = line.strip("\n").strip()
                if len(currLine) == 0:
                    save.write(line)
                    continue
                if currLine == "---EOF---":
                    save.write(line)
                    break
                
                if idx == 1:
                    save.write(line)
                else: #Assuming data with people in it
                    vals = currLine.split(",")
                    id = vals[6]

                    if id in ["mabulay2", "saanvik2", "waynec2", "grantem2", "agarbis2"]: #Adding an exception for the LA
                        save.write(line)
                        continue

                    team = invTeams.get(id)
                    if team is None:
                        save.write(line)
                        continue
                    
                    save.write(
                        ",".join(vals[0:6]) + f",{id}," +
                        grades[team] + "\n"
                    )

            for line in sourceIter:
                save.write(line)
        
        save.seek(0)
        with open(sourceLoc, "w") as source:
            for line in save:
                source.write(line)
