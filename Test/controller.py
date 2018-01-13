from Test.readRoster import *
from Test.sim import *
from Test.roster import Roster
from time import *
import time

log_file = open("Simulation_log.txt", "w")          # Log-Datei erstellen

tStart = clock()                                    # Zeitvariable zur Laufzeitmessung

log_file.write("####################################################################################\n")
log_file.write("Simulation starten\n")
log_file.write("####################################################################################\n")
                                    
roster = createEmptyRoster()                        # Leeren Dienstplan erstellen
newRoster = fillRoster(roster)                      # Leeren Dienstplan fuellen
basicInfos = getRosterData()                        # Basis Constraints einlesen
empList = getEmployees()                            # MA-Daten einlesen
R1 = Roster(newRoster, basicInfos, empList)         # Datenstruktur Roster mit Daten erzeugen

simulate(R1, log_file)                                        # Aufruf der Simulationsfunktion


tEnd = clock()                                      # Zeitvariable zur Laufzeitmessung

log_file.write("####################################################################################\n")
log_file.write("Laufzeit der Simulation: "  + str(tEnd-tStart) + " sec \n")
log_file.write("####################################################################################\n")
log_file.close()


"""
print("Plan-ID: " + R1.planID)
print("Anzahl Tage: " + str(R1.cntDays))
print("Anzahl Wochen: " + str(R1.cntWeeks))
print("Anzahl Mitarbeiter: " + str(len(R1.employees)))
print("Startdatum: " + R1.start)
print("Maximale Anzahl Sonntage: " + str(R1.maxSun))
print("Maximale Anzahl Ueberstunden: " + str(R1.maxOver))
print("Maximale Anzahl Unterstunden: " + str(R1.maxUnder))
print("Verbotene Schichtfolgen: " + str(R1.forbidden))
print("Standard Arbeitsvertrag: " + str(R1.contracts))
print("Schichten: " + str(R1.shifts))
print("Schichtanfragen: " + str(R1.requests))
print("Fest zugewiesene Schichten: " + str(R1.fixed))
print("Schichtarten: " + str(R1.shiftTypes))
"""      
