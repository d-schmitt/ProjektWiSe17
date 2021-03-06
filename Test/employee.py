# Mitarbeiterklasse als Objekt fuer MA-Daten
class Employee(object):
    
    # Konstruktor
    def __init__(self, eID, eFName, eLName, eHours, eMinConsecutive, eMaxConsecutive, eMinExtra, eMaxExtra, eOff, eVacation, eHistory, eWeekendConstraints, eShifts, eOverUnderTime):
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
        self.illnessHoursThisMonth = 0              # Anzahl Krankheitsstunden
        self.extraHours = 0                         # Anzahl Stunden ueber Re-Scheduling eingeteilt
        self.hoursWorked = 0
        self.vacationHours = 0
        self.satisfactionScore = 0                  # Zufriedenheitswert
        self.overUnderTime = eOverUnderTime         # woechentliche Ueber-/ Unterstunden
        
    
    
    # Statusaenderung des MAs
    def setState(self, newState):
        self.state = newState
