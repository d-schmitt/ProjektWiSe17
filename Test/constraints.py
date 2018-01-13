from Test.reschedulingHelpers import *
from datetime import datetime, timedelta, date

def checkShiftAssignments(roster):
    """
    Each employee is not allowed to work more than one shift per day.
    :param roster:
    :return: True, if all employees do not work more than one shift per day.
             False, if at least one employee works more than one shift per day.
    """

    # for each employee i
    for i in roster.employees:
        ename = i.fName + " " + i.lName
        onList, offList = roster.getOnOffDays(ename)

        # for each day he/she neither has an offday or vacation day
        for j in onList:
            shiftassignments = 0  # counts how many shifts have been assigned to one employee per day

            # for each shift
            for k in roster.shiftTypes:

                # check if employee i works shift k on day j
                # make a list with working employees for the day and shift
                EmployeesWorkingShiftThatDay = roster.getWorkingEmployees(j, k['name'])

                # check if current employee i is in list
                for e in EmployeesWorkingShiftThatDay:
                    if (e == ename):
                        shiftassignments = shiftassignments + 1

            # if one employee has more than one shift per day assigned, return false
            if (shiftassignments > 1):
                return False
    return True


def checkDaysOff_old(roster):
    """
    Each employee should not work on his/her day offs.
    Old Version of the CheckDaysOff Constraint.
    New Version see below.
    ** Outdated**

    :param roster:
    :return: True if no employee works on his/her day offs
             False, if at least one employee works on his/her day off
    """

    for i in roster.employees:
        ename = i.fName + " " + i.lName
        onList, offList = roster.getOnOffDays(ename)

        # for each offday or vacation day
        for j in offList:
            shiftassignments = 0  # counts how many shifts have been assigned to employee per day

            # for each shift
            for k in roster.shiftTypes:

                # check if employee i works shift k on day j
                # make a list with working employees for the day and shift
                EmployeesWorkingShiftThatDay = roster.getWorkingEmployees(j, k['name'])

                # check if current employee i is in list
                for e in EmployeesWorkingShiftThatDay:
                    if (e == ename):
                        shiftassignments = shiftassignments + 1

            # if one employee has more than zero shifts per day assigned on his/her day off, return false
            if (shiftassignments > 0):
                return False

    return True


def checkVacationDaysOff(roster):
    """
    Each employee should not work on his/her day offs.
    :param roster:
    :return: True if no employee works on his/her vacation day
             False, if at least one employee works on his/her vacation day
    """
    # Für jeden Mitarbeiter
    for i in roster.employees:
        # for each vacation day
        if (len(i.vacation) > 0):  # da Leihnurse keine Vacation Days hat
            for j in i.vacation:  # Für jeden Vacation Day
                if (getShiftByEmployeeByDate01(roster, j, i) == 1):  # Wenn Nurse dort arbeitet, dann return false
                    return False
    return True


def checkOffDaysOff(roster):
    """
    Each employee should not work on his/her day offs.
    :param roster:
    :return: True if no employee works on his/her off day
             False, if at least one employee works on his/her off day
    """
    # Für jeden Mitarbeiter
    for i in roster.employees:
        # for each Off day
        if (len(i.off) > 0):  # da Leihnurse keine Off Days hat
            for j in i.off:  # Für jeden Off Day
                if (getShiftByEmployeeByDate01(roster, j, i) == 1):  # Wenn Nurse dort arbeitet, dann return false
                    return False
    return True


def checkShiftAssignmentToDemand(roster):
    """
    Prio 2 Constraint
    Überprüft, ob Shift Assignments für den Tag mit dem entsprechendem Demand übereinstimmen.
    :param roster: Dienstplanroster
    :return: True if shift assignment and demand are the same
             False if shift assignment and demand do not fit
    """
    # Variable für Demand: shiftTypes[0].requirements
    currentTime = datetime.strptime(roster.start, '%Y-%m-%d')

    start_date = date(currentTime.year, currentTime.month, currentTime.day)
    end_period = currentTime + timedelta(days=roster.cntDays)
    end_date = date(end_period.year, end_period.month, end_period.day)

    # bekomme den Demand für alle Schichten
    demand = []
    for i in roster.shiftTypes:
        demand.append(i['requirements'])

    # rechne Demand für Schichten in Demand pro Tag um
    demandPerDay = []
    for i in range(0, len(demand[0])):
        demandPerDay.append(demand[0][i] + demand[1][i])

    # summiere Shift Assignments auf
    assignments = []
    for single_date in daterange(start_date, end_date):
        sdDay = single_date.strftime("%Y-%m-%d")
        dayCount = 0
        for i in roster.employees:
            if (getShiftByEmployeeByDateN(roster, sdDay, i) == 1):
                dayCount += 1
        assignments.append(dayCount)

    # checks if Assignments and Demand are the same for each day
    for i in range(0, len(assignments)):
        if (demandPerDay[i] != assignments[i]):
            return False
    return True

def checkMinMaxConsec(roster):
    """
    Constraint 7+8+9 for Minimum and Maximum of consecutive working days
    :param roster: Nurse Roster
    :return: True - if Constraint 7-9 are fulfilled
             False - if at least one Constraint is not fulfilled
    """
    currentTime = datetime.strptime(roster.start, '%Y-%m-%d')

    start_date = date(currentTime.year, currentTime.month, currentTime.day)
    end_period = currentTime + timedelta(days=roster.cntDays)
    end_date = date(end_period.year, end_period.month, end_period.day)

    # for each day
    for single_date in daterange(start_date, end_date):  # checkt er hier auch letzten Tag?
        sdDay = single_date.strftime("%Y-%m-%d")
        if (sdDay != roster.start):  # for all days not being the first day in the period
            sdDayBefore = (single_date - timedelta(days=1)).strftime("%Y-%m-%d")
            # for each employee
            for i in roster.employees:
                if (i.lName != "Nurse"):  # for all nurses except Leih Nurses
                    startDay = getConsecStartDay(sdDay, roster, i)
                    eWorks = getShiftByEmployeeByDate01(roster, sdDay, i)
                    eWorksY = getShiftByEmployeeByDate01(roster, sdDayBefore, i)

                    if ((eWorks - eWorksY - startDay > 0)
                        or (eWorks - startDay < 0)
                        or (startDay + eWorksY > 1)):
                        return False
        else:  # for first day in period
            # for each employee
            for i in roster.employees:
                if (i.lName != "Nurse"):
                    startDay = getConsecStartDay(sdDay, roster, i)
                    oldPeriod = 0
                    if (i.history["lastAssignedShiftType"] == "Spaet" or i.history["lastAssignedShiftType"] == "Frueh"):
                        oldPeriod = 1
                    eWorks = getShiftByEmployeeByDate01(roster, sdDay, i)
                    if ((eWorks - oldPeriod - startDay > 0)
                        or (eWorks - startDay < 0)
                        or (startDay + oldPeriod > 1)):
                        return False
    return True


def forbiddenPatterns(roster):
    """

    :return:
    """
    currentTime = datetime.strptime(roster.start, '%Y-%m-%d')

    start_date = date(currentTime.year, currentTime.month, currentTime.day)
    end_period = currentTime + timedelta(days=roster.cntDays - 1)
    end_date = date(end_period.year, end_period.month, end_period.day)

    for f in roster.forbidden:  # für jede verbotene Schichtreihenfolge
        for single_date in daterange(start_date, end_date):  # for each day
            sdDay = single_date.strftime("%Y-%m-%d")
            sdDayTomorrow = (single_date + timedelta(days=1)).strftime("%Y-%m-%d")
            for i in roster.employees:  # for each employee
                if (i.lName != "Nurse"):  # for all nurses except Leih Nurses
                    eWorks = getShiftByEmployeeByDateByShift(roster, sdDay, i, f['preceedingShiftType'])
                    eWorksT = getShiftByEmployeeByDateByShift(roster, sdDayTomorrow, i, f['succeedingShiftType'])
                    if (eWorks + eWorksT > 1):  # wenn nurse verbotene schichtreihenfolge arbeitet
                        return False

        # Für Periodenübergang (letzter Tag vorheriger Periode und erster Tag dieser Periode)
        sdDay = start_date.strftime("%Y-%m-%d")
        for i in roster.employees:
            if (i.lName != "Nurse"):
                eWorks = getShiftByEmployeeByDateByShift(roster, sdDay, i, f['succeedingShiftType'])
                eWorksY = 0
                if (i.history["lastAssignedShiftType"] == f['preceedingShiftType']):
                    eWorksY = 1
                if (eWorks + eWorksY > 1):
                    return False

    return True


def maxSundays(roster):
    """
    Überprüft, ob die definierte maximale Anzahl Sonntage, welche pro Mitarbeiter in einer Periode gearbeitet werden, eingehalten wird.
    :param roster:
    :return: True - if Constraint 13 is fulfilled
             False - if Constraint 13 is not fulfilled
    """

    currentTime = datetime.strptime(roster.start, '%Y-%m-%d')
    start_date = date(currentTime.year, currentTime.month, currentTime.day)
    end_period = currentTime + timedelta(days=roster.cntDays - 1)
    end_date = date(end_period.year, end_period.month, end_period.day)

    periodSun = []
    # erstelle liste mit tagen der sonntage aus periode
    for single_date in daterange(start_date, end_date + timedelta(days=1)):  # für alle Tage der Periode
        if (single_date.weekday() == 6):  # 6 = Sunday
            periodSun.append(single_date.strftime("%Y-%m-%d"))

    # überprüfe für jeden tag, ob mitarbeiter an sonntag arbeitet, falls ja, erhöhe workSun
    if (len(periodSun) > 0):
        for i in roster.employees:
            if (i.lName != "Nurse"):
                workSun = 0
                for j in periodSun:
                    eWorks = getShiftByEmployeeByDate01(roster, j, i)
                    if (eWorks == 1):
                        workSun += 1
                if (workSun > roster.maxSun):
                    return False
    return True

def maxSundaysS(roster):
    """
    Überprüft, ob die definierte maximale Anzahl Sonntage, welche pro Mitarbeiter in einer Periode gearbeitet werden, eingehalten wird.
    Zusätzliche Anpassung, sodass SatisfactionScore zurückgegeben wird
    :param roster:
    :return: True - if Constraint 13 is fulfilled
             False - if Constraint 13 is not fulfilled
    """

    currentTime = datetime.strptime(roster.start, '%Y-%m-%d')
    start_date = date(currentTime.year, currentTime.month, currentTime.day)
    end_period = currentTime + timedelta(days=roster.cntDays - 1)
    end_date = date(end_period.year, end_period.month, end_period.day)

    periodSun = []
    # erstelle liste mit tagen der sonntage aus periode
    for single_date in daterange(start_date, end_date + timedelta(days=1)):  # für alle Tage der Periode
        if (single_date.weekday() == 6):  # 6 = Sunday
            periodSun.append(single_date.strftime("%Y-%m-%d"))

    SatisfactionScore = 0
    # überprüfe für jeden tag, ob mitarbeiter an sonntag arbeitet, falls ja, erhöhe workSun
    if (len(periodSun) > 0):
        for i in roster.employees:
            if (i.lName != "Nurse"):
                workSun = 0
                for j in periodSun:
                    eWorks = getShiftByEmployeeByDate01(roster, j, i)
                    if (eWorks == 1):
                        workSun += 1
                if (workSun > roster.maxSun):
                    SatisfactionScore -= (workSun -roster.maxSun)
    return SatisfactionScore

def weekendDaysS(roster):
    """
    Constraint 14 + 15
    Muss ggf. aufgeweicht werden zwecks Krankheit
    SatisfactionScore
    :param roster:
    :return:
    """

    currentTime = datetime.strptime(roster.start, '%Y-%m-%d')
    start_date = date(currentTime.year, currentTime.month, currentTime.day)
    end_period = currentTime + timedelta(days=roster.cntDays - 1)
    end_date = date(end_period.year, end_period.month, end_period.day)

    periodSun = []
    satisfactionScore = 0
    # erstelle liste mit tagen der sonntage aus periode
    for single_date in daterange(start_date, end_date + timedelta(days=1)):  # für alle Tage der Periode
        if (single_date.weekday() == 6):  # 6 = Sunday
            periodSun.append(single_date.strftime("%Y-%m-%d"))

    if (len(periodSun) > 0):
        for i in roster.employees:
            if (i.lName != "Nurse"):
                for j in range(len(periodSun)):
                    eWorks = getShiftByEmployeeByDate01(roster, periodSun[j], i)
                    saturday = (datetime.strptime(periodSun[j], "%Y-%m-%d") - timedelta(days=1)).strftime("%Y-%m-%d")
                    eWorksY = getShiftByEmployeeByDate01(roster, saturday, i)
                    weekendConstraint = i.weekendContraints[j]
                    if (((eWorksY + eWorks) < 2 * eWorks * weekendConstraint)
                        or ((eWorksY + eWorks) < 2 * eWorksY * weekendConstraint)):
                        satisfactionScore -=1
    return satisfactionScore

def weekendDays(roster):
    """
    Constraint 14 + 15
    Muss ggf. aufgeweicht werden zwecks Krankheit
    :param roster:
    :return:
    """

    currentTime = datetime.strptime(roster.start, '%Y-%m-%d')
    start_date = date(currentTime.year, currentTime.month, currentTime.day)
    end_period = currentTime + timedelta(days=roster.cntDays - 1)
    end_date = date(end_period.year, end_period.month, end_period.day)

    periodSun = []
    # erstelle liste mit tagen der sonntage aus periode
    for single_date in daterange(start_date, end_date + timedelta(days=1)):  # für alle Tage der Periode
        if (single_date.weekday() == 6):  # 6 = Sunday
            periodSun.append(single_date.strftime("%Y-%m-%d"))

    if (len(periodSun) > 0):
        for i in roster.employees:
            if (i.lName != "Nurse"):
                for j in range(len(periodSun)):
                    eWorks = getShiftByEmployeeByDate01(roster, periodSun[j], i)
                    saturday = (datetime.strptime(periodSun[j], "%Y-%m-%d") - timedelta(days=1)).strftime("%Y-%m-%d")
                    eWorksY = getShiftByEmployeeByDate01(roster, saturday, i)
                    weekendConstraint = i.weekendContraints[j]
                    if (((eWorksY + eWorks) < 2 * eWorks * weekendConstraint)
                        or ((eWorksY + eWorks) < 2 * eWorksY * weekendConstraint)):
                        return False
    return True


def extraHours(roster):
    """
    Constraint 16 + 17
    Für jeden Employee dürfen die Extra working hours nicht die upper bound für Extra working hours überschreiten
    Für jeden Employee dürfen die Extra working hours nicht die lower bound für Extra working hours unterschreiten
    Constraint 22 + 23
    Für jeden Employee müssen die maximum hours aller Employees gleich oder größer sein wie die Extra hours des einzelnen Employee
    Für jeden Employee müssen die minimum hours aller Employees gleich oder kleiner sein wie die Extra hours des einzelnen Employee
    :param roster:
    :return:
    """
    for i in roster.employees:
        if (i.lName != "Nurse"):
            empExtraHours = i.extraHours
            if (i.eMaxExtra < empExtraHours or i.minExtra > empExtraHours
                or roster.maxOver < empExtraHours or roster.maxUnder > empExtraHours):
                return False
    return True


def fixedAssignments(roster):
    """
    Constraint 4
    Überprüft, ob die Fixed Assignments auch mit den tatsächlichen Arbeitstagen der Mitarbeiter übereinstimmen
    :param roster:
    :return:
    """
    for i in roster.fixed:
        employee = int(i['employee'])
        day = i['day']
        shift = i['shiftType']
        eWorks = getShiftByEmployeeByDateByShift(roster, day, getEmployeeById(roster, employee), shift)
        eShift = i.shifts['day']
        if (eWorks == 0 and eShift != 'sickDay' and eShift != 'vacationDay' and eShift != 'offDay'):
            return False
    return True


def minConsec(roster):
    """
    Constraint 10
    :param roster:
    :return:
    """
    currentTime = datetime.strptime(roster.start, '%Y-%m-%d')
    start_date = date(currentTime.year, currentTime.month, currentTime.day)
    end_period = currentTime + timedelta(days=roster.cntDays - 1)
    end_date = date(end_period.year, end_period.month, end_period.day)

    dayCount = 1
    for single_date in daterange(start_date, end_date + timedelta(days=1)):  # für alle Tage der Periode
        for i in roster.employees:  # für alle Mitarbeiter

            # Berechnung wieviele Tage in bisheriger Periode gearbeitet wurden
            daySum = min(roster.cntDays, (dayCount + i.minConsecutive - 1))
            consecDays = 0
            for j in range(dayCount, daySum + 1):
                d = single_date + timedelta(days=j - 1)
                d = d.strftime("%Y-%m-%d")
                consecDays += getShiftByEmployeeByDate01(roster, d, i)

            consecutiveStart = consecStart(roster, single_date, i)
            minDays = min(i.minConsecutive, roster.cntDays - dayCount + 1)

            # Überprüfung: minimale consecutive Arbeitstage müssen auch gearbeitet werden
            if (consecDays < consecutiveStart * minDays):
                return False
        dayCount += 1

    return True


def consecStart(roster, current_date, employee):
    """
    Gibt an, ob es sich bei Datum um start einer consecutiven Reihe an Arbeitstagen handelt
    :param roster:
    :return: 1, falls ja, 0 wenn nicht
    """
    startTime = datetime.strptime(roster.start, '%Y-%m-%d')
    start_date = date(startTime.year, startTime.month, startTime.day)
    # xstart berechnen (gibt an, ob start consecutiver reihe)
    sdDay = current_date.strftime("%Y-%m-%d")

    eWorks = getShiftByEmployeeByDate01(roster, sdDay, employee)
    if (current_date == start_date):  # für ersten Tag in Periode
        if (employee.history['lastAssignedShiftType'] != "Frueh" and employee.history[
            'lastAssignedShiftType'] != "Spaet"):
            eWorksY = 0
        else:
            eWorksY = 1
    else:
        sdDayY = current_date - timedelta(days=1)
        sdDayY = sdDayY.strftime("%Y-%m-%d")
        eWorksY = getShiftByEmployeeByDate01(roster, sdDayY, employee)

    if (eWorks == 1 and eWorksY == 0):
        return (1)
    else:
        return (0)


def maxConsec(roster):
    """
    Constraint 11
    :param roster:
    :return:
    """
    currentTime = datetime.strptime(roster.start, '%Y-%m-%d')
    start_date = date(currentTime.year, currentTime.month, currentTime.day)
    end_period = currentTime + timedelta(days=roster.cntDays - 1)
    end_date = date(end_period.year, end_period.month, end_period.day)

    for i in roster.employees:
        dayCount = 1
        for single_date in daterange(start_date, end_date - timedelta(days=i.maxConsecutive + 1)):
            daySum = dayCount + i.maxConsecutive
            dayStart = dayCount + i.minConsecutive

            # Summe
            consecDaysSum = 0
            for j in range(dayStart, daySum + 1):
                d = single_date + timedelta(days=j - 1)
                d = d.strftime("%Y-%m-%d")
                consecDaysSum += (1 - getShiftByEmployeeByDate01(roster, d, i))

            # xestart
            consecutiveStart = consecStart(roster, single_date, i)

            # Überprüfung
            if (consecDaysSum < consecutiveStart):
                return False

            dayCount += 1
    return True


def minConsecPeriod(roster):
    """
    Constraint 18
    :param roster:
    :return:
    """

    currentTime = datetime.strptime(roster.start, '%Y-%m-%d')
    start_date = date(currentTime.year, currentTime.month, currentTime.day)

    for i in roster.employees:  # für alle Mitarbeiter
        if (i.minConsecutive > i.history['numberOfConsecutiveWorkingDays']):
            # linke Summe
            daySum = min(i.minConsecutive - i.history['numberOfConsecutiveWorkingDays'], roster.cntDays)
            consecDays = 0
            dayCount = 1
            for j in range(dayCount, daySum + 1):
                d = start_date + timedelta(days=j - 1)
                d = d.strftime("%Y-%m-%d")
                consecDays += getShiftByEmployeeByDate01(roster, d, i)

            # rechter Teil
            eWorksY = 0
            if (i.history['lastAssignedShiftType'] == "Frueh" or i.history['lastAssignedShiftType'] == "Spaet"):
                eWorksY = 1
            rSum = min(i.minConsecutive - i.history['numberOfConsecutiveWorkingDays'], roster.cntDays - dayCount + 1)

            if (consecDays < eWorksY * rSum):
                return False
    return True


def maxConsecPeriod(roster):
    """
    Constraint 19
    :param roster:
    :return:
    """
    currentTime = datetime.strptime(roster.start, '%Y-%m-%d')
    start_date = date(currentTime.year, currentTime.month, currentTime.day)

    for i in roster.employees:  # für alle Mitarbeiter
        if (i.maxConsecutive - i.history['numberOfConsecutiveWorkingDays'] < roster.cntDays):
            # linke Summe
            dayCount = 1
            daySum = dayCount + i.maxConsecutive - i.history['numberOfConsecutiveWorkingDays']
            consecDays = 0
            for j in range(dayCount, daySum + 1):
                d = start_date + timedelta(days=j - 1)
                d = d.strftime("%Y-%m-%d")
                consecDays += (1 - getShiftByEmployeeByDate01(roster, d, i))

            # rechter Teil
            eWorksY = 0
            if (i.history['lastAssignedShiftType'] == "Frueh" or i.history['lastAssignedShiftType'] == "Spaet"):
                eWorksY = 1

            if (consecDays < eWorksY):
                return False
    return True

def MinMaxSatisfactionScore(roster):
    """
    Constraint 24+25
    :param roster:
    :return:
    """
    satmin, satmax = MinMaxSatisfaction(roster)

    for i in roster.employees:
        if(i.satisfactionScore > satmax or i.satisfactionScore < satmin):
            return False

    return True

def checkHardConstraints(r):
    """
    Überprüft harte Restriktionen
    :param r: roster
    :return:
    """
    hardConstraints = [checkShiftAssignments(r),checkVacationDaysOff(r),checkOffDaysOff(r),
                       checkShiftAssignmentToDemand(r),forbiddenPatterns(r), checkMinMaxConsec(r)]
    count = 0
    for i in hardConstraints:
        if(i == False):
            #print("Hard",count)
            return False
        count +=1
    return True

def checkAllConstraints(r):
    """
    Überprüft alle Restriktionen
    :param r: roster
    :return:
    """
    hardConstraints = [checkShiftAssignments(r),checkVacationDaysOff(r),checkOffDaysOff(r),
                       checkShiftAssignmentToDemand(r), forbiddenPatterns(r), checkMinMaxConsec(r),
                       maxSundays(r)]
    count = 0
    for i in hardConstraints:
        if(i == False):
            print("All",count)
            return False
        count +=1
    return True

def checkSoftConstraints(r):
    """
    Überprüft inwiefern Soft Constraints eingehalten wurden
    WE,x
    mehr Sonntage,x
    minimale und maximale Konsekutive Arbeitstage dürfen auch verletzt werden (fehlt noch)

    :param r:
    :return:
    """
    softConstraints = [maxSundaysS(r), weekendDaysS(r)]
    rosterScore = 0
    for i in softConstraints:
        rosterScore += i
    return rosterScore