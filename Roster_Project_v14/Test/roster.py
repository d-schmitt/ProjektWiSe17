from datetime import datetime, timedelta, date
import itertools
import collections
from random import randint
from random import gauss

### Rescheduling Imports
from Test.constraints import *
from Test.reschedulingHelpers import *
import copy
import random

# Rosterklasse als Uebergabeobjekt zwischen Rescheduling und Simulation
class Roster(object):
    
    # Konstruktor
    def __init__(self, s, infos, empList):
        self.shifts = s                 # Umformatierter Schichtplan
        self.planID = infos[0]          # Plan ID
        self.cntDays = infos[1]         # Anzahl Tage
        self.cntWeeks = infos[2]        # Anzahl Wochen
        self.start = infos[3]           # Startdatum des Plans
        self.maxSun = infos[4]          # Maximale Anzahl Sonntage
        self.maxOver = infos[5]         # Maximale Anzahl Ueberstunden
        self.maxUnder = infos[6]        # Maximale Anzahl Unterstudnen
        self.forbidden = infos[7]       # Verbotene Schichtfolgen
        self.contracts = infos[8]       # Standard Arbeitsvertrag
        self.requests = infos[9]        # Anfragen von Mitarbeitern nach Schichten
        self.fixed = infos[10]          # Fest zugewiesene Schichten
        self.shiftTypes = infos[11]     # Schichtarten
        self.employees = empList        # Liste aller Mitarbeiter  
        self.vacationBegin = self.createVacationBegin() # Liste der ersten Urlaubstage des Monats
        self.vacationEnd = self.createVacationEnd()     # Liste der Urlaubsenden
        self.avgIllnessDaysPerMonth = 9                # Gesamtkrankheitstage aller Mitarbeiter
        self.avgTimeBeforeSick = 8                      # 8 halbe Stunden vorher wird durchschnittlich Bescheid gesagt       
    
        
    # Funktion gibt den Mitarbeiter mit einer bestimmten ID zurueck
    def getEmployeeById(self, empID):
        for e in self.employees:
            if e.eID == empID:
                return(e)
        print("Es existiert kein Mitarbeiter mit der ID " + str(empID))
        
        
    # Funktion gibt den Mitarbeiter mit einer bestimmten ID zurueck
    def changeEmployeeState(self, empName, empState):
        for e in self.employees:
            if e.fName + " " + e.lName == empName:
                if empState == "sick":
                    e.illnessDaysThisMonth = e.illnessDaysThisMonth + 1
                e.state = empState
            
           
    # Funktion zur Ausgabe der aktuellen Stati aller MA
    def printStates(self, log_file, alertMA):
        for e in self.employees:
            if e.eID == alertMA:
                log_file.write(e.fName + " " + e.lName + ": " + e.state + " --- Achtung: Dieser MA ist krank und soll diese Schicht arbeiten\n")
            else:
                log_file.write(e.fName + " " + e.lName + ": " + e.state + "\n")
        
        
    # Gibt die Uhrzeit der naechsten beginnenden schicht zurueck
    def getNextStartTime(self, currentHour):
        # Loop ueber die Schichtarten - Wichtig: Muessen sortiert sein
        for i in range(0,len(self.shiftTypes)):
            if int(self.shiftTypes[i]["startTime"][0:2]) > currentHour:
                return(self.shiftTypes[i]["startTime"], self.shiftTypes[i]["name"], 0)
        # Rueckgabewerte: Startzeit, Name der Schicht, naechster Tag (bool)    
        return([self.shiftTypes[0]["startTime"], self.shiftTypes[0]["name"], 1])
    
    
    # Gibt die Endzeit einer Schichtart mit bestimmter Anfangszeit zurueck
    def getEndByStart(self, type):
        # Loop ueber die Schichtarten - Wichtig: Muessen sortiert sein
        for i in range(0,len(self.shiftTypes)):
            if self.shiftTypes[i]["name"] == type:
                return(self.shiftTypes[i]["endTime"])
            
            
    # Gibt zu einem bestimmten Tag und einer bestimmten Schichtart die dazu arbeitenden Mitarbeiter zurueck
    def getWorkingEmployees(self, day, sType):
        workingList = []                    # wird bei der Iteration gefuellt
        for e in self.employees:
            if e.eID != 0:                  # Zeitarbeitsnurse nicht beruecksichtigen
                if e.shifts[str(day)[:10]] == sType:
                    workingList.append(e)
        return(workingList)
        
    
    # Gibt eine Liste aller Tage der Periode zurueck
    def getDays(self):
        dayList = []
        for i in range(1, self.cntDays+1):
            currentDay = datetime.strptime(self.start, '%Y-%m-%d') + timedelta(days=i-1)
            dayList.append(currentDay)
        return(dayList)
    
    # Gibt zurueck, welche Schicht ein MA an einem bestimmten Tag arbeitet
    def getShiftByEmployeeByDay(self, day, employee):
        for e in self.employees:
            if e.fName + " " + e.lName == employee:
                if(e.shifts[str(day)[:10]] == "Frueh" or e.shifts[str(day)[:10]] == "Spaet"):
                    return(e.shifts[str(day)[:10]])
                else:
                    return(0)  
    
    # Gibt zurueck, ob ein MA an einem tag arbeitet
    def getShiftByEmployeeByDay01(self, day, employee):
        for e in self.employees:
            if e.fName + " " + e.lName == employee:
                if(e.shifts[str(day)[:10]] == "Frueh" or e.shifts[str(day)[:10]] == "Spaet"):
                    return(1)
                else:
                    return(0)
    
    
    # Gibt die Anzahl der Wochen der Periode zurueck
    def getCountWeeks(self):
        return self.cntWeeks
        
    
    # Gibt eine Liste der Dati der Sonntage in der Periode zurueck
    def getSundays(self):
        sundayList = []
        for i in range(1, self.cntDays+1):
            currentDay = datetime.strptime(self.start, '%Y-%m-%d') + timedelta(days=i-1)
            if currentDay.weekday() == 6:
                sundayList.append(currentDay)
        return(sundayList) 
           
            
    # Liste der Tage an denen ein bestimmter Mitarbeiter keinen Off- oder Vacation-Day hat
    def getOnOffDays(self, employee):
        onList = []
        offList = []
        emplObject = ""
        # passenden MA aus der emplyeeListe heraussuchen
        for e in self.employees:
            if e.fName + " " + e.lName == employee:
                emplObject = e
                break
        if emplObject != "":
            # Tage, die nicht Off oder Vacation sind aus dem Schichtplan des MA heraussuchen
            for key, value in emplObject.shifts.items():
                if value != "offDay" and value != "vacationDay":
                    onList.append(datetime.strptime(key, '%Y-%m-%d'))
                else:
                    offList.append(datetime.strptime(key, '%Y-%m-%d'))
            return(onList, offList)       # Rueckgabewert eine Liste, in der auf 0 die onList und 1 die offList liegt
        else:
            return("Zu dem Mitarbeiter " + employee  + " liegen keine Daten vor.")
        
        print(employee)
        
        
    # Erstellt ein Dictionary mit Datumswerten als Key und den MAs, die an diesem Tag Urlaubsbeginn haben als value
    def createVacationBegin(self):
        vacBeginList = []
        for e in self.employees:
            for key, value in e.shifts.items():
                if value == "offDay" or value == "vacationDay":
                    if(datetime.strptime(key, '%Y-%m-%d').day != 1):
                        previous = e.shifts.get(str(datetime.strptime(key, '%Y-%m-%d') - timedelta(days=1))[0:10])
                        if previous != "offDay" and previous != "vacationDay":
                            vacBeginList.append(((datetime.strptime(key, '%Y-%m-%d')), e.fName + " " + e.lName))
                    else:
                        vacBeginList.append(((datetime.strptime(key, '%Y-%m-%d')), e.fName + " " + e.lName))         
        vacBeginDictUnordered = {}
        for row in vacBeginList:
            vacBeginDictUnordered.setdefault(row[0],[]).append(row[1])
        vacBeginDictOrdered = collections.OrderedDict(sorted(vacBeginDictUnordered.items()))
        return(vacBeginDictOrdered)
    
    
    # Erstellt ein Dictionary mit Datumswerten als Key und den MAs, die an diesem Tag Urlaubsende haben als value
    def createVacationEnd(self):
        vacEndList = []
        for e in self.employees:
            for key, value in e.shifts.items():
                if value != "offDay" and value != "vacationDay":
                    if(datetime.strptime(key, '%Y-%m-%d').day != 1):
                        previous = e.shifts.get(str(datetime.strptime(key, '%Y-%m-%d') - timedelta(days=1))[0:10])
                        if previous == "offDay" or previous == "vacationDay":
                            vacEndList.append(((datetime.strptime(key, '%Y-%m-%d')), e.fName + " " + e.lName))         
        vacEndDictUnordered = {}
        for row in vacEndList:
            vacEndDictUnordered.setdefault(row[0],[]).append(row[1])
        vacEndDictOrdered = collections.OrderedDict(sorted(vacEndDictUnordered.items()))
        return(vacEndDictOrdered)
    
    
    # Gibt aufgrund der Wahrscheinlichkeit, mit der einzelne MAs krank werden den naechsten kranken MA zurueck
    def determineIllness(self):                
        iDays = 0               # Summiert die Differenzen zum Durchschnitt auf, um eine Zufallsauswahl treffen zu koennen 
        iDistribution = {}      # Dict zur Speicherung von MAs und Krankheitswahrscheinlichkeitsverteilung
        retID = 0               # Variable zur Speicherung  der ID des ausgwaehlten MAs
        for e in self.employees:                    # Wahrscheinlichkeitsverteilung erstellen
            if e.eID != 0:                      # Ohne Zeitarbeitsnurse
                iDays = iDays + (e.avgIllnessDaysPerMonth-e.illnessDaysThisMonth)
                iDistribution.update({e.eID:iDays})    
        for key, value in iDistribution.items():    # Per Zufallszahl aus der Wahrscheinlichkeistverteilung waehlen
            if value >= randint(0, iDays):
                retID = key
                break
        return(self.getEmployeeById(retID))         # MA Objekt zurueckgeben
    
    # terminiert den naechsten Krankheitsbedingten Ausfall
    # TODO: Vereinfachte Version geht von exakt definierter Anzahl an krankheiten aus und terminiert genau gleichmaessig
    def determineIllnessTime(self, currentTime):
        # uniFormDelta erzeugt gleichmaessige Zeitschritte
        uniformDelta = timedelta(minutes=int((self.cntDays*48)/self.avgIllnessDaysPerMonth)*30)
        # Abweichung von 24 halben Stunden = 1 Tagen moeglich
        standardDev = int(gauss(0, 48))
        addTime = timedelta(minutes=standardDev*30)      
        nTime = currentTime + uniformDelta + addTime
        lastTime = datetime.strptime(self.start, '%Y-%m-%d')+timedelta(days=self.cntDays)
        if nTime < lastTime:        # Damit SImulation am letzten Tag endet
            return(nTime)
           
           
           
           
    #----------------------------------------------------------------------------------------------------------------
    # Re-Scheduling
    #----------------------------------------------------------------------------------------------------------------
    # currentTime: datetime, empID: integer, duration: integer (kann bei Bedarf auch als timedelte uebergeben werden)
    def reSchedule(self, currentTime, empID, duration):
        """
        print(currentTime)
        print(empID)
        print(duration)
        """

        # Input
        #currentTime = datetime.strptime(self.start, '%Y-%m-%d')
        illnessPeriod = duration# illnessPeriod = 5
        illemID = empID # 52
        #####################################################################

        # Constraint Testing



        #####################################################################
        # Testing
        RTest = copy.deepcopy(self)
        print(getEmployeeName(getEmployeeById(self, illemID)))
        #####################################################################
        # Determine Start and End Date of IllnessPeriod
        start_date = date(currentTime.year, currentTime.month, currentTime.day)
        illnessEndDate = currentTime + timedelta(days=illnessPeriod)
        end_date = date(illnessEndDate.year, illnessEndDate.month, illnessEndDate.day)

        # Liegt Ende der Krankheit in Periode?
        end_date_full_period = datetime.strptime(self.start,"%Y-%m-%d")+ timedelta(days=self.cntDays)
        # wenn Krankheit über Dienstplanungsperiode hinausgeht
        if(end_date >= end_date_full_period.date()):
            end_date = end_date_full_period.date()

        IllnessShift = []  # sammelt Tag und Schicht, für welche Ersatz gefunden werden muss

        # Finde heraus, welche Schichten von Mitarbeiterausfall betroffen sind
        for single_date in daterange(start_date, end_date):  # Für jeden Tag
            sdDay = single_date.strftime("%Y-%m-%d")
            print(sdDay)
            for j in self.shiftTypes:  # Für jede Schicht
                if (getShiftByEmployeeByDateByShift(self, sdDay, getEmployeeById(self, illemID),
                                                    j['name']) == 1):  # Wenn Mitarbeiter dort arbeitet
                    print("Ersatz notwendig")
                    IllnessShift.append([sdDay, j['name']])
                    # hier könnte man nun direkt krank melden

        if(len(IllnessShift)==0):
            print("Keine Schichten sind von Mitarbeiterausfall betroffen.")
        else:
            print(IllnessShift)
        # (Wiederhole für jede ausgefallene Schicht:)

        # Mitarbeiter Krank melden für alle seine Schichten --> könnte man in schichtausfall integrieren
        for i in range(0, len(IllnessShift)):
            changeEmployeeShift(self, IllnessShift[i][0], getEmployeeName(getEmployeeById(self, illemID)), 'sickDay')

        # Erzeuge eine Liste an Nurses, welche die ausgefallene Schicht ersetzen kann
        nurses = []

        if (len(IllnessShift) > 0):  # Wenn es Schichten gibt, welche ausfallen
            # für jede Schicht, wofür ein Ersatz gefunden werden muss
            for i in range(0, len(IllnessShift)):
                print(IllnessShift[i][0])
                # überprüfe für jede Nurse
                for j in self.employees:

                    # Wenn Nurse an dem Tag noch nicht arbeitet:
                    if (getShiftByEmployeeByDate01(self, IllnessShift[i][0], j) == 0 and getEmployeeName(
                            j) != "Leih Nurse"
                        and getEmployeeName(j) != getEmployeeName(getEmployeeById(self, illemID))):

                        # Erzeuge Kopie des bisherigen Rosters
                        # Rostercopy = self
                        selfcopy = copy.deepcopy(self)

                        # setze Nurse in ausgefallene Schicht der Rosterkopie ein
                        changeEmployeeShift(selfcopy, IllnessShift[i][0], getEmployeeName(j), IllnessShift[i][1])

                        # Wenn Rosterkopie-Schichtplan gültige Lösung liefert, füge zu Nurseliste hinzu
                        if (checkShiftAssignments(selfcopy) == True and checkVacationDaysOff(selfcopy) == True
                            and checkOffDaysOff(selfcopy)):
                            nurses.append([IllnessShift[i], getEmployeeName(j)])

        print(nurses)

        IllnessShiftErsatz = []  # Liste mit Ersatz für kranke Schichten
        shiftCount = 0
        # für jede ermittelte krankheitsschicht:
        for i in IllnessShift:
            ersatz = 0  # bleibt 0, falls kein Ersatz gefunden wird für Schicht i

            # Wenn nurses für schicht zur verfügung stehen:
            if (getNoErsatzNurses(i, nurses) > 0):
                ErsatzNurses = getErsatzNurseNames(i, nurses)
                # für jede zum Ersatz stehende Nurse
                for j in ErsatzNurses:
                    # Berechne Wahrscheinlichkeit für annehmen
                    a = random.random()
                    print("Wahrscheinlichkeit", a, " für Annahme der Schicht von ", j)
                    if (a > 0.5):
                        # Assign nurse
                        changeEmployeeShift(self, IllnessShift[shiftCount][0], j, IllnessShift[shiftCount][1])
                        IllnessShiftErsatz.append([IllnessShift[shiftCount], j])
                        ersatz = 1
                        break

                        # Advanced Lösung: Nehme die Nurse, wo Durchschnitt aus Satisfaction Score + Überstunden minimiert wird (über alle)

            if (getNoErsatzNurses(i, nurses) == 0 or ersatz == 0):
                # Einfache Lösung: Zeitarbeitsnurse anstellen
                changeEmployeeShift(self, IllnessShift[shiftCount][0], 'Leih Nurse', IllnessShift[shiftCount][1])
                IllnessShiftErsatz.append([IllnessShift[shiftCount], 'Leih Nurse'])
                print('Leih Nurse eingetragen für', IllnessShift[shiftCount][0])
                # Was wenn zwei Mitarbeiter in selber Schicht krank sind? --> zwei Leih Nurses

                # Advanced Lösung: Restriktion ggf. aufweichen (WE z.B.)
            shiftCount += 1

        print("Gefundener Ersatz:",IllnessShiftErsatz)
        #print(checkMinMaxConsec(self))
        
            
            
        
                    
            
            
            
            
           
        