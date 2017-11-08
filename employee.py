# Mitarbeiterklasse als Objekt fuer MA-Daten
class Employee(object):
    
    # Konstruktor
    def __init__(self, eID, eFName, eLName, eHours, eMinConsecutive, eMaxConsecutive, eMinExtra, eMaxExtra, eOff, eVacation, eHistory, eWeekendConstraints):
        self.eID = eID
        self.fName = eFName
        self.lName = eLName
        self.hours = eHours
        self.minConsecutive = eMinConsecutive
        self.maxConsecutive = eMaxConsecutive
        self.minExtra = eMinExtra
        self.eMaxExtra = eMaxExtra
        self.off = eOff
        self.vacation = eVacation
        self.history = eHistory
        self.weekendContraints = eWeekendConstraints
