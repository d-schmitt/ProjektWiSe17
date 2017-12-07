import json
from employee import Employee       # eigene Employeeklasse
import copy

constraintsFile = 'roster-simulation_01_1705.json'
rosterFile = 'roster-simulation_01_170506_00-10.json'

# Funktion zur Erstellung eines leeren Rosterdictionary
def createEmptyRoster():
    # Constraints-Datei oeffnen
    with open(constraintsFile) as constraints:
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
    with open(rosterFile) as json_data:
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
    with open(constraintsFile) as constraints:
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
    shiftTypes = data["shiftTypes"]                         # Schichtearten als Liste

    # Rueckgabe der Informationen als Array zur einfaches Weiterverarbeitung
    return([planID, cntDays, cntWeeks, firstDay, maxSundays, maxOvertime, maxUndertime, forbiddenShifts, standardContr, shiftReq, fixedShifts, shiftTypes])
    


# Funktion zum Lesen der Daten ueber Mitarbeiter
def getEmployees():
    # Constraints-Datei oeffnen
    with open(constraintsFile) as constraints:
        # in dictionary schreiben
        data = json.load(constraints)
        
    with open(rosterFile) as empRoster:
        rosterData = json.load(empRoster)
        
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
        eShifts = rosterData[eFName + " " + eLName]     # Schichtplan des MAs
        
        # Employee Objekt erstellen
        currentEmployee = Employee(eID, eFName, eLName, eHours, eMinConsecutive, eMaxConsecutive, eMinExtra, eMaxExtra, eOff, eVacation, eHistory, eWeekendConstraints, eShifts)
        
        employeeList.append(currentEmployee)    # Mitarbeiter der Liste hinzufuegen
        
    # Zeitarbeitsnurse erstellen
    leihShifts = copy.deepcopy(eShifts)        # Schichtplan fuer Leiharbeiter erstellen
    for key in leihShifts.keys():       # Leeren Schichtplan erstellen
        leihShifts[key] = "None"
    
    leihNurse = Employee(0, "Leih", "Nurse", 99, 0, 99, 0, 999, [], [], {}, [], leihShifts)
    employeeList.append(leihNurse)    # Mitarbeiter der Liste hinzufuegen
        
    return(employeeList)

