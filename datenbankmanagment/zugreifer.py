import sqlite3


####################
##____Methoden____##
####################

##aufbauende Methoden##
def createTB_Kunde():
    cur = con.cursor()
    cur.execute("CREATE TABLE 'kunde'('username' TEXT, 'password' TEXT,'vorname' TEXT, 'nachname' TEXT,'adresse' TEXT)")

def createTB_Restaurant():
    cur = con.cursor()
    cur.execute("CREATE TABLE 'restaurant'('username' TEXT, 'password' TEXT, 'name' TEXT,'oeffnungszeiten' TEXT, 'adresse' TEXT)")

#Die Werte hier sind eventuell noch nicht passend gewählt
def createTB_Item():
    cur = con.cursor()
    cur.execute("CREATE TABLE 'item'('name' TEXT, 'preis' NUMB)")

#Die Werte hier sind eventuell noch nicht passend gewählt
def createTB_Bestellung():
    cur = con.cursor()
    cur.execute("CREATE TABLE 'bestellung' ('bestell_id' NUMB,'status' TEXT, 'eingangsTag' NUMB, 'eingangsUhrzeit' NUMB, 'zusatztext' TEXT)")    

def createTB_Speisekarte():
    cur = con.cursor()
    #ist die Speisekaarte an sich so noetig??

#fuegt in die Datenabnk alle Tabellen ein
def createTB_All():
    createTB_Kunde()
    createTB_Restaurant()
    createTB_Item()
    createTB_Bestellung()
    createTB_Speisekarte()

#
#Kundenaccountverwaltungsmethoden
#

#fügt neuen Kunden in die Datenbank ohne zu überprüfen, ob dieser schon vorhanden ist
def insertNewKunde(username, password,vorname,nachname,adresse):
    cur = con.cursor()
    cur.executemany("INSERT INTO kunde VALUES(?,?,?,?,?)", username,password,vorname,nachname,adresse)

#eine Bestellung soll aufgegeben werden
def bestellungAufgeben():
    cur = con.cursor()

#Bestellverlauf soll so eingesehen werden koennen
def bestellungVorhanden():
    cur = con.cursor()
    


#
#Restaurantaccountverwaltungsmethoden
#

#fügt neues Restaurant in die Datenbank ein
def insertNewRestaurant(username, password, name, oeffnungszeiten, adresse):
    cur = con.cursor()

# ändert die Öffnungszeiten in der Datenbank zu Restaurant
def changeOeffnungszeiten(restaurantname, neueoeffnungszeiten):
    cur = con.cursor()

#vorallem für das an- & ablehnen gedacht
def changeBestellungStatus():
    cur = con.cursor()

#so sollen neue Speisen, Getraenke & co eingefügt werden können
def addItemKarte():
    cur = con.cursor()

#so sollen nicht mehr zu verkaufstehende Items wieder gelöscht werden
def removeItemKarte():
    cur = con.cursor()

            ########
            ##Idee##
            ########
    #Methode zum bearbeiten eines Items bspw. Preis


#
#Ende Methodendefinition
#

#Erstellt die Verbindung zur Datenbank
con = sqlite3.connect("Database.db")
cur = con.cursor()


#rufe folgende Methoden sofort auf
createTB_Kunde()


#beendet die Verbindung zur Datenbank
cur.close()
con.close()