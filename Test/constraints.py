
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
        ename = i.fName+" "+i.lName
        onList, offList = roster.getOnOffDays(ename)

        # for each day he/she neither has an offday or vacation day
        for j in onList:
            shiftassignments = 0 # counts how many shifts have been assigned to one employee per day

            # for each shift
            for k in roster.shiftTypes:

            # check if employee i works shift k on day j
                # make a list with working employees for the day and shift
                EmployeesWorkingShiftThatDay = roster.getWorkingEmployees(j, k['name'])

                # check if current employee i is in list
                for e in EmployeesWorkingShiftThatDay:
                    if(e ==ename):
                        shiftassignments = shiftassignments+1

            # if one employee has more than one shift per day assigned, return false
            if(shiftassignments>1):
                return False
    return True

def checkDaysOff_old(roster):
    """
    Each employee should not work on his/her day offs.
    Old Version of the CheckDaysOff Constraint.
    New Version see below.

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
        if(len(i.vacation)>0): # da Leihnurse keine Vacation Days hat
            for j in i.vacation: # Für jeden Vacation Day
                if(getShiftByEmployeeByDate01(roster,j,i)==1): # Wenn Nurse dort arbeitet, dann return false
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
        if(len(i.off)>0): # da Leihnurse keine Off Days hat
            for j in i.off: # Für jeden Off Day
                if(getShiftByEmployeeByDate01(roster,j,i)==1): # Wenn Nurse dort arbeitet, dann return false
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
            if (getShiftByEmployeeByDate01(roster, sdDay, i) == 1):
                dayCount += 1
        assignments.append(dayCount)

    # checks if Assignments and Demand are the same for each day
    for i in range(0, len(assignments)):
        if (demandPerDay[i] != assignments[i]):
            return False
    return True

def checkWeeklyWorkingHours(roster):
    """
    Für jeden Employee und jede Woche gilt:
    Die Summe an Wochenstunden über die Tagen und Schichten die ein Employee arbeitet
    – dessen Überstunden und
    + die Unterstunden
    = müssen gleich der regular working hours sein
    :param roster:
    :return:
    """
    """
    Für jeden Employee und jede Woche gilt: Die Summe an Wochenstunden über die Tagen und Schichten die ein Employee arbeitet – dessen Überstunden und + die Unterstunden müssen gleich der regular working hours sein
Für jeden Mitarbeiter i
Für jede Woche j aus getWeeks
Für jeden Tag der Woche d
Für jede Schicht s

Wenn getContract(i).RegularWorkingHours != """

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
    for single_date in daterange(start_date, end_date):# checkt er hier auch letzten Tag?
        sdDay = single_date.strftime("%Y-%m-%d")
        if(sdDay != roster.start): # for all days not being the first day in the period
            sdDayBefore = (single_date - timedelta(days=1)).strftime("%Y-%m-%d")
            # for each employee
            for i in roster.employees:
                if (i.lName != "Nurse"): # for all nurses except Leih Nurses
                    startDay = getConsecStartDay(sdDay, roster, i)
                    if ((getShiftByEmployeeByDate01(roster, sdDay, i) - getShiftByEmployeeByDate01(roster, sdDayBefore,
                                                                                                   i) - startDay > 0)
                        or (getShiftByEmployeeByDate01(roster, sdDay, i) - startDay < 0)
                        or (startDay + getShiftByEmployeeByDate01(roster, sdDayBefore, i) > 1)):
                        return False
        else: # for first day in period
            # for each employee
            for i in roster.employees:
                if(i.lName != "Nurse"):
                    startDay = getConsecStartDay(sdDay, roster, i)
                    oldPeriod=0
                    if(i.history["lastAssignedShiftType"]=="Spaet" or i.history["lastAssignedShiftType"]=="Frueh"):
                        oldPeriod=1
                    if ((getShiftByEmployeeByDate01(roster, sdDay, i) - oldPeriod - startDay > 0)
                        or (getShiftByEmployeeByDate01(roster, sdDay, i) - startDay < 0)
                        or (startDay + oldPeriod > 1)):
                        return False
    return True
