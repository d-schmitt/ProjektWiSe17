from Test.readRoster import *
from Test.roster import Roster
from Test.constraints import *
from Test.reschedulingHelpers import *
import collections
from time import *
from Test.event import shiftBegin, shiftEnd, vacationBegin, vacationEnd,\
    illnessBegin, illnessEnd
from datetime import datetime, timedelta, date
import copy
import random

# Initiale Definitionen zum Testen
roster = createEmptyRoster()                        # Leeren Dienstplan erstellen
newRoster = fillRoster(roster)                      # Leeren Dienstplan fuellen
basicInfos = getRosterData()                        # Basis Constraints einlesen
empList = getEmployees()                            # MA-Daten einlesen
R1 = Roster(newRoster, basicInfos, empList)         # Datenstruktur Roster mit Daten erzeugen

# Input
currentTime = datetime.strptime(R1.start, '%Y-%m-%d')
illnessPeriod = 5
illemID = 52
#####################################################################

# Constraint Testing



#####################################################################
# Testing
RTest=copy.deepcopy(R1)
print(getEmployeeName(getEmployeeById(R1,illemID)))

# Determine Start and End Date of IllnessPeriod
start_date = date(currentTime.year, currentTime.month, currentTime.day)
illnessEndDate = currentTime +timedelta(days=illnessPeriod)
end_date = date(illnessEndDate.year, illnessEndDate.month, illnessEndDate.day)

IllnessShift = [] # sammelt Tag und Schicht, für welche Ersatz gefunden werden muss

# Finde heraus, welche Schichten von Mitarbeiterausfall betroffen sind
for single_date in daterange(start_date, end_date): # Für jeden Tag
    sdDay = single_date.strftime("%Y-%m-%d")

    for j in R1.shiftTypes: # Für jede Schicht
        if(getShiftByEmployeeByDateByShift(R1,sdDay,getEmployeeById(R1,illemID),j['name'])==1): # Wenn Mitarbeiter dort arbeitet
            print("Ersatz notwendig")
            IllnessShift.append([sdDay,j['name']])
            # hier könnte man nun direkt krank melden

print(IllnessShift)
# (Wiederhole für jede ausgefallene Schicht:)

#Mitarbeiter Krank melden für alle seine Schichten --> könnte man in schichtausfall integrieren
for i in range(0,len(IllnessShift)):
    changeEmployeeShift(R1, IllnessShift[i][0], getEmployeeName(getEmployeeById(R1,illemID)), 'sickDay')

# Erzeuge eine Liste an Nurses, welche die ausgefallene Schicht ersetzen kann
nurses = []

if(len(IllnessShift)>0): # Wenn es Schichten gibt, welche ausfallen
    # für jede Schicht, wofür ein Ersatz gefunden werden muss
    for i in range(0,len(IllnessShift)):
        print(IllnessShift[i][0])
        #überprüfe für jede Nurse
        for j in R1.employees:

            #Wenn Nurse an dem Tag noch nicht arbeitet:
            if(getShiftByEmployeeByDate01(R1,IllnessShift[i][0],j)==0 and getEmployeeName(j) != "Leih Nurse"
               and getEmployeeName(j) != getEmployeeName(getEmployeeById(R1,illemID))):

                #Erzeuge Kopie des bisherigen Rosters
                # Rostercopy = self
                R1copy=copy.deepcopy(R1)

                #setze Nurse in ausgefallene Schicht der Rosterkopie ein
                changeEmployeeShift(R1copy,IllnessShift[i][0],getEmployeeName(j), IllnessShift[i][1])

                #Wenn Rosterkopie-Schichtplan gültige Lösung liefert, füge zu Nurseliste hinzu
                if(checkShiftAssignments(R1copy)==True and checkVacationDaysOff(R1copy) == True
                   and checkOffDaysOff(R1copy)):
                    nurses.append([IllnessShift[i], getEmployeeName(j)])

print(nurses)

IllnessShiftErsatz = [] # Liste mit Ersatz für kranke Schichten
shiftCount = 0
# für jede ermittelte krankheitsschicht:
for i in IllnessShift:
    ersatz = 0 # bleibt 0, falls kein Ersatz gefunden wird für Schicht i

    # Wenn nurses für schicht zur verfügung stehen:
    if(getNoErsatzNurses(i,nurses)>0):
        ErsatzNurses = getErsatzNurseNames(i,nurses)
        # für jede zum Ersatz stehende Nurse
        for j in ErsatzNurses:
            # Berechne Wahrscheinlichkeit für annehmen
            a = random.random()
            print("Wahrscheinlichkeit für Annahme der Schicht", a)
            print("Mitarbeiter", j)
            if(a > 0.5):
                # Assign nurse
                changeEmployeeShift(R1, IllnessShift[shiftCount][0], j, IllnessShift[shiftCount][1])
                IllnessShiftErsatz.append([IllnessShift[shiftCount], j])
                ersatz = 1
                break

            # Advanced Lösung: Nehme die Nurse, wo Durchschnitt aus Satisfaction Score + Überstunden minimiert wird (über alle)

    if(getNoErsatzNurses(i,nurses)==0 or ersatz == 0):
        # Einfache Lösung: Zeitarbeitsnurse anstellen
        changeEmployeeShift(R1,IllnessShift[shiftCount][0],'Leih Nurse',IllnessShift[shiftCount][1])
        IllnessShiftErsatz.append([IllnessShift[shiftCount], 'Leih Nurse'])
        print('Leih Nurse eingetragen für',IllnessShift[shiftCount][0])
        # Was wenn zwei Mitarbeiter in selber Schicht krank sind? --> zwei Leih Nurses

        # Advanced Lösung: Restriktion ggf. aufweichen (WE z.B.)
    shiftCount += 1

print(IllnessShiftErsatz)
print(checkMinMaxConsec(R1))
print(1)