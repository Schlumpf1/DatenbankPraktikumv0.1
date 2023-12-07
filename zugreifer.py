import sqlite3
import os
from module_item import *

####################
##____Methoden____##
####################

##aufbauende Methoden##
def createTB_Kunde():
    con = sqlite3.connect("Database.db")
    cur = con.cursor()
    cur.execute("CREATE TABLE 'kunde'('kundenId'INTEGER PRIMARY KEY AUTOINCREMENT,'username' TEXT, 'password' TEXT,'vorname' TEXT, 'nachname' TEXT,'adresse' TEXT, 'postleitzahl' INTEGER)")
    cur.close()
    con.close()

def createTB_Restaurent():
    con = sqlite3.connect("Database.db")
    cur = con.cursor()
    cur.execute("CREATE TABLE 'restaurant'('restaurantId'INTEGER PRIMARY KEY AUTOINCREMENT,'username' TEXT, 'password' TEXT, 'name' TEXT,'oeffnungszeiten' TEXT, 'adresse' TEXT, 'postleitzahl' INTEGER)")
    cur.close()
    con.close()

#Die Werte hier sind eventuell noch nicht passend gewählt
def createTB_Item():
    con = sqlite3.connect("Database.db")
    cur = con.cursor()
    cur.execute("CREATE TABLE 'items'('itemId' INTEGER PRIMARY KEY AUTOINCREMENT, 'speisekartenId' INTEGER, 'name' TEXT, 'preis' INTEGER, 'beschreibung' TEXT, 'bild' BLOB)")
    cur.close()
    con.close()

#Die Werte hier sind eventuell noch nicht passend gewählt
def createTB_Bestellung():
    con = sqlite3.connect("Database.db")
    cur = con.cursor()
    cur.execute("CREATE TABLE 'bestellung' ('bestell_id' INTEGER PRIMARY KEY AUTOINCREMENT,'status' TEXT, 'eingangsTag' INTEGER, 'eingangsUhrzeit' INTEGER, 'zusatztext' TEXT)")    
    cur.close()
    con.close()

def createTB_Speisekarte():
    con = sqlite3.connect("Database.db")
    cur = con.cursor()
    cur.execute("CREATE TABLE 'speisekarten'( 'speisekartenId' INTEGER PRIMARY KEY AUTOINCREMENT, 'restaurantId' INTEGER)")
    cur.close()
    con.close()

    #ist die Speisekaarte an sich so noetig??

#fuegt in die Datenabnk alle Tabellen ein
def createTB_All():
    createTB_Kunde()
    createTB_Restaurent()
    createTB_Item()
    createTB_Bestellung()
    createTB_Speisekarte()


def insertExampleData_All():
    #Kunde
    insertNewKunde("MusterUser","Musterpasswort","Max", "Mustermann", "Musterstrasse 5",47057)
    restaurantId = insertNewRestaurent("firstRestaurent", "xyz123", "Musterrestaurant", "unbekannt", "Musterwald 5",47057)
    print("restaurantid",restaurantId)
    speisekartenId = insertNewSpeisekarte(restaurantId)
    #speisekartenId = 1
    print("SpeisekartenId",speisekartenId)
    insertNewItem(speisekartenId,"Das beste Essen",0,"Nicht vorhandene Beschreibung",None)
    
#
#Kundenaccountverwaltungsmethoden


#fügt neuen Kunden in die Datenbank ohne zu überprüfen, ob dieser schon vorhanden ist
def insertNewKunde(username, password,vorname,nachname,adresse,postleitzahl):
    con = sqlite3.connect("Database.db")
    cur = con.cursor()
    cur.execute("INSERT INTO kunde (username, password, vorname, nachname, adresse, postleitzahl) VALUES(?,?,?,?,?,?)",
    (username,password,vorname,nachname,adresse,postleitzahl))
    zwischenspeicher = cur.lastrowid
    cur.close()
    con.commit()
    con.close()
    return zwischenspeicher

#eine Bestellung soll aufgegeben werden
def bestellungAufgeben():
    con = sqlite3.connect("Database.db")
    cur = con.cursor()
    cur.close()
    con.commit()
    con.close()

#Bestellverlauf soll so eingesehen werden koennen
def bestellungVorhanden():
    con = sqlite3.connect("Database.db")
    cur = con.cursor()
    cur.close()
    con.close()


#
#restaurantaccountverwaltungsmethoden
#

#fügt neues restaurant in die Datenbank ein
def insertNewRestaurent(username, password, name, oeffnungszeiten, adresse,postleitzahl):
    con = sqlite3.connect("Database.db")
    cur = con.cursor()
    cur.execute("INSERT INTO restaurant (username, password, name, oeffnungszeiten, adresse, postleitzahl) VALUES(?,?,?,?,?,?)",
    (username, password, name, oeffnungszeiten, adresse, postleitzahl))
    zwischenspeicher = cur.lastrowid
    cur.close()
    con.commit()
    con.close()
    return zwischenspeicher

#fügt eine Speisekarte dem Restaurent hinzu
def insertNewSpeisekarte(restaurantId):
    con = sqlite3.connect("Database.db")
    cur = con.cursor()
    cur.execute("INSERT INTO speisekarten (restaurantId) VALUES( "+str(restaurantId)+ ")")
    zwischenspeicher = cur.lastrowid
    cur.close()
    con.commit()
    con.close()
    return zwischenspeicher
    

# ändert die Öffnungszeiten in der Datenbank zu Restaurent
def changeOeffnungszeiten(restaurantname, neueoeffnungszeiten):
    con = sqlite3.connect("Database.db")
    cur = con.cursor()
    cur.close()
    con.commit()
    con.close()

#vorallem für das an- & ablehnen gedacht
def changeBestellungStatus():
    con = sqlite3.connect("Database.db")
    cur = con.cursor()
    cur.close()
    con.commit()
    con.close()

#gibt alle Items von dem restaurant wieder
def getSpeisekarte(restaurantId):
    con = sqlite3.connect("Database.db")
    cur = con.cursor()
    cur.execute("SELECT restaurantId FROM speisekarten WHERE restaurantId= "+str(restaurantId))
    zwischenspeicher = cur.fetchone()
    cur.close()
    con.close()
    return zwischenspeicher


def getItemsVonSpeisekarte(speisekartenId):
    con = sqlite3.connect("Database.db")
    cur = con.cursor()
    zwischenspeicher = cur.execute("SELECT * FROM items WHERE speisekartenId= ?",speisekartenId)
    
    itemlist = list()
    
    for x in zwischenspeicher:
        itemlist.append(item(x[0],x[1],x[2],x[3],x[4],x[5]))
    cur.close()
    con.close()
    return itemlist
#    return [item(1,"Apfel","2,70","keine Beschreibung", "Kein Bild"), item(2,"Birne","2,80","keine Beschreibung", "Kein Bild")]

#so sollen neue Speisen, Getraenke & co eingefügt werden können
def insertNewItem(speisekartenId,name,preis,beschreibung,bild):
    con = sqlite3.connect("Database.db")
    cur = con.cursor()
    cur.execute("INSERT INTO items (speisekartenId,name,preis,beschreibung,bild) VALUES(?,?,?,?,?)",(speisekartenId,name,preis,beschreibung,bild))
    cur.close()
    con.commit()
    con.close()
    
#so sollen nicht mehr zu verkaufstehende Items wieder gelöscht werden
def removeItemKarte():
    con = sqlite3.connect("Database.db")
    cur = con.cursor()
    cur.close()
    con.commit()
    con.close()



#
#Ende Methodendefinition
#

os.remove("Database.db")
#Erstellt die Verbindung zur Datenbank
con = sqlite3.connect("Database.db")



#rufe folgende Methoden sofort auf
createTB_All()
insertExampleData_All()
#beendet die Verbindung zur Datenbank
#cur.close()
con.close()