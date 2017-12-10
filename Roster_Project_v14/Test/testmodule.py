from roster import Roster
from readRoster import *
from time import *
from datetime import datetime, timedelta

tStart = clock()                                    # Zeitvariable zur Laufzeitmessung

roster = createEmptyRoster()                        # Leeren Dienstplan erstellen
newRoster = fillRoster(roster)                      # Leeren Dienstplan fuellen
basicInfos = getRosterData()                        # Basis Constraints einlesen
empList = getEmployees()                            # MA-Daten einlesen
R1 = Roster(newRoster, basicInfos, empList)         # Datenstruktur Roster mit Daten erzeugen

#print(R1.getDays())

print(R1.getShiftByEmployeeByDay(datetime(2017, 5, 4, 0, 0), "Justus Jonas"))

for e in R1.employees:
   print(e.fName + ": " + str(e.shifts))

#print(R1.getSundays())

#onList, offList = R1.getOnOffDays("Donald Duck")        # nur ein Funktionsaufruf fuer on- und offList
#print(onList)
#print(offList)

#print(R1.createVacationBegin())

#print(R1.createVacationEnd())

tEnd = clock()                                      # Zeitvariable zur Laufzeitmessung

print("Laufzeit der Simulation: "  + str(tEnd-tStart) + " sec")