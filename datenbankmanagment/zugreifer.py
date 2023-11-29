import sqlite3



#____Methoden____


def createTB_Kunde():
    cur = con.cursor()
    cur.execute("CREATE TABLE 'kunde'('username' TEXT, 'password' TEXT,'vorname' TEXT, 'nachname' TEXT,'adresse' TEXT)")

def createTB_Restaurant():
    cur = con.cursor()
    cur.execute("CREATE TABLE 'restaurant'('username' TEXT, 'password' TEXT, 'name' TEXT,'oeffnungszeiten' TEXT, 'adresse' TEXT)")

def createTB_Item():
    cur = con.cursor()
    cur.execute("CREATE TABLE 'item'('name' TEXT, 'preis')")

def createTB_Bestellung():
    cur = con.cursor()
    
def createTB_Speisekarte():
    cur = con.cursor()

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


#
#Restaurantaccountverwaltungsmethoden
#

#fügt neues Restaurant in die Datenbank ein
def insertNewRestaurant(username, password, name, oeffnungszeiten, adresse):
    cur = con.cursor()

# ändert die Öffnungszeiten in der Datenbank zu Restaurant
def changeOeffnungszeiten(restaurantname, neueoeffnungszeiten):
    cur = con.cursor()


#Erstellt die Verbindung zur Datenbank
con = sqlite3.connect("Database.db")

#rufe folgende Methoden sofort auf
createTB_Kunde()