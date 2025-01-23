# Main.py

import pandas as pd
import logging


logging.basicConfig()
class Section:
    def __init__(self, name:str, roster:str = None):
        self.log = logging.getLogger(__name__)
        self.id = name
        self.students
        
    def importRoster(self, roster:str, form:str=None):
        if not(form):
            try:
               form = roster.rsplit('.')[-1]
            except IndexError:
                self.log.warning(f"No format sspecified or detected on file {roster}")
        if form == "csv":
            pass

    def addStudent(self, name:str, netid:str):

        self.Student[netid] = name

    def addStudentCsv(self, roster:pd.DataFrame, nameCol:int, netidcol: int):
        