import sqlite3
from module_item import *
from module_openingTime import *
from module_postcodeitem import *
from module_order import *
from module_restaurant import *
from module_orderDetails import *
from module_orderedItem import * 
from module_customer import *
from externMethods import *
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
    cur.execute("CREATE TABLE 'items'('itemId' INTEGER PRIMARY KEY AUTOINCREMENT, 'speisekartenId' INTEGER, 'name' TEXT, 'preis' INTEGER, 'beschreibung' TEXT, 'bild' BLOB, 'category' text)")
    cur.close()
    con.close()

#Die Werte hier sind eventuell noch nicht passend gewählt
def createTB_Bestellung():
    con = sqlite3.connect("Database.db")
    cur = con.cursor()
    cur.execute("CREATE TABLE 'bestellung' ('bestell_id' INTEGER PRIMARY KEY AUTOINCREMENT,'status' TEXT, 'eingangsTag' DATE, 'eingangsUhrzeit' TIME, 'zusatztext' TEXT, 'restaurant_username' TEXT, 'customer_username' TEXT, FOREIGN KEY (restaurant_username) references restaurant(username), FOREIGN KEY (customer_username) references kunde(username))")    
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
    insertNewKunde("MusterUser","Musterpasswort","Max", "Mustermann", "Musterstrasse 5, 47057 Duisburg", 47057)
    insertNewKunde("MusterUser1", "password", "MixMuster", "Mustermann", "Musterstrasse 6, 50858 Köln", 50858)
    insertNewKunde("MusterUser2", "password2", "MuxMuster2", "Mustermann", "Musterstrasse 12, 40545 Stadt", 40545)
    restaurantId = insertNewRestaurant("firstRestaurant", "xyz123", "Musterrestaurant", "Musterwald 5")
    speisekartenId = insertNewSpeisekarte("firstRestaurant")
    #speisekartenId = 1
    print("SpeisekartenId",speisekartenId)
    itemId1 = insertNewItem(speisekartenId,"Das beste Essen",10,"Nicht vorhandene Beschreibung","Vorspeise")
    itemId2 = insertNewItem(speisekartenId,"Das beste Essen1",20,"Nicht vorhandene Beschreibung","Vorspeise")
    itemId3 = insertNewItem(speisekartenId,"Das beste Essen2",10,"Nicht vorhandene Beschreibung","Nachtisch")
    itemId4 = insertNewItem(speisekartenId,"Das beste Essen3",15,"Nicht vorhandene Beschreibung", "Hauptgericht")
    addPostcode(12345,"firstRestaurant")
    addPostcode(12346,"firstRestaurant")
    addPostcode(12347,"firstRestaurant")
    addPostcode(12348,"firstRestaurant")
    addOpeningTimes("firstRestaurant", "Montag",12,14)
    addOpeningTimes("firstRestaurant", "Montag",15,16)
    bestellungsId = addNewBestellung('In Bearbeitung', '20-12-2023', '08:00', 'text', 'firstRestaurant', 'MusterUser')
    addNewItemToBestellt(bestellungsId, itemId1, 1)
    addNewItemToBestellt(bestellungsId, itemId2, 2)
    addNewItemToBestellt(bestellungsId, itemId3, 1)
    addNewItemToBestellt(bestellungsId, itemId4, 3)
    bestellungsId = addNewBestellung('In Zubereitung', '20-12-2023', '08:00', 'text', 'firstRestaurant', 'MusterUser')
    addNewItemToBestellt(bestellungsId, itemId1, 1)
    addNewItemToBestellt(bestellungsId, itemId2, 2)
    bestellungsId = addNewBestellung('Abgeschlossen', '20-12-2023', '08:00', 'text', 'firstRestaurant', 'MusterUser')
    addNewItemToBestellt(bestellungsId, itemId1, 1)
    addNewItemToBestellt(bestellungsId, itemId3, 2)
    bestellungsId = addNewBestellung('Storniert', '20-12-2023', '08:00', 'text', 'firstRestaurant', 'MusterUser')
    addNewItemToBestellt(bestellungsId, itemId2, 1)
    addNewItemToBestellt(bestellungsId, itemId4, 2)
#Kundenaccountverwaltungsmethoden


#fügt neuen Kunden in die Datenbank ohne zu überprüfen, ob dieser schon vorhanden ist
def insertNewKunde(username, password,vorname,nachname,adresse, plz):
    con = sqlite3.connect("Database.db")
    cur = con.cursor()
    cur.execute("INSERT INTO kunde (username, password, vorname, nachname, adresse, postleitZahl) VALUES(?,?,?,?,?,?)",
    (username,password,vorname,nachname,adresse, plz))
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

def existPostcodeForRestaurant(postcode, restaurant_username):
    con = sqlite3.connect('Database.db')
    cur = con.cursor()
    result = cur.execute("SELECT * FROM postcodes WHERE restaurant_username= '" +restaurant_username + "'");  
    postcodes = list()
    for x in result:
        postcodes.append(postcodeitem(x[0], x[1], x[2]))
        
    returner = False
    for x in postcodes:
        print(str(x.postcode))
        if externMethods.compareNumbers(x.postcode, postcode):
            returner = True
    cur.close()
    con.close()
    if returner:
        print("It exists at minimum 1 Postcode (="+str(postcode)+") for the restaurant "+ restaurant_username)
    else:
        
        print("It does not exists a Postcode (="+str(postcode)+") for the restaurant "+ restaurant_username)
    return returner

def deletePostcodeWithId(postcodeId):
    con = sqlite3.connect("Database.db")
    cur = con.cursor()
    cur.execute("DELETE FROM postcodes WHERE id = "+str(postcodeId))
    cur.close()
    con.commit()
    con.close()
    print("Deletion of one postcode( "+str(postcodeId) +")")

def addNewBestellung (status, eingangsTag, eingangsUhrzeit, zusatztext, restaurant_username, customer_username):
    con = sqlite3.connect("Database.db")
    cur = con.cursor()
    cur.execute("INSERT INTO bestellung(status, eingangsTag, eingangsUhrzeit, zusatztext, restaurant_username, customer_username) VALUES(?,?,?,?,?,?)", (status,eingangsTag, eingangsUhrzeit, zusatztext, restaurant_username, customer_username))
    zwischenspeicher = cur.lastrowid
    cur.close()
    con.commit()
    con.close()
    return zwischenspeicher;

def addNewItemToBestellt(bestellungId, itemId, anzahl):
    con = sqlite3.connect("Database.db")
    cur = con.cursor()
    cur.execute("INSERT INTO bestellt(bestell_id, itemId, anzahl) VALUES(?,?, ?)", (bestellungId, itemId, anzahl))
    cur.close()
    con.commit()
    con.close()

# get new orders for restaurant
def getNewOrdersForRestaurant(username):
    con = sqlite3.connect("Database.db")
    cur = con.cursor()    
    result = cur.execute("SELECT * FROM bestellung where restaurant_username='" + username + "' and status='In Bearbeitung' order by eingangsTag asc , eingangsUhrzeit asc;");
    newOrders = list()
    for x in result:
        newOrders.append(order(x[0], x[1], x[2], x[3], x[4], x[5], x[6]))
    cur.close()
    con.close()
    return newOrders;

# get pending orders for restaurant
def getPendingOrdersForRestaurant(username):
    con = sqlite3.connect("Database.db")
    cur = con.cursor()    
    result = cur.execute("SELECT * FROM bestellung where restaurant_username='" + username + "' and status='In Zubereitung' order by eingangsTag asc , eingangsUhrzeit asc;");
    pendingOrders = list()
    for x in result:
        pendingOrders.append(order(x[0], x[1], x[2], x[3], x[4], x[5], x[6]))
    cur.close()
    con.close()
    return pendingOrders;

# get finished orders for restaurant
def getFinishedOrdersForRestaurant(username):
    con = sqlite3.connect("Database.db")
    cur = con.cursor()    
    result = cur.execute("SELECT * FROM bestellung where restaurant_username='" + username + "' and status='Abgeschlossen' order by eingangsTag asc , eingangsUhrzeit asc;");
    finishedOrders = list()
    for x in result:
        finishedOrders.append(order(x[0], x[1], x[2], x[3], x[4], x[5], x[6]))
    cur.close()
    con.close()
    return finishedOrders;    

# get canceled orders for restaurant
def getCanceledOrdersForRestaurant(username):
    con = sqlite3.connect("Database.db")
    cur = con.cursor()    
    result = cur.execute("SELECT * FROM bestellung where restaurant_username='" + username + "' and status='Storniert' order by eingangsTag asc , eingangsUhrzeit asc;");
    canceledOrders = list()
    for x in result:
        canceledOrders.append(order(x[0], x[1], x[2], x[3], x[4], x[5], x[6]))
    cur.close()
    con.close()
    return canceledOrders;  

# get new orders for customer
def getNewOrdersForCustomer(username):
    con = sqlite3.connect("Database.db")
    cur = con.cursor()    
    result = cur.execute("SELECT * FROM bestellung where customer_username='" + username + "' and status='In Bearbeitung' order by eingangsTag asc , eingangsUhrzeit asc;");
    newOrders = list()
    for x in result:
        newOrders.append(order(x[0], x[1], x[2], x[3], x[4], x[5], x[6]))
    cur.close()
    con.close()
    return newOrders;

# get pending orders for customer
def getPendingOrdersForCustomer(username):
    con = sqlite3.connect("Database.db")
    cur = con.cursor()    
    result = cur.execute("SELECT * FROM bestellung where customer_username='" + username + "' and status='In Zubereitung' order by eingangsTag asc , eingangsUhrzeit asc;");
    pendingOrders = list()
    for x in result:
        pendingOrders.append(order(x[0], x[1], x[2], x[3], x[4], x[5], x[6]))
    cur.close()
    con.close()
    return pendingOrders;

# get finished orders for customer
def getFinishedOrdersForCustomer(username):
    con = sqlite3.connect("Database.db")
    cur = con.cursor()    
    result = cur.execute("SELECT * FROM bestellung where customer_username='" + username + "' and status='Abgeschlossen' order by eingangsTag asc , eingangsUhrzeit asc;");
    finishedOrders = list()
    for x in result:
        finishedOrders.append(order(x[0], x[1], x[2], x[3], x[4], x[5], x[6]))
    cur.close()
    con.close()
    return finishedOrders; 

    # get canceled orders for customer
def getCanceledOrdersForCustomer(username):
    con = sqlite3.connect("Database.db")
    cur = con.cursor()    
    result = cur.execute("SELECT * FROM bestellung where customer_username='" + username + "' and status='Storniert' order by eingangsTag asc , eingangsUhrzeit asc;");
    canceledOrders = list()
    for x in result:
        canceledOrders.append(order(x[0], x[1], x[2], x[3], x[4], x[5], x[6]))
    cur.close()
    con.close()
    return canceledOrders;

def getRestaurantDetailsForOrder(orderId):
    con = sqlite3.connect("Database.db")
    cur = con.cursor()
    result = cur.execute("SELECT r.name, r.adresse FROM restaurant r, bestellung b where r.username=b.restaurant_username and b.bestell_id=" + str(orderId))
    restaurant1 = None
    for x in result:
        restaurant1 = restaurant(None, None, x[0], None, x[1], None)
    cur.close()
    con.close()
    return restaurant1;

def getCustomerDetailsForOrder(orderId):
    con = sqlite3.connect("Database.db")
    cur = con.cursor()
    result = cur.execute("SELECT k.vorname, k.nachname, k.adresse FROM kunde k, bestellung b where k.username=b.customer_username and b.bestell_id=" + str(orderId))
    customer1 = None
    for x in result:
        customer1 = customer(None, None, x[0], x[1], x[2])
    cur.close()
    con.close()
    return customer1;

def getOrderDetailsForOrder(orderId):
    con = sqlite3.connect("Database.db")
    cur = con.cursor()
    result = cur.execute("SELECT b.status, b.eingangsTag, b.eingangsUhrzeit, b.zusatzText FROM bestellung b where b.bestell_id=" + str(orderId))
    bestellung1 = None
    for x in result:
        bestellung1 = order(None, x[0], x[1], x[2], x[3], None, None)
    cur.close()
    con.close()
    return bestellung1;

def getItemDetailsForOdrer(orderId):
    con = sqlite3.connect("Database.db")
    cur = con.cursor()
    result = cur.execute("select i.name, i.preis, b.anzahl from items i inner join bestellt b on b.itemId = i.itemId where bestell_id=" + str(orderId))
    items = list()
    total = 0;
    for x in result:
        items.append(orderedItem(x[0], x[1], x[2], x[1] * x[2]))
        total += (x[1] * x[2])       
    cur.close()
    con.close()
    orderDetails1 = orderDetails(items, total)
    return orderDetails1;    



#vorallem für das an- & ablehnen gedacht
def changeBestellungStatus(orderId, status):
    con = sqlite3.connect("Database.db")
    cur = con.cursor()
    cur.execute("UPDATE bestellung set status='" + status + "' where bestell_id=" + str(orderId));
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
        itemlist.append(item(x[0],x[1],x[2],x[3],x[4],x[5], x[6]))
        localItem = itemlist[0]
    cur.close()
    con.close()
    print("GetItemById response with: "+ str(localItem))
    return localItem
#Speisekartenid zuveraendern macht hier keinen Sinn, da jedes Restaurant nur eine Speisekarte hat
def changeItemById(itemId, itemname, itempreis, itembeschreibung, category):
    con = sqlite3.connect("Database.db")
    cur = con.cursor()
    print("UPDATE items SET name = '"+itemname+ "' , preis = '"+str(itempreis) +"', beschreibung = '"+itembeschreibung + "', category = '" + category +"' WHERE itemId ='"+str(itemId)+"'")
    cur.execute("UPDATE items SET name = '"+itemname+ "' , preis = '"+str(itempreis) +"', beschreibung = '"+itembeschreibung + "', category = '" + category +"' WHERE itemId ='"+str(itemId)+"'")
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
        itemlist.append(item(x[0],x[1],x[2],x[3],x[4],x[5], x[6]))
    cur.close()
    con.close()
    print("Items (list.size= "+ str(len(itemlist))+") from Speisekarte "+ str(speisekartenId) +" requested")
    return itemlist
#    return [item(1,"Apfel","2,70","keine Beschreibung", "Kein Bild"), item(2,"Birne","2,80","keine Beschreibung", "Kein Bild")]

#so sollen neue Speisen, Getraenke & co eingefügt werden können
def insertNewItem(speisekartenId, name, preis, beschreibung, category ):
    con = sqlite3.connect("Database.db")
    cur = con.cursor()
    item = (speisekartenId ,name ,preis ,beschreibung, category)
    print(item)
    cur.execute("INSERT INTO items (speisekartenId, name, preis, beschreibung, category) VALUES( ? , ? , ? , ?, ?)", item)  
    zwischenSpeicher = cur.lastrowid;
    cur.close()
    con.commit()
    con.close()
    print("New Item inserted (name: "+name +")")
    return zwischenSpeicher;
    
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


