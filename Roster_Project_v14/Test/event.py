from datetime import datetime, timedelta
from random import randint
#--------------------------------------------------------------------------------------------------------------------------------
# Erklaerung zu den verschiedenen Stati
# working: der MA ist gerade im Dienst
# none: der MA hat frei und steht - wenn keine Restriktionen dadurch verletzt werden - fuer das Rescheduling bereit
# vacation: der MA hat Urlaub, damit steht er nicht fuer das Rescheduling bereit
# sick: der MA ist krank und steht nicht fuer das Rescheduling bereit, waehrend er den Status sick hat, kann er die vorher
#         festgelegten Schichten nicht antreten und es muss ein Rescheduling stattfinden.
#--------------------------------------------------------------------------------------------------------------------------------

# Ereignisklasse fuer die Simulation
class Event(object):
    # Konstruktor
    def __init__(self, eDate):
        self.date = eDate               # Datum, wann das Ereignis terminiert ist

#---------------------------------------------------------------------------------------------------------------------------------
# Abschnitt: Schichtbeginn & -Ende
#---------------------------------------------------------------------------------------------------------------------------------
# Spezialereignis Schichtbeginn
class shiftBegin(Event):
    # Konstruktor
    def __init__(self, r, currentTime):
        eTime = self.terminateEvent(r, currentTime)[0]
        self.type = self.terminateEvent(r, currentTime)[1]
        Event.__init__(self, eTime)                         # Attribut an Superklasse weiterreichen
        self.sType = self.setShiftType(eTime, r)            # Schichtart bestimmen
    
    # Funktion zur Bestimmung der Schichtart    
    def setShiftType(self, dt, r):
        for st in r.shiftTypes:
            if datetime.strptime(st["startTime"], '%H:%M').hour == dt.hour:
                return st["name"]
    
    # Funktion zur Terminierung des naechsten Schichtbeginns    
    def terminateEvent(self, r, currentTime):
        nextShift = r.getNextStartTime(currentTime.hour)
        nextShiftTime = nextShift[0]                        # Startzeit der naechsten Schicht
        currentDay0 = currentTime - timedelta(hours=currentTime.hour, minutes=currentTime.minute)   # Zeit auf 0 Uhr setzen
        nextShiftDateTime = currentDay0 + timedelta(days=nextShift[2], hours=int(nextShiftTime[0:2]), minutes=int(nextShiftTime[3:5]))  # Startzeit addieren
        return(nextShiftDateTime, nextShift[1])
    
    # Aenderung der Zustandsvariablen der einzelnen MItarbeiter, die durch den Schichtbeginn ausgeloest wird
    def changeState(self, r, log_file):
        #print("Zustandsaenderungen Schichtbeginn " + self.sType + ":")
        workingList = r.getWorkingEmployees(self.date, self.sType)      # Liste der Mitarbeiter
        alertMA = 999
        for e in workingList:
            if e.state != "sick":
                r.changeEmployeeState(e.fName + " " + e.lName, "working")
            else:
                alertMA = e.eID
        r.printStates(log_file, alertMA)
        return(r)
                        
        
    
# Spezialereignis: Schichtende
class shiftEnd(Event):
    # Konstruktor
    def __init__(self, sType, beginnTime, r):
        self.type = sType
        self.beginnTime = str(beginnTime)
        eTime = self.terminateEvent(r)
        Event.__init__(self, eTime)                 # Attribut an Superklasse weiterreichen
        self.sType = self.setShiftType(eTime, r)    # Schichtart bestimmen
        
    # Funktion zur Bestimmung der Schichtart    
    def setShiftType(self, dt, r):
        for st in r.shiftTypes:
            if datetime.strptime(st["endTime"], '%H:%M').hour == dt.hour:
                return st["name"]
        
    def terminateEvent(self, r):
        endTime = r.getEndByStart(self.type)
        beginTimeForm = datetime.strptime(self.beginnTime, '%Y-%m-%d %H:%M:%S')
        currentDay0 = beginTimeForm - timedelta(hours=int(beginTimeForm.hour), minutes=int(beginTimeForm.minute))   # Zeit auf 0 Uhr setzen
        nextEndDateTime = currentDay0 + timedelta(hours=int(endTime[0:2]), minutes=int(endTime[3:5]))  # Startzeit addieren
        return(nextEndDateTime)
        
    # Aenderung der Zustandsvariablen der einzelnen Mitarbeiter, die durch das Schichtende ausgeloest wird
    def changeState(self, r, log_file):
        alertMA = 999
        #print("Zustandsaenderungen Schichtende " + self.sType + ":")  
        beginTimeForm = datetime.strptime(self.beginnTime, '%Y-%m-%d %H:%M:%S')  
        workingList = r.getWorkingEmployees(beginTimeForm, self.sType)      # Liste der Mitarbeiter
        for e in workingList:
            if e.state != "sick":
                r.changeEmployeeState(e.fName + " " + e.lName, "none")
                for st in r.shiftTypes:
                    if st["name"] == self.sType:
                        e.hoursWorked = e.hoursWorked + st["workingHours"]
        r.printStates(log_file, alertMA)
        return(r)
    
    
#---------------------------------------------------------------------------------------------------------------------------------
# Abschnitt: Urlaubsbeginn & -Ende
#---------------------------------------------------------------------------------------------------------------------------------    
# Spezialereignis: Urlaubsbeginn
class vacationBegin(Event):
    # Konstruktor
    def __init__(self, r, currentTime):
        eTime, employees = self.terminateEvent(r, currentTime)
        Event.__init__(self, eTime)
        self.employees = employees
    
    # Zeitpunkt des Eregnisses terminieren    
    def terminateEvent(self, r, currentTime):
        for key, value in r.vacationBegin.items():
            if key >= currentTime:
                return(key + timedelta(minutes=30), value)
        return("none","none")
    
    # Aenderung der Zustandsvariablen der, die durch den Urlaubsbeginn ausgeloest werden
    def changeState(self, r, log_file):
        alertMA = 999
        for e in self.employees:
            r.changeEmployeeState(e, "vacation")
        r.printStates(log_file, alertMA)
        return(r)
    
    
# Spezialereignis: Urlaubsende
class vacationEnd(Event):
    # Konstruktor
    def __init__(self, r, currentTime):
        eTime, employees = self.terminateEvent(r, currentTime)
        Event.__init__(self, eTime)
        self.employees = employees
    
    # Zeitpunkt des Eregnisses terminieren    
    def terminateEvent(self, r, currentTime):
        for key, value in r.vacationEnd.items():
            if key >= currentTime:
                return(key + timedelta(hours=1), value)
        return("none","none")
    
    # Aenderung der Zustandsvariablen der, die durch den Urlaubsbeginn ausgeloest werden
    def changeState(self, r, log_file):
        alertMA = 999
        for e in self.employees:
            r.changeEmployeeState(e, "none")
        r.printStates(log_file, alertMA)
        return(r)
    
#---------------------------------------------------------------------------------------------------------------------------------
# Abschnitt: Krankheitsbeginn, Re-Scheduling & Krankheitsende
#---------------------------------------------------------------------------------------------------------------------------------
# Spezialereignis: Krankheitsbeginn
class illnessBegin(Event):
    # Konstruktor
    def __init__(self, r, currentTime):
        eTime, eEmployee = self.terminateEvent(r, currentTime)
        Event.__init__(self, eTime)
        self. employee = eEmployee
        self.duration = self.terminateDuration()
    
    # Dauer der Krankheit festlegen
    # TODO: besseren Algorithmus    
    def terminateDuration(self):
        iTime = timedelta(days=randint(1,5))
        return(iTime)
        
    # Zeitpunkt des Ereignisses terminieren
    def terminateEvent(self, r, currentTime):
        iEmployee = r.determineIllness()
        iTime = r.determineIllnessTime(currentTime)
        return(iTime, iEmployee)
    
    # Zustandaenderung durchfuehren    
    def changeState(self, r, log_file):
        alertMA = 999
        r.changeEmployeeState(self.employee.fName + " " + self.employee.lName, "sick")
        r.printStates(log_file, alertMA)
        return(r)
    

# Spezialereignis: Krankheitsende
class illnessEnd(Event):
    # Konstruktor
    def __init__(self, r, currentTime, employee, duration):
        eTime = self.terminateEvent(r, currentTime, duration)
        Event.__init__(self, eTime)
        self. employee = employee
        
    # Zeitpunkt des Ereignisses terminieren
    def terminateEvent(self, r, currentTime, duration):
        iTime = currentTime+duration
        return(iTime)
    
    # Zustandsaenderung durchfuehren    
    def changeState(self, r, log_file):
        alertMA = 999
        r.changeEmployeeState(self.employee.fName + " " + self.employee.lName, "none")
        r.printStates(log_file, alertMA)
        return(r)
    
    
    
    
    
    
    
         
        