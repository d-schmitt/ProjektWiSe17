# Simlationsfunktion - Eingabeparameter: Objekt der Klasse Roster
from datetime import datetime, timedelta
from event import Event
from Test.event import shiftBegin, shiftEnd, vacationBegin, vacationEnd,\
    illnessBegin, illnessEnd

# Zeitlicher Ablauf der Simulation
def simulate(r, log_file):
    
    currentRoster = r
    
    i = 0                                                       # Simulationsuhr initialisieren
    currentTime = datetime.strptime(r.start, '%Y-%m-%d')        # Zeitrechner initialisieren
    
    # Initiale Eregnisse jeder Sorte terminieren
    initialShiftBegin = shiftBegin(r, currentTime)
    initialVacationBegin = vacationBegin(r, currentTime)
    initialVacationEnd = vacationEnd(r, currentTime)
    initialIllness = illnessBegin(r,currentTime);
    eventList = {initialShiftBegin.date:initialShiftBegin, initialVacationBegin.date:initialVacationBegin, initialVacationEnd.date:initialVacationEnd, initialIllness.date:initialIllness}
    
    while i < r.cntDays*24*2:         # setzt die zeitliche Simulationsschrittlaenge auf 30 min

        i += 1                                                  # Simulationsiterator eine Stunde hochzaehlen
        currentTime += timedelta(minutes=30)                       # Umgerechnete Zeit um eine Stunde hochzaehlen
        
        # TODO: So anpassen, dass mehrere Events zur gleichen Zeit eintreten koennen
        
        # In jedem Simulationsschritt pruefen, ob fuer den Zeitpunkt ein Event terminiert wurde
        if eventList.__contains__(currentTime):
    
            currentEvent = eventList.get(currentTime)
            
            # Falls es sich bei dem Ereignis um einen Schichtbegin handelt
            if isinstance(currentEvent, shiftBegin):
                
                log_file.write(str(currentEvent.date) + ": " + str(currentEvent) + "\n")
                
                # Zustandsaenderungen taetigen
                currentRoster = currentEvent.changeState(currentRoster, log_file)
                        
                # Schichtende und naechsten Schichtbeginn terminieren und der Ereignisliste hinzufuegen
                thisShiftEnd = shiftEnd(currentEvent.type, currentEvent.date, currentRoster)        
                nextShiftBeginn = shiftBegin(currentRoster, currentTime)                            
                eventList.update({thisShiftEnd.date:thisShiftEnd})                      
                eventList.update({nextShiftBeginn.date:nextShiftBeginn})                    
            
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
                eventList.update({nextVacationBegin.date:nextVacationBegin})
                    
            # Falls es sich bei dem Ereignis um ein Urlaubsende handelt   
            if isinstance(currentEvent, vacationEnd):
                
                log_file.write(str(currentEvent.date) + ": " + str(currentEvent) + "\n")
                
                # Zustandsaenderungen taetigen
                currentRoster = currentEvent.changeState(currentRoster, log_file)
                
                # Naechsten Urlaubsbeginn terminieren
                nextVacationEnd = vacationEnd(currentRoster, currentTime)
                eventList.update({nextVacationEnd.date:nextVacationEnd})
                
            # Falls es sich bei dem Ereignis um einen Krankheitsbeginn handelt
            if isinstance(currentEvent, illnessBegin):
                
                log_file.write(str(currentEvent.date) + ": " + str(currentEvent) + "--" + currentEvent.employee.fName + "\n")
                print(str(currentEvent.date) + ": " + str(currentEvent) + "--" + currentEvent.employee.fName + "\n")
                
                # Zustandsaenderungen taetigen
                currentRoster = currentEvent.changeState(currentRoster, log_file)
                
                currentRoster.reSchedule(currentTime, currentEvent.employee.eID, currentEvent.duration.days)
                
                # Naechstes Krankheitsende terminieren
                thisIllnessEnd = illnessEnd(currentRoster, currentTime, currentEvent.employee, currentEvent.duration)
                eventList.update({thisIllnessEnd.date:thisIllnessEnd})
                
                # Naechsten Krankheitsbeginn terminieren
                nextIllnessBegin = illnessBegin(currentRoster, currentTime)    
                eventList.update({nextIllnessBegin.date:nextIllnessBegin})
                
            # Falls es sich bei dem Ereignis um einen Krankheitsende handelt
            if isinstance(currentEvent, illnessEnd):
                
                log_file.write(str(currentEvent.date) + ": " + str(currentEvent) + "--" + currentEvent.employee.fName +  "\n")
                print(str(currentEvent.date) + ": " + str(currentEvent) + "--" + currentEvent.employee.fName + "\n")
                
                # Zustandsaenderungen taetigen
                currentRoster = currentEvent.changeState(currentRoster, log_file)
    
    
    log_file.write("####################################################################################\n")
    log_file.write("Ende der Simulation\n")
    log_file.write("####################################################################################\n")
    
    log_file.write("\n")
    log_file.write("\n")
    log_file.write("\n")
    
    log_file.write("####################################################################################\n")
    log_file.write("Zusammenfassung der Ergebnisse der Simulation\n")
    log_file.write("####################################################################################\n")                 
    
                
    # Simulationsergebnisse zusammenfassen
    # 1. Arbeitsstunden
    log_file.write("\n")
    log_file.write("Gearbeitete Stunden im Simulationszeitraum\n")
    log_file.write("------------------------------------------\n")
    log_file.write("\n")
    for e in currentRoster.employees:
        log_file.write(e.fName + " " + e.lName + ": " + str(e.hoursWorked) + "\n")
        
        
    # 2. Krankheitsbedingte Ausfaelle
    log_file.write("\n")
    log_file.write("Anzahl der Krankheitsbedingten Ausfaelle\n")
    log_file.write("------------------------------------------\n")
    log_file.write("\n")
    for e in currentRoster.employees:
        log_file.write(e.fName + " " + e.lName + ": " + str(e.illnessDaysThisMonth) + "\n")
        
        
        
        
    log_file.write("\n")
    log_file.write("\n")
    log_file.write("\n")
        
                
                
                
                