# Rosterklasse als Uebergabeobjekt zwischen Rescheduling und Simulation
class Roster(object):
    
    # Konstruktor
    def __init__(self, s, infos, empList):
        self.shifts = s                 # Umformatierter Schichtplan
        self.planID = infos[0]          # Plan ID
        self.cntDays = infos[1]         # Anzahl Tage
        self.cntWeeks = infos[2]        # Anzahl Wochen
        self.start = infos[3]           # Startdatum des Plans
        self.maxSun = infos[4]          # Maximale Anzahl Sonntage
        self.maxOver = infos[5]         # Maximale Anzahl Ueberstunden
        self.maxUnder = infos[6]        # Maximale Anzahl Unterstudnen
        self.forbidden = infos[7]       # Verbotene Schichtfolgen
        self.contracts = infos[8]       # Standard Arbeitsvertrag
        self.requests = infos[9]        # Anfragen von Mitarbeitern nach Schichten
        self.fixed = infos[10]          # Fest zugewiesene Schichten
        self.employees = empList        # Liste aller Mitarbeiter
        
        
        
    # Funktion gibt den Mitarbeiter mit einer bestimmten ID zurueck
    def getEmployeeById(self, empID):
        for e in self.employees:
            if e.eID == empID:
                return(e)
        print("Es existiert kein Mitarbeiter mit der ID " + str(empID))
        