# Simlationsfunktion - Eingabeparameter: Objekt der Klasse Roster
from datetime import datetime, timedelta
from Test.event import Event
from Test.event import shiftBegin, shiftEnd, vacationBegin, vacationEnd,\
    illnessBegin, illnessEnd
    
# Zufriedenheit der Mitarbeiter vorab berechnen    
def calculateSatisfaction(r):
    for ro in r.requests:
        cEmp = r.getEmployeeById(ro["employeeID"])
        if cEmp.shifts[ro["day"]] == "None" or cEmp.shifts[ro["day"]] == "vacationDay" or cEmp.shifts[ro["day"]] == "offDay":
            x = 1
        else:
            if ro["shiftType"] == cEmp.shifts[ro["day"]]:
                cEmp.satisfactionScore += ro["preference"]
    return r


# Ueber- Unterstunden vorab berechnen
def calculateWeeklyOverUnderTime(r):
    dayTime = datetime.strptime(r.start, '%Y-%m-%d')        # Zeitrechner initialisieren
    mDay = 1
    currentWeek = 0
    while(mDay <= r.cntDays):
        if dayTime.weekday() == 0 and mDay != 1:
            currentWeek += 1
        stringDate = dayTime.strftime('%Y-%m-%d')
        for e in r.employees:
            if e.shifts[stringDate] == "offDay" or e.shifts[stringDate] == "None":
                e.overUnderTime[currentWeek] = e.overUnderTime[currentWeek]
            if e.shifts[stringDate] == "vacationDay":
                e.overUnderTime[currentWeek] += e.hours/5
            else:
                shiftDef = r.getShiftDefByName(e.shifts[stringDate])
                if shiftDef != 0:
                    e.overUnderTime[currentWeek] += shiftDef["workingHours"]   
        dayTime += timedelta(days=1)
        mDay += 1
    
    for e in r.employees:
        i = 0
        while i < len(r.workDaysPerWeek):
            e.overUnderTime[i] = e.overUnderTime[i] - (r.workDaysPerWeek[i] * (e.hours/5))
            i += 1    
    return r


# Zeitlicher Ablauf der Simulation
def simulate(r, log_file):
    
    # Zufriedenheit der Mitarbeiter vorab berechnen 
    r = calculateSatisfaction(r)
    
    # Ueber- Unterstunden vorab berechnen
    r = calculateWeeklyOverUnderTime(r)
    
    # urspruenglich geplante Arbeitsstunden berechnen (wird am Ende zum Abgleich mit tatsaechlich gearbeitetetn Stunden benoetigt)
    plannedHours = {}
    for emp in r.employees:
        plannedHours.update({emp.eID:0})
        for key, value in emp.shifts.items():
            sType = r.getShiftDefByName(value)
            if sType != 0:
                plannedHours[emp.eID] += sType["workingHours"]
    
    
    currentRoster = r
    
    i = 0                                                       # Simulationsuhr initialisieren
    currentTime = datetime.strptime(r.start, '%Y-%m-%d')        # Zeitrechner initialisieren
    
    # Initiale Eregnisse jeder Sorte terminieren
    initialShiftBegin = shiftBegin(r, currentTime)
    initialVacationBegin = vacationBegin(r, currentTime)
    initialVacationEnd = vacationEnd(r, currentTime)
    initialIllness = illnessBegin(r, currentTime, 0);
    eventList = {initialShiftBegin.date:[initialShiftBegin], initialVacationBegin.date:[initialVacationBegin], initialVacationEnd.date:[initialVacationEnd], initialIllness.date:[initialIllness]}
    
    while i < r.cntDays*24*2:         # setzt die zeitliche Simulationsschrittlaenge auf 30 min

        i += 1                                                  # Simulationsiterator eine Stunde hochzaehlen
        currentTime += timedelta(minutes=30)                       # Umgerechnete Zeit um eine Stunde hochzaehlen
        
        # In jedem Simulationsschritt pruefen, ob fuer den Zeitpunkt ein Event terminiert wurde
        if eventList.__contains__(currentTime):
    
            currentEvents = eventList.get(currentTime)
            
            for currentEvent in currentEvents:
                
                newEvents = {}                                          # sammelt alle neuen Events pro Iteration
            
                # Falls es sich bei dem Ereignis um einen Schichtbegin handelt
                if isinstance(currentEvent, shiftBegin):
                    
                    log_file.write(str(currentEvent.date) + ": " + str(currentEvent) + "\n")
                    
                    # Zustandsaenderungen taetigen
                    currentRoster = currentEvent.changeState(currentRoster, log_file)
                            
                    # Schichtende und naechsten Schichtbeginn terminieren und der Ereignisliste hinzufuegen
                    thisShiftEnd = shiftEnd(currentEvent.type, currentEvent.date, currentRoster)        
                    nextShiftBeginn = shiftBegin(currentRoster, currentTime)                            
                    #eventList.update({thisShiftEnd.date:[thisShiftEnd]})                      
                    #eventList.update({nextShiftBeginn.date:[nextShiftBeginn]})
                    newEvents.update({thisShiftEnd.date:thisShiftEnd})                      
                    newEvents.update({nextShiftBeginn.date:nextShiftBeginn})                     
                
                # Falls es sich bei dem Ereignis um ein Schichtende handelt   
                if isinstance(currentEvent, shiftEnd):
                    
                    log_file.write(str(currentEvent.date) + ": " + str(currentEvent) + "\n")
                    
                    # Zustandsaenderungen taetigen
                    currentRoster = currentEvent.changeState(currentRoster, log_file)
                    
                # Falls es sich bei dem Ereignis um einen Urlaubsbeginn handelt   
                if isinstance(currentEvent, vacationBegin):
                    
                    log_file.write(str(currentEvent.date) + ": " + str(currentEvent) + "\n")
                    
                    # Zustandsaenderungen taetigen
                    currentRoster = currentEvent.changeState(currentRoster, log_file)
                    
                    # Naechsten Urlaubsbeginn terminieren
                    nextVacationBegin = vacationBegin(currentRoster, currentTime)
                    #eventList.update({nextVacationBegin.date:[nextVacationBegin]})
                    newEvents.update({nextVacationBegin.date:nextVacationBegin})
                        
                # Falls es sich bei dem Ereignis um ein Urlaubsende handelt   
                if isinstance(currentEvent, vacationEnd):
                    
                    log_file.write(str(currentEvent.date) + ": " + str(currentEvent) + "\n")
                    
                    # Zustandsaenderungen taetigen
                    currentRoster = currentEvent.changeState(currentRoster, log_file)
                    
                    # Naechsten Urlaubsbeginn terminieren
                    nextVacationEnd = vacationEnd(currentRoster, currentTime)
                    #eventList.update({nextVacationEnd.date:[nextVacationEnd]})
                    newEvents.update({nextVacationEnd.date:nextVacationEnd})
                    
                # Falls es sich bei dem Ereignis um einen Krankheitsbeginn handelt
                if isinstance(currentEvent, illnessBegin):
                    
                    log_file.write(str(currentEvent.date) + ": " + str(currentEvent) + "--" + currentEvent.employee.fName + "\n")
                    print(str(currentEvent.date) + ": " + str(currentEvent) + "--" + currentEvent.employee.fName + "\n")
                    
                    # Zustandsaenderungen taetigen
                    currentRoster = currentEvent.changeState(currentRoster, log_file, currentTime)
                    
                    # Re-Scheduling aufrufen
                    currentRoster.reSchedule(currentTime, currentEvent.employee.eID, currentEvent.duration.days, log_file)
                    
                    # Dieses Krankheitsende terminieren
                    thisIllnessEnd = illnessEnd(currentRoster, currentTime, currentEvent.employee, currentEvent.duration)
                    #eventList.update({thisIllnessEnd.date:[thisIllnessEnd]})
                    newEvents.update({thisIllnessEnd.date:thisIllnessEnd})
                    
                    # Naechsten Krankheitsbeginn terminieren
                    nextIllnessBegin = illnessBegin(currentRoster, currentTime, currentEvent.employee.eID)    
                    #eventList.update({nextIllnessBegin.date:[nextIllnessBegin]})
                    newEvents.update({nextIllnessBegin.date:nextIllnessBegin})
                    
                # Falls es sich bei dem Ereignis um einen Krankheitsende handelt
                if isinstance(currentEvent, illnessEnd):
                    
                    log_file.write(str(currentEvent.date) + ": " + str(currentEvent) + "--" + currentEvent.employee.fName +  "\n")
                    print(str(currentEvent.date) + ": " + str(currentEvent) + "--" + currentEvent.employee.fName + "\n")
                    
                    # Zustandsaenderungen taetigen
                    currentRoster = currentEvent.changeState(currentRoster, log_file)
                
                # neue Events der Ereignisliste hinzufuegen
                for key, value in newEvents.items():
                    if eventList.__contains__(key):
                        print(str(key) + ": " + str(value) + "--" + "Zu diesem Zeitpunkt existiert bereits ein Ereignis")
                        eventList[key].append(value)
                    else:
                        eventList.update({key:[value]})
                #print(newEvents)
            
                
    
    log_file.write("####################################################################################\n")
    log_file.write("Ende der Simulation\n")
    log_file.write("####################################################################################\n")
    
    log_file.write("\n")
    log_file.write("\n")
    log_file.write("\n")
    
    log_file.write("####################################################################################\n")
    log_file.write("Zusammenfassung der Ergebnisse der Simulation\n")
    log_file.write("####################################################################################\n")
    
    """
    # gearbeitete Stunden
    workedHours = {}
    for emp in r.employees:
        workedHours.update({emp.eID:0})
        for key, value in emp.shifts.items():
            sType = r.getShiftDefByName(value)
            if sType != 0:
                workedHours[emp.eID] += sType["workingHours"]                 
    """
    
    # Urlaubsstunden
    vacationHours = {}
    vacationDays = {}
    for emp in r.employees:
        vacationHours.update({emp.eID:0})
        vacationDays.update({emp.eID:0})
        for key, value in emp.shifts.items():
            if value == "vacationDay":
                vacationHours[emp.eID] += emp.hours/5
                vacationDays[emp.eID] += 1
                
                
    # Soll-Arbeitszeit berechnen
    demandedHours = {}
    for empl in currentRoster.employees:
        currentDay = datetime.strptime(r.start, '%Y-%m-%d')
        demandedHours.update({empl.eID:0})
        j = 0
        while j < r.cntDays:
            if currentDay.weekday() != 5 and currentDay.weekday() != 6 and empl.eID != 0:
                demandedHours[empl.eID] += empl.hours/5
            currentDay += timedelta(days=1)
            j += 1
    
    
                
    # Simulationsergebnisse zusammenfassen
    
    # 0. urspruenglich geplante Arbeitsstunden
    log_file.write("\n")
    log_file.write("Urspruenglich geplante Stunden im Simulationszeitraum\n")
    log_file.write("------------------------------------------\n")
    log_file.write("\n")
    for e, value in plannedHours.items():
        empl = r.getEmployeeById(e)
        log_file.write(empl.fName + " " + empl.lName + ": " + str(value) + "\n")
    
    
    # 1. Arbeitsstunden
    log_file.write("\n")
    log_file.write("Gearbeitete Stunden im Simulationszeitraum\n")
    log_file.write("------------------------------------------\n")
    log_file.write("\n")
    for e in currentRoster.employees:
        log_file.write(e.fName + " " + e.lName + ": " + str(e.hoursWorked) + "\n")
        
    """
    # Arbeitsstunden v2
    log_file.write("\n")
    log_file.write("Gearbeitete Stunden im Simulationszeitraum 2\n")
    log_file.write("------------------------------------------\n")
    log_file.write("\n")
    for e, value in workedHours.items():
        empl = r.getEmployeeById(e)
        log_file.write(empl.fName + " " + empl.lName + ": " + str(value) + "\n")    
    """
        
    # 2. Krankheitsstunden
    log_file.write("\n")
    log_file.write("Aufgrund von Krankheit verpasste Stunden im Simulationszeitraum\n")
    log_file.write("------------------------------------------\n")
    log_file.write("\n")
    for e in currentRoster.employees:
        log_file.write(e.fName + " " + e.lName + ": " + str(e.illnessHoursThisMonth) + "\n")
        
    
    # 3. Zusatzstunden
    log_file.write("\n")
    log_file.write("Durch Re-Scheduling zugewiesene Zusatzstunden\n")
    log_file.write("------------------------------------------\n")
    log_file.write("\n")
    for e in currentRoster.employees:
        log_file.write(e.fName + " " + e.lName + ": " + str(e.extraHours) + "\n")
        
        
    # 4. Krankheitsbedingte Ausfaelle
    log_file.write("\n")
    log_file.write("Anzahl der Krankheitsbedingten Ausfaelle\n")
    log_file.write("------------------------------------------\n")
    log_file.write("\n")
    for e in currentRoster.employees:
        log_file.write(e.fName + " " + e.lName + ": " + str(e.illnessDaysThisMonth) + "\n")
        
        
    # 5. Urlaubsstunden
    log_file.write("\n")
    log_file.write("Anzahl der Urlaubsstunden\n")
    log_file.write("------------------------------------------\n")
    log_file.write("\n")
    for key, value in vacationHours.items():
        empl = r.getEmployeeById(key)
        log_file.write(empl.fName + " " + empl.lName + ": " + str(value) + "\n")
        
        
    # 6. Urlaubstage
    log_file.write("\n")
    log_file.write("Anzahl der Urlaubstage\n")
    log_file.write("------------------------------------------\n")
    log_file.write("\n")
    for key, value in vacationDays.items():
        empl = r.getEmployeeById(key)
        log_file.write(empl.fName + " " + empl.lName + ": " + str(value) + "\n")
        
        
    # 7. Soll Arbeitszeit laut Vertrag
    log_file.write("\n")
    log_file.write("Vertraglich verpflichtete Arbeitsstunden im Monat\n")
    log_file.write("------------------------------------------\n")
    log_file.write("\n")
    for key, value in demandedHours.items():
        empl = r.getEmployeeById(key)
        log_file.write(empl.fName + " " + empl.lName + ": " + str(value) + "\n")
        
        
    # 8. Uber-/ Unterstunden
    log_file.write("\n")
    log_file.write("Ueber- / Unterstunden\n")
    log_file.write("------------------------------------------\n")
    log_file.write("\n")
    for e in currentRoster.employees:
        log_file.write(e.fName + " " + e.lName + ": " + str((e.hoursWorked + vacationHours[e.eID] + e.illnessHoursThisMonth) - demandedHours[e.eID]) + "\n")     
        
        
        
    log_file.write("\n")
    log_file.write("\n")
    log_file.write("\n")
        
                
                
                
                