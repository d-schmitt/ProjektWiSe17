# Mitarbeiterklasse als Objekt fuer MA-Daten
class Employee(object):
    
    # Konstruktor
    def __init__(self, eID, eFName, eLName, eHours, eMinConsecutive, eMaxConsecutive, eMinExtra, eMaxExtra, eOff, eVacation, eHistory, eWeekendConstraints, eShifts):
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
        self.state = "none"
        self.shifts = eShifts
        self.avgIllnessDaysPerMonth = 1             # Durchschnittlche Krankheitstage pro Monat
        self.illnessDaysThisMonth = 0               # Anzahl tatsaechlicher Krankheitstage
        self.hoursWorked = 0
        
    
    
    # Statusaenderung des MAs
    def setState(self, newState):
        self.state = newState
