
from Test.reschedulingHelpers import *

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


