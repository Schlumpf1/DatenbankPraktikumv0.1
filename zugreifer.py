import sqlite3
from module_item import *
from module_openingTime import *
####################
##____Methoden____##
####################

##aufbauende Methoden##
def createTB_Kunde():
    con = sqlite3.connect("Database.db")
    cur = con.cursor()
    cur.execute("CREATE TABLE 'kunde'('username' TEXT PRIMARY KEY , 'password' TEXT,'vorname' TEXT, 'nachname' TEXT,'adresse' TEXT, 'postleitzahl' INTEGER)")
    cur.close()
    con.close()

def createTB_Restaurant():
    con = sqlite3.connect("Database.db")
    cur = con.cursor()
    cur.execute("CREATE TABLE 'restaurant'('username' TEXT PRIMARY KEY , 'password' TEXT, 'name' TEXT, 'adresse' TEXT)")
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

def createTB_Bestellt_Items():
    con = sqlite3.connect("Database.db")
    cur = con.cursor()
    cur.execute("CREATE TABLE 'bestellt' ('bestell_id' INTEGER, 'itemId' INTEGER, 'anzahl' INTEGER, FOREIGN KEY (bestell_id) references bestellung(bestell_id), FOREIGN KEY (itemId) references items(itemId))") ;   
    cur.close()
    con.close()

def createTB_Speisekarte():
    con = sqlite3.connect("Database.db")
    cur = con.cursor()
    cur.execute("CREATE TABLE 'speisekarten'( 'speisekartenId' INTEGER PRIMARY KEY AUTOINCREMENT, 'restaurant_username' Text, FOREIGN KEY (restaurant_username) references restaurant(username))")
    cur.close()
    con.close()

    #ist die Speisekaarte an sich so noetig??

def createTB_OpeningTimes():
    con = sqlite3.connect('Database.db')
    cur = con.cursor()
    cur.execute("CREATE TABLE 'openingTimes'('id' INTEGER PRIMARY KEY AUTOINCREMENT,'restaurant_username' TEXT, 'day' TEXT, 'fromTime' Time,'toTime' Time, FOREIGN KEY(restaurant_username) REFERENCES restaurant(username))")
    cur.execute("")

#fuegt in die Datenabnk alle Tabellen ein
def createTB_All():
    createTB_Kunde()
    createTB_Restaurant()
    createTB_Item()
    createTB_Bestellung()
    createTB_Speisekarte()
    createTB_OpeningTimes()
    createTB_Bestellt_Items()

def insertExampleData_All():
    #Kunde
    insertNewKunde("MusterUser","Musterpasswort","Max", "Mustermann", "Musterstrasse 5",47057)
    restaurantId = insertNewRestaurant("firstRestaurant", "xyz123", "Musterrestaurant", "Musterwald 5")
    speisekartenId = insertNewSpeisekarte("firstRestaurant")
    #speisekartenId = 1
    print("SpeisekartenId",speisekartenId)
    insertNewItem(speisekartenId,"Das beste Essen",0,"Nicht vorhandene Beschreibung",None)
    insertNewItem(speisekartenId,"Das beste Essen1",0,"Nicht vorhandene Beschreibung",None)
    insertNewItem(speisekartenId,"Das beste Essen2",0,"Nicht vorhandene Beschreibung",None)
    insertNewItem(speisekartenId,"Das beste Essen3",0,"Nicht vorhandene Beschreibung",None)
    
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
def insertNewRestaurant(username, password, name, adresse):
    con = sqlite3.connect("Database.db")
    cur = con.cursor()
    cur.execute("INSERT INTO restaurant (username, password, name, adresse) VALUES(?,?,?,?)",
    (username, password, name, adresse))
    zwischenspeicher = cur.lastrowid
    cur.close()
    con.commit()
    con.close()
    return zwischenspeicher

def existUsername(username):
    con = sqlite3.connect("Database.db")
    cur = con.cursor()
    cur.execute("SELECT EXISTS ( SELECT username FROM restaurant WHERE username = '" +str(username)+"')")
    zwischenspeicher= cur.fetchone()[0]  
    cur.close()
    con.commit()
    con.close()
    return zwischenspeicher


def checkLogindata(username, password):
    con = sqlite3.connect("Database.db")
    cur = con.cursor()
    cur.execute("SELECT password FROM restaurant WHERE username = '" +str(username)+"'")
    zwischenspeicher = (cur.fetchone()[0] ==password)
    cur.close()
    con.commit()
    con.close()
    return zwischenspeicher

#fügt eine Speisekarte dem Restaurent hinzu
def insertNewSpeisekarte(username):
    con = sqlite3.connect("Database.db")
    cur = con.cursor()
    cur.execute("INSERT INTO speisekarten (restaurant_username) VALUES( '"+ username + "')")
    zwischenspeicher = cur.lastrowid
    cur.close()
    con.commit()
    con.close()
    return zwischenspeicher
    

# ändert die Öffnungszeiten in der Datenbank zu Restaurent
def addOpeningTimes(username, day, fromTime, toTime):
    con = sqlite3.connect("Database.db")
    cur = con.cursor()
    cur.execute("INSERT INTO openingTimes(restaurant_username, day, fromTime, toTime) VALUES(?,?,?,?)", (username, day,str(fromTime),str(toTime)))
    cur.close()
    con.commit()
    con.close()
def selectOpeningTimeGreaterThanFrom(username, day, fromTime):
    con = sqlite3.connect("Database.db")
    cur = con.cursor()
    cur.execute("SELECT * FROM openingTimes WHERE restaurant_username = '" + username + "' and day = '" +  day  + "' and fromTime < '" + str(fromTime) + "' and toTime >'" + str(fromTime) + "'");
    result = cur.fetchone()
    cur.close()
    con.commit()
    con.close()
    return result;

def selectOpeningTimesLessThanTo(username, day, toTime):
    con = sqlite3.connect("Database.db")
    cur = con.cursor()
    cur.execute("SELECT * FROM openingTimes WHERE restaurant_username ='" + username + "' and day = '" +  day  + "' and fromTime < '" + str(toTime) + "' and toTime > '" + str(toTime) + "'");
    result = cur.fetchone()
    cur.close()
    con.commit()
    con.close()
    return result;

def selectOpeningTimesIncludeOtherTimes(username, day, fromTime, toTime):
    con = sqlite3.connect("Database.db")
    cur = con.cursor()
    cur.execute("SELECT * FROM openingTimes WHERE restaurant_username ='" + username + "' and day = '" +  day  + "' and fromTime >= '" + str(fromTime) + "' and toTime <= '" + str(toTime) + "'");
    result = cur.fetchone()
    cur.close()
    con.commit()
    con.close()
    return result;

def getOpeningTimesForRestaurant(username):
    con = sqlite3.connect('Database.db')
    cur = con.cursor()
    result = cur.execute("SELECT * FROM openingTimes WHERE restaurant_username= '" +username + "'");  
    openingTimes = list()
    for x in result:
        openingTimes.append(OpeningTime(x[0], x[1], x[2], x[3], x[4]))
    cur.close()
    con.close()
    return openingTimes

def deleteOpeningTimeWithId(id):
    con = sqlite3.connect("Database.db")
    cur = con.cursor()
    cur.execute("DELETE FROM openingTimes WHERE id =" +str(id))
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
def getSpeisekarte(username):
    con = sqlite3.connect("Database.db")
    cur = con.cursor()
    cur.execute("SELECT speisekartenId FROM speisekarten WHERE restaurant_username= '" + username + "'")
    zwischenspeicher = cur.fetchone()[0]
    cur.close()
    con.close()
    return zwischenspeicher


def getItemsVonSpeisekarte(speisekartenId):
    con = sqlite3.connect("Database.db")
    cur = con.cursor()
    zwischenspeicher = cur.execute("SELECT * FROM items WHERE speisekartenId= "+str(speisekartenId))
    
    itemlist = list()
    
    for x in zwischenspeicher:
        itemlist.append(item(x[0],x[1],x[2],x[3],x[4],x[5]))
    cur.close()
    con.close()
    return itemlist
#    return [item(1,"Apfel","2,70","keine Beschreibung", "Kein Bild"), item(2,"Birne","2,80","keine Beschreibung", "Kein Bild")]

#so sollen neue Speisen, Getraenke & co eingefügt werden können
def insertNewItem(speisekartenId, name, preis, beschreibung, bild):
    con = sqlite3.connect("Database.db")
    cur = con.cursor()
    item = (speisekartenId ,name ,preis ,beschreibung)
    print(item)
    cur.execute("INSERT INTO items (speisekartenId, name, preis, beschreibung) VALUES( ? , ? , ? , ? )", item)  
    
    cur.close()
    con.commit()
    con.close()
    
#so sollen nicht mehr zu verkaufstehende Items wieder gelöscht werden
def removeItemFromSpeisekarte(itemId):
    con = sqlite3.connect("Database.db")
    cur = con.cursor()
    cur.execute("DELETE FROM items WHERE itemId =" +str(itemId))
    cur.close()
    con.commit()
    con.close()



#
#Ende Methodendefinition
#


