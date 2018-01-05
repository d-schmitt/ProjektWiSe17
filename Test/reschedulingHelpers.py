from datetime import datetime, timedelta, date
from Test.constraints import *

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
# TODO: durch diese kleine Aenderung kann man die Laufzeit von n^2 auf n reduzieren
# Ich habe dir zum Vergleich deinen Code kommentiert stehen lassen
def changeEmployeeShift(r,date,e, status):
    employee = getEmployeeByName(r, e)
    for key, value in getEmployeeByName(r, e).shifts.items():
        if (key == date):
            employee.shifts[key] = status
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
    eWorks = getShiftByEmployeeByDate01(r,today,employee)
    if(today != r.start): # für mitten in der periode
        yesterday = (datetime.strptime(today,"%Y-%m-%d") - timedelta(days=1)).strftime("%Y-%m-%d")
        eWorksY= getShiftByEmployeeByDate01(r, yesterday, employee)
        if(eWorks==1 and eWorksY==0):
            return(1)
        return(0)
    else: # für ersten Tag der Periode
        # wenn empl. heute arbeitet und last assigned shift type == None
        if(eWorks == 1 and
               (employee.history["lastAssignedShiftType"] != "Spaet" and employee.history["lastAssignedShiftType"]!="Frueh")):
            return(1)
        return(0)


def MinMaxSatisfaction(roster):
    """
    Calculates min und max Satisfaction Score of roster
    :param roster:
    :return: satmin, satmax
    """
    satmax = 0
    satmin = 0
    for i in roster.employees:
        if (i.satisfactionScore >= satmax):
            satmax = i.satisfactionScore

        if (i.satisfactionScore <= satmin):
            satmin = i.satisfactionScore

    return satmin, satmax

def cumSatScore(roster):
    """
    Returns cumulative Satisfaction Score
    :param roster:
    :return:
    """
    cumulativeSatScore = 0
    for i in roster.employees:
        cumulativeSatScore += i.satisfactionScore
        #cumulativeSatScore += abs(i.satisfactionScore) # absolute value

    return cumulativeSatScore

def getMondays(roster):
    """
    returns a list with all mondays within the period
    :param roster:
    :return:
    """
    weeks = []
    currentTime = datetime.strptime(roster.start, '%Y-%m-%d')
    start_date = date(currentTime.year, currentTime.month, currentTime.day)
    end_period = currentTime + timedelta(days=roster.cntDays - 1)
    end_date = date(end_period.year, end_period.month, end_period.day)

    for single_date in daterange(start_date, end_date +timedelta(days=1)):
        d = single_date.strftime("%Y-%m-%d")
        if(single_date.weekday()==0): # Monday
            weeks.append(d)
    return weeks

def getWeekNo(r,date):
    """
    Returns the Week No. of a given date
    :param r: roster
    :param date: current day
    :return: no. of weeks the current day lies in a month
    """
    fDay = r.start
    dayTime = datetime.strptime(fDay, '%Y-%m-%d')

    mDay = 1
    cntWeeks = 1
    while mDay <= int(date.day):
        if dayTime.weekday() == 0 and mDay != 1:
            cntWeeks += 1
        dayTime += timedelta(days=1)
        mDay += 1

    return cntWeeks

def getDayDifference(start_date,current_date):
    """
    calculates the difference in days between two dates
    :return:
    """
    newDay = int(current_date[8:])
    startDay = int(start_date.day)

    difference = newDay - startDay
    return difference

def getSatisfactionScoreChanges(r, start_date, currentDay, currentShift, empName):
    """
    Änderung des Satisfaction Score berechnen: (-5 / Anzahl Tage vorher Bescheid Abzug für Satisfaction Score+1)
    :return:
    """

    # Berechnung Unzufriedenheit wegen kurzfristigem Einsatz
    dayDifference = getDayDifference(start_date, currentDay)
    maxSatisfactionScoreReduction = 5
    satisfactionScoreChange = -(maxSatisfactionScoreReduction / (dayDifference + 1))  # +1 to avoid dayDifference being 0

    # Überprüfung: Hat Mitarbeiter so Wunschtag/Hasstag erhalten?
    employeeID = getEmployeeByName(r, empName).eID
    for request in r.requests:
        if (request['employeeID'] == employeeID and request['shiftType'] == currentShift
            and request['day'] == currentDay):
            satisfactionScoreChange += request['preference']

    return satisfactionScoreChange

def getObjectiveFunction(r):
    """
    Berechnet den Zielfunktionswert aus Überstunden und Zufriedenheit der Mitarbeiter für ein gegebenes Roster
    :param r: roster
    :return: Zielfunktionswert
    """
    maxSatisfactionScore = 0
    minSatisfactionScore = 0

    maxOvertime = 0
    minOvertime = 0
    for e in r.employees:
        # Zufriedenheit
        empSatisfactionScore = e.satisfactionScore
        if (empSatisfactionScore > maxSatisfactionScore):
            maxSatisfactionScore = empSatisfactionScore
        if (empSatisfactionScore < minSatisfactionScore):
            minSatisfactionScore = empSatisfactionScore

        # Überstunden
        empOvertime = e.extraHours
        if (empOvertime > maxOvertime):
            maxOvertime = empOvertime
        if (empOvertime < minOvertime):
            minOvertime = empOvertime

    alpha = 0.5
    beta = 0.5
    objectiveFunction = alpha*(maxSatisfactionScore-minSatisfactionScore) + beta*(maxOvertime-minOvertime)
    return objectiveFunction
