from Test.roster import Roster
from Test.readRoster import *
from time import *
from datetime import datetime, timedelta

tStart = clock()                                    # Zeitvariable zur Laufzeitmessung

roster = createEmptyRoster()                        # Leeren Dienstplan erstellen
newRoster = fillRoster(roster)                      # Leeren Dienstplan fuellen
basicInfos = getRosterData()                        # Basis Constraints einlesen
empList = getEmployees()                            # MA-Daten einlesen
R1 = Roster(newRoster, basicInfos, empList)         # Datenstruktur Roster mit Daten erzeugen

for e in R1.employees:
    print(str(e))


#print(R1.getSickShifts(52, datetime(2017, 5, 3, 8, 0), datetime(2017, 5, 7, 23, 30)))
#print(R1.addSickHours(49, datetime(2017, 5, 4, 11, 0), datetime(2017, 5, 9, 11, 0)))

#print(R1.getShiftDefByName("Spaet"))

#print(R1.getDays())

#print(R1.getShiftByEmployeeByDay(datetime(2017, 5, 4, 0, 0), "Justus Jonas"))

#for e in R1.employees:
   #print(e.fName + ": " + str(e.shifts))

#print(R1.getSundays())

#onList, offList = R1.getOnOffDays("Donald Duck")        # nur ein Funktionsaufruf fuer on- und offList
#print(onList)
#print(offList)

#print(R1.createVacationBegin())

#print(R1.createVacationEnd())

tEnd = clock()                                      # Zeitvariable zur Laufzeitmessung

print("Laufzeit der Simulation: "  + str(tEnd-tStart) + " sec")