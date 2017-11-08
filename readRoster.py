import json
from roster import Roster           # eigene Rosterklasse
from employee import Employee       # eigene Employeeklasse



# Funktion zur Erstellung eines leeren Rosterdictionary
def createEmptyRoster():
    # Constraints-Datei oeffnen
    with open('roster-simulation_01_1705.json') as constraints:
        # in dictionary schreiben
        data = json.load(constraints)
    
    # Informationen ueber Schichten    
    shifts = data["shiftTypes"]
    
    # Variable zum Erfassen der Schichtarten pro Tag
    dailyShifts = [];
    for s in shifts:
        dailyShifts.append(s["name"])
    
    # Erster Tag des Dienstplanes
    startDate = data["firstDay"]
    i = 1
    # Anzahl Tage, die der Dienstplan umfasst    
    upperBound = data["numberOfDays"]
    # Variable zum Erfassen der Schichtarten pro Monat
    allShifts = []
    
    # Fuer jeden Tag eine Frueh- und Spaetschicht in Liste eintragen
    while i <= upperBound:
        for ds in dailyShifts:
            for s2 in shifts:
                if(s2["name"] == ds):
                    j = 1
                    liste = s2["requirements"]
                    while j <= liste[i-1]:
                        allShifts.append(startDate[:len(startDate)-len(str(i))] + str(i) + "-" + ds + "-" + str(j))
                        j = j + 1     
        i = i + 1
    
    # leeres Dictionary mit allen zu belegenden Schichten als Keys zurueckgeben
    return(dict.fromkeys(allShifts))



# Funktion zum befuellen des leeren Dienstplanes aus den JSON-Dateien
def fillRoster(ros):
    # Schichtplan 1 oeffnen
    with open('roster-simulation_01_170506_00-10.json') as json_data:
        # in dictionary schreiben
        d = json.load(json_data)
    
    rDD = {"Donald Duck":d["Donald Duck"]}                  # Schichtplan fuer Donald Duck
    rMM = {"Minnie Mouse":d["Minnie Mouse"]}                # Schichtplan fuer Minnie Mouse
    rWP = {"Winnieh Pooh":d["Winnieh Pooh"]}                # Schichtplan fuer Winnieh Pooh
    rBB = {"Bibi Blocksberg":d["Bibi Blocksberg"]}          # Schichtplan fuer Bibi Blocksberg
    rBBl = {"Benjamin Bluemchen":d["Benjamin Bluemchen"]}   # Schichtplan fuer Benjamin Bluemchen 
    rJJ = {"Justus Jonas":d["Justus Jonas"]}                # Schichtplan fuer Justus Jonas
    rPS = {"Peter Shaw":d["Peter Shaw"]}                    # Schichtplan fuer Peter Shaw
    rBA = {"Bob Andrews":d["Bob Andrews"]}                  # Schichtplan fuer Bob Andrews
    rKK = {"Karla Kolumna":d["Karla Kolumna"]}              # Schichtplan fuer Karla Kolumna
        
    # Alle Einzelschichtplaene in eine Liste schreiben
    rAll = [rDD, rMM, rWP, rBB, rBBl, rJJ, rPS, rBA, rKK];
    
    # Loop ueber die Individualroster und einfuegen in das Dict
    for r in rAll:
        empl = next(iter(r))
        for rVal in r.values():
            for x in rVal:
                if(rVal.get(x) == "Frueh"):
                    if(ros[x + "-" + rVal.get(x) + "-1"] == None):
                        ros[x + "-" + rVal.get(x) + "-1"] = empl
                    else:
                        ros[x + "-" + rVal.get(x) + "-2"] = empl
                elif(rVal.get(x) == "Spaet"):
                    if(ros[x + "-" + rVal.get(x) + "-1"] == None):
                        ros[x + "-" + rVal.get(x) + "-1"] = empl
                    else:
                        ros[x + "-" + rVal.get(x) + "-2"] = empl
    
    return(ros)



# Funktion zum lesen der Daten aus der JSON-Constraints Datei
def getRosterData():
    # Constraints-Datei oeffnen
    with open('roster-simulation_01_1705.json') as constraints:
        # in dictionary schreiben
        data = json.load(constraints)
        
    planID = data["id"]                                     # ID des Plans
    cntDays = data["numberOfDays"]                          # Anzahl der Tage des Plans
    cntWeeks = data["numberOfWeeks"]                        # Anzahl Wochen
    firstDay = data["firstDay"]                             # Erster Tag des Plans
    maxSundays = data["maxSundays"]                         # Maximale Anzahl Sonntage
    maxOvertime = data["maximumOvertime"]                   # Maximale Ueberstunden
    maxUndertime = data["maximumUndertime"]                 # Maximale Unterstunden
    forbiddenShifts = data["forbiddenShiftTypeSuccessions"] # Verbotene Schichtfolgen
    standardContr = data["standardContract"]                # Standard Arbeitsvertrag
    shiftReq = data["shiftRequestJSONs"]                    # Schicht Anfragen von Mitarbeitern
    fixedShifts = data["fixedAssignmentJSONs"]              # Fest zugewiesene Schichten

    # Rueckgabe der Informationen als Array zur einfaches Weiterverarbeitung
    return([planID, cntDays, cntWeeks, firstDay, maxSundays, maxOvertime, maxUndertime, forbiddenShifts, standardContr, shiftReq, fixedShifts])
    


# Funktion zum Lesen der Daten ueber Mitarbeiter
def getEmployees():
    # Constraints-Datei oeffnen
    with open('roster-simulation_01_1705.json') as constraints:
        # in dictionary schreiben
        data = json.load(constraints)
        
    employees = data["employees"]       # Array aus Dicionarys in employees speichern
    
    employeeList = []                   # Liste zum iterativen Hinzufuegen von Employee Objekten
    
    for e in employees:                 # Loop ueber alle Angestellten um Employee Objekte zu erstellen
        eID = e["ID"]                               # Mitarbeiter ID
        eFName = e["firstName"]                     # Vorname
        eLName = e["lastName"]                      # Nachname
        eHours = e["regularWorkingHoursPerWeek"]    # Arbeitsstunden pro Woche
        eMinConsecutive = e["minimumNumberOfConsecutiveWorkingDaysIndividual"]   # Minimale Anzahl aufeinanderfolgender Arbeitstage
        eMaxConsecutive = e["maximumNumberOfConsecutiveWorkingDaysIndividual"]  # Maximale Anzahl aufeinanderfolgender Arbeitstage
        eMinExtra = e["lowerBoundExtraHours"]       # Minimale Anzahl Ueberstunden
        eMaxExtra = e["upperBoundExtraHours"]       # Maximale Anzahl Ueberstunden
        eOff = e["offDays"]                         # Arbeitsfreie Tage (kann an diesen Tagen als Ersatz verwendet werden)
        eVacation = e["vacationDays"]               # Urlaubstage (kann an diesen Tagen nicht als Ersatz verwendet werden)
        eHistory = e["individualHistory"]           # Dictionary mit individuellen Daten ueber MA
        eWeekendConstraints = e["weekendConstraints"]   # Array mit Informationen ueber Wochenende
        
        # Employee Objekt erstellen
        currentEmployee = Employee(eID, eFName, eLName, eHours, eMinConsecutive, eMaxConsecutive, eMinExtra, eMaxExtra, eOff, eVacation, eHistory, eWeekendConstraints)
        
        employeeList.append(currentEmployee)    # Mitarbeiter der Liste hinzufuegen
        
    return(employeeList)



roster = createEmptyRoster()                        # Leeren Dienstplan erstellen
newRoster = fillRoster(roster)                      # Leeren Dienstplan fuellen

basicInfos = getRosterData()                        # Basis Constraints einlesen

empList = getEmployees()                            # MA-Daten einlesen

R1 = Roster(newRoster, basicInfos, empList)         # Datenstruktur Roster mit Daten erzeugen


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




