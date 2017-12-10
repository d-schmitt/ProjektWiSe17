from datetime import datetime, timedelta

# Gibt zurueck, ob MA Schicht X am Tag Y arbeitet (0-1)
def getShiftByEmployeeByDateByShift(r, date, employee, shift):
    for e in r.employees:
        if e.eID == employee.eID and e.lName != "Nurse":
            if (e.shifts[str(date)[:10]] == shift):
                return (1)
            else:
                return (0)
        elif e.eID == employee.eID and e.lName == "Nurse":
            return(0)
    print("Mitarbeiter nicht gefunden")

# Gibt zurueck, ob ein MA an einem tag arbeitet
def getShiftByEmployeeByDate01(r, date, employee):
    for e in r.employees:
        if e.eID == employee.eID and e.lName != "Nurse":
            if (e.shifts[str(date)[:10]] == "Frueh" or e.shifts[str(date)[:10]] == "Spaet"):
                return (1)
            else:
                return (0)
        elif e.eID== employee.eID and e.lName=="Nurse":
            return(0)
    print("Mitarbeiter nicht gefunden")

# Funktion gibt den Mitarbeiter mit einer bestimmten ID zurueck
def getEmployeeById(r, empID):
    for e in r.employees:
        if e.eID == empID:
            return(e)
    print("Es existiert kein Mitarbeiter mit der ID " + str(empID))

# Funktion gibt den gesamten Namen des Mitarbeiters zurück
def getEmployeeName(employee):
    ename = employee.fName + " " + employee.lName
    return ename

# Funktion gibt den Mitarbeiter mit einem bestimmten Namen zurueck
def getEmployeeByName(r, empname):
    for e in r.employees:
        ename = e.fName + " " + e.lName
        if ename==empname:
            return(e)
    print("Es existiert kein Mitarbeiter mit der ID " + str(empname))

# Ändert den Status eines Mitarbeiters in seinem Schichtverzeichnis
def changeEmployeeShift(r,date,e, status):
    for key, value in getEmployeeByName(r, e).shifts.items():
        if (key == date):
            getEmployeeByName(r, e).shifts[key] = status
            return(r)
    print("Der angegebene Tag existiert nicht im Mitarbeiterschichtverzeichnis.")

def getNoErsatzNurses(a,nurses):
    # gibt die Anzahl der Nurses für eine bestimmte Schicht und Tag zurück, welche als Ersatz zur Verfügung stehen
    count = 0
    for i in range(len(nurses)):
        if(nurses[i][0][0] == a[0] and nurses[i][0][1] == a[1]):
            count = count+1
    return count

def getErsatzNurseNames(a, nurses):
    # gibt eine Liste der ErsatzNurse Namen zurück aus Nurse für eine Schicht a
    count = []
    for i in range(len(nurses)):
        if(nurses[i][0][0] == a[0] and nurses[i][0][1] == a[1]):
            count.append(nurses[i][1])
    return count

def daterange(start_date, end_date):
    # iterates over all days between given start and end date
    for n in range(int ((end_date - start_date).days)):
        yield start_date + timedelta(n)

def getConsecStartDay(today,r, employee):
    # findet heraus, ob Tag Start einer Consekutiven Reihe eines Mitarbeiters ist
    # works only for employees who are not a Leih Nurse
    if(today != r.start): # für mitten in der periode
        yesterday = (datetime.strptime(today,"%Y-%m-%d") - timedelta(days=1)).strftime("%Y-%m-%d")
        if(getShiftByEmployeeByDate01(r,today,employee)==1 and getShiftByEmployeeByDate01(r,yesterday,employee)==0):
            return(1)
        return(0)
    else: # für ersten Tag der Periode
        # wenn empl. heute arbeitet und last assigned shift type == None
        if(getShiftByEmployeeByDate01(r,today,employee)==1 and
               (employee.history["lastAssignedShiftType"] != "Spaet" and employee.history["lastAssignedShiftType"]!="Frueh")):
            return(1)
        return(0)