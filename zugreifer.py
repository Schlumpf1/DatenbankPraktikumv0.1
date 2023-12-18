import sqlite3
from module_item import *
from module_openingTime import *
from module_postcodeitem import *
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
    cur.execute("CREATE TABLE 'bestellung' ('bestell_id' INTEGER PRIMARY KEY AUTOINCREMENT,'status' TEXT, 'eingangsTag' INTEGER, 'eingangsUhrzeit' INTEGER, 'zusatztext' TEXT, 'restaurant_username' TEXT, 'customer_username' TEXT, FOREIGN KEY (restaurant_username) references restaurant(username), FOREIGN KEY (customer_username) references kunde(username))")    
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
    cur.close()
    con.close()

def createTB_Postcode():
    con = sqlite3.connect('Database.db')
    cur = con.cursor()
    cur.execute("CREATE TABLE 'postcodes'('id' INTEGER PRIMARY KEY AUTOINCREMENT,'restaurant_username' TEXT, postcode INTEGER, FOREIGN KEY(restaurant_username) REFERENCES restaurant(username))")
    cur.close()
    con.close()


#fuegt in die Datenabnk alle Tabellen ein
def createTB_All():
    createTB_Kunde()
    createTB_Restaurant()
    createTB_Item()
    createTB_Bestellung()
    createTB_Speisekarte()
    createTB_OpeningTimes()
    createTB_Bestellt_Items()
    createTB_Postcode()

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
    addPostcode(12345,"firstRestaurant")
    addPostcode(12346,"firstRestaurant")
    addPostcode(12347,"firstRestaurant")
    addPostcode(12348,"firstRestaurant")
    addOpeningTimes("firstRestaurant", "Montag",12,14)
    addOpeningTimes("firstRestaurant", "Montag",15,16)
    
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
    print("Inserted new Customer with the username "+username)
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

#fügt neues Restaurant in die Datenbank ein
def insertNewRestaurant(username, password, name, adresse):
    con = sqlite3.connect("Database.db")
    cur = con.cursor()
    cur.execute("INSERT INTO restaurant (username, password, name, adresse) VALUES(?,?,?,?)",
    (username, password, name, adresse))
    zwischenspeicher = cur.lastrowid
    cur.close()
    con.commit()
    con.close()
    print("Inserted new Restaurant with the username "+username)
    return zwischenspeicher

def existUsername(username):
    con = sqlite3.connect("Database.db")
    cur = con.cursor()
    cur.execute("SELECT EXISTS ( SELECT username FROM restaurant WHERE username = '" +str(username)+"')")
    zwischenspeicher= cur.fetchone()[0]  
    cur.close()
    con.commit()
    con.close()
    print("Request if Restaurant username "+username+" already exists: "+str(zwischenspeicher))
    return zwischenspeicher

def existsCustomersUsername(username):
    con = sqlite3.connect('Database.db')
    cur = con.cursor()
    cur.execute("SELECT EXISTS (SELECT username FROM kunde WHERE username = '" + username + "')")
    zwischenspeicher= cur.fetchone()[0]  
    cur.close()
    con.commit()
    con.close()
    print("Request if Customer username "+username+" already exists: "+str(zwischenspeicher))
    return zwischenspeicher

def checkLogindata(username, password):
    con = sqlite3.connect("Database.db")
    cur = con.cursor()
    cur.execute("SELECT password FROM restaurant WHERE username = '" +str(username)+"'")
    zwischenspeicher = (cur.fetchone()[0] ==password)
    cur.close()
    con.commit()
    con.close()
    print("checkLoginData for Restaurant username: "+username +" password: "+password + "Sucess: "+str(zwischenspeicher))
    return zwischenspeicher

def checkCustomerLoginData(username, password):
    con = sqlite3.connect('Database.db')    
    cur = con.cursor()
    cur.execute("SELECT password FROM kunde WHERE username = '" + username +"'")
    zwischenspeicher = (cur.fetchone()[0] ==password)
    cur.close()
    con.commit()
    con.close()
    print("checkLoginData for Customer username: "+username +" password: "+password + "Sucess: "+str(zwischenspeicher))
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
    print("New Speisekarte for the restaurant with username: "+username )
    return zwischenspeicher
    

# ändert die Öffnungszeiten in der Datenbank zu Restaurent
def addOpeningTimes(username, day, fromTime, toTime):
    con = sqlite3.connect("Database.db")
    cur = con.cursor()
    cur.execute("INSERT INTO openingTimes(restaurant_username, day, fromTime, toTime) VALUES(?,?,?,?)", (username, day,str(fromTime),str(toTime)))
    cur.close()
    con.commit()
    con.close()
    print("Inserted OpeningTimes for the restaurant with username: "+username)
    
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
    result = cur.execute("SELECT * FROM openingTimes WHERE restaurant_username= '" +username + "' ORDER BY fromTime ASC");  
    openingTimes = list()
    for x in result:
        openingTimes.append(OpeningTime(x[0], x[1], x[2], x[3], x[4]))
    cur.close()
    con.close()
    print("Found "+str(len(openingTimes)) +" openingtime(s) for restaurant with username: "+ username )
    return openingTimes

def deleteOpeningTimeWithId(id):
    con = sqlite3.connect("Database.db")
    cur = con.cursor()
    cur.execute("DELETE FROM openingTimes WHERE id =" +str(id))
    cur.close()
    con.commit()
    con.close()
    print("Deletion of one openingtime")
    
def addPostcode(postcode, restaurant_username):
    con = sqlite3.connect("Database.db")
    cur = con.cursor()
    cur.execute("INSERT INTO postcodes(restaurant_username, postcode) VALUES(?,?)", (restaurant_username,str(postcode)))
    cur.close()
    con.commit()
    con.close()
    print("Inserted Poctcode( "+str(postcode) +" for the restaurant with username: "+restaurant_username)


def getPostcodesForRestaurant(restaurant_username):
    con = sqlite3.connect('Database.db')
    cur = con.cursor()
    result = cur.execute("SELECT * FROM postcodes WHERE restaurant_username= '" +restaurant_username + "'");  
    postcodes = list()
    for x in result:
        postcodes.append(postcodeitem(x[0], x[1], x[2]))
    cur.close()
    con.close()
    print("Found "+str(len(postcodes)) +" postcode(s) for restaurant with username: "+ restaurant_username)
    return postcodes

def deletePostcodeWithId(postcodeId):
    con = sqlite3.connect("Database.db")
    cur = con.cursor()
    cur.execute("DELETE FROM postcodes WHERE id = "+str(postcodeId))
    cur.close()
    con.commit()
    con.close()
    print("Deletion of one postcode( "+str(postcodeId) +")")

#vorallem für das an- & ablehnen gedacht
def changeBestellungStatus():
    con = sqlite3.connect("Database.db")
    cur = con.cursor()
    cur.close()
    con.commit()
    con.close()
    print("Bestellung changed")

#gibt alle Items von dem restaurant wieder
def getSpeisekarte(username):
    con = sqlite3.connect("Database.db")
    cur = con.cursor()
    cur.execute("SELECT speisekartenId FROM speisekarten WHERE restaurant_username= '" + username + "'")
    zwischenspeicher = cur.fetchone()[0]
    cur.close()
    con.close()
    print("Speisekarte from restaurant_username: "+ username +" requested")
    return zwischenspeicher

def getItemById(itemId):
    con = sqlite3.connect("Database.db")
    cur = con.cursor()
    zwischenspeicher = cur.execute("SELECT * FROM items WHERE itemId= "+str(itemId))
    itemlist = list()
    for x in zwischenspeicher:
        itemlist.append(item(x[0],x[1],x[2],x[3],x[4],x[5]))
        localItem = itemlist[0]
    cur.close()
    con.close()
    print("GetItemById response with: "+ str(localItem))
    return localItem
#Speisekartenid zuveraendern macht hier keinen Sinn, da jedes Restaurant nur eine Speisekarte hat
def changeItemById(itemId, itemname, itempreis, itembeschreibung):
    con = sqlite3.connect("Database.db")
    cur = con.cursor()
    print("UPDATE items SET name = '"+itemname+ "' , preis = '"+str(itempreis) +"', beschreibung = '"+itembeschreibung +"' WHERE itemId ='"+str(itemId)+"'")
    cur.execute("UPDATE items SET name = '"+itemname+ "' , preis = '"+str(itempreis) +"', beschreibung = '"+itembeschreibung +"' WHERE itemId ='"+str(itemId)+"'")
    cur.close()
    con.commit()
    con.close()
    print("Item(Id: "+str(itemId)+") was changed [SQL:UPDATED]")
    


def getItemsVonSpeisekarte(speisekartenId):
    con = sqlite3.connect("Database.db")
    cur = con.cursor()
    zwischenspeicher = cur.execute("SELECT * FROM items WHERE speisekartenId= "+str(speisekartenId))
    
    itemlist = list()
    
    for x in zwischenspeicher:
        itemlist.append(item(x[0],x[1],x[2],x[3],x[4],x[5]))
    cur.close()
    con.close()
    print("Items (list.size= "+ str(len(itemlist))+") from Speisekarte "+ str(speisekartenId) +" requested")
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
    print("New Item inserted (name: "+name +")")
    
#so sollen nicht mehr zu verkaufstehende Items wieder gelöscht werden
def removeItemFromSpeisekarte(itemId):
    con = sqlite3.connect("Database.db")
    cur = con.cursor()
    cur.execute("DELETE FROM items WHERE itemId =" +str(itemId))
    cur.close()
    con.commit()
    con.close()
    print("Removed Item")


#
#Ende Methodendefinition
#


