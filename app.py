from flask import Flask, render_template, render_template, redirect, request, jsonify, session, flash
import zugreifer
from module_openingTime import *
import os
import re
from datetime import date, datetime


app = Flask(__name__)
app.secret_key = 'BAD_SECRET_KEY'


@app.route("/")
def home():
    return render_template("startpage.html")



@app.route("/initTables")
def initTables():
    os.remove("Database.db")
    zugreifer.createTB_All()
    zugreifer.insertExampleData_All()
    session.clear()
    return redirect("/restaurant")

@app.route("/home")
def home1():
    return "Hallo"

@app.route("/restaurant")
def restaurant():
    if(not 'restaurant_username' in session):
        return render_template('restaurant_login.html')
    
    name = zugreifer.getRestaurantName(session['restaurant_username'])    
    return render_template('speisekarte.html', items=zugreifer.getItemsVonSpeisekarte(zugreifer.getSpeisekarte(session['restaurant_username'])), name=name)

@app.route("/restaurant/logout")
def restaurant_logout():
    session.pop("restaurant_username", None)
    return render_template('startpage.html')

@app.route("/customer/logout")
def customer_logout():
    session.pop("customer_username", None)
    session.pop('chosen_restaurant', None)
    return render_template('startpage.html')

@app.route('/restaurant/bestellungen/neu')
def newOrders():
    if(not 'restaurant_username' in session):
        return render_template('restaurant_login.html')
    username = session['restaurant_username']
    newOrders = zugreifer.getNewOrdersForRestaurant(username)
    return render_template('restaurant_new_orders.html', newOrders = newOrders)


@app.route('/restaurant/new_order_details/<int:orderId>', methods=['POST'])
def newOrderDetails(orderId):
    customer = zugreifer.getCustomerDetailsForOrder(orderId)
    bestellung = zugreifer.getOrderDetailsForOrder(orderId)
    orderDetails = zugreifer.getItemDetailsForOdrer(orderId)
    return render_template('restaurant_new_order_details.html', orderId = orderId, customer = customer, bestellung = bestellung, orderDetails = orderDetails)


@app.route('/restaurant/bestellungen')
def restaurantOrders():
    if(not 'restaurant_username' in session):
        return render_template('restaurant_login.html')
    username = session['restaurant_username']
    openOrders = zugreifer.getNewOrdersForRestaurant(username)
    pendingOrders = zugreifer.getPendingOrdersForRestaurant(username)
    finishedOrders = zugreifer.getFinishedOrdersForRestaurant(username)
    canceledOrders = zugreifer.getCanceledOrdersForRestaurant(username)
    return render_template('restaurant_orders.html',openOrders = openOrders, pendingOrders = pendingOrders, finishedOrders = finishedOrders, canceledOrders = canceledOrders)    

@app.route('/restaurant/order_details/<int:orderId>', methods=['POST'])
def restaurantOrderDetails(orderId):
    customer = zugreifer.getCustomerDetailsForOrder(orderId)
    bestellung = zugreifer.getOrderDetailsForOrder(orderId)
    orderDetails = zugreifer.getItemDetailsForOdrer(orderId)
    return render_template('restaurant_order_details.html', orderId = orderId, customer = customer, bestellung = bestellung, orderDetails = orderDetails)

@app.route('/restaurant/bestellungen/<int:orderId>', methods=['POST'])
def setOrderAsDone(orderId):
    zugreifer.changeBestellungStatus(orderId, "Abgeschlossen")
    return restaurantOrderDetails(orderId)

@app.route('/restaurant/bestellungen/accept/<int:orderId>', methods=['POST'])
def setOrderAsAccepted(orderId):
    zugreifer.changeBestellungStatus(orderId, "In Zubereitung")
    return restaurantOrderDetails(orderId)

@app.route('/restaurant/bestellungen/cancel/<int:orderId>', methods=['POST'])
def setOrderAsCancelled(orderId):
    zugreifer.changeBestellungStatus(orderId, "Storniert")
    return restaurantOrderDetails(orderId)


@app.route("/customer/bestellungen")
def customerOrders():
    if(not 'customer_username' in session):
        return render_template('customer_login.html')
    username = session['customer_username'] 
    newOrders = zugreifer.getNewOrdersForCustomer(username)
    pendingOrders = zugreifer.getPendingOrdersForCustomer(username)
    finishedOrders = zugreifer.getFinishedOrdersForCustomer(username)
    canceledOrders = zugreifer.getCanceledOrdersForCustomer(username)
    return render_template('customer_orders.html', newOrders = newOrders, pendingOrders = pendingOrders, finishedOrders = finishedOrders, canceledOrders = canceledOrders)   

@app.route('/customer/order_details/<int:orderId>', methods=['POST'])
def customerOrderDetails(orderId):
    restaurant = zugreifer.getRestaurantDetailsForOrder(orderId)
    bestellung = zugreifer.getOrderDetailsForOrder(orderId)
    orderDetails = zugreifer.getItemDetailsForOdrer(orderId)
    return render_template('customer_order_details.html', orderId = orderId, restaurant = restaurant, bestellung = bestellung, orderDetails = orderDetails)


@app.route("/restaurant/delete_Item/<int:itemId>", methods=['POST'])
def delete_Item(itemId):
    if(not 'restaurant_username' in session):
        return render_template('restaurant_login.html')
    zugreifer.removeItemFromSpeisekarte(itemId)
    return redirect("/restaurant")

@app.route("/restaurant/newItem")
def newItem():
    if(not 'restaurant_username' in session):
        return render_template('restaurant_login.html')
    return render_template('restaurant_newItem.html')
    
@app.route("/restaurant/newItem/safe", methods=['POST'])
def newItem_safe():
    if(not 'restaurant_username' in session):
        return render_template('restaurant_login.html')
    username = session['restaurant_username']
    itemName = request.form['itemname']
    itemPreis = request.form['itempreis']
    itemBeschreibung = request.form['itembeschreibung']
    itemBild = request.form['itembild']
    category = request.form['category']
    print(itemBild)
    speisekartenId = zugreifer.getSpeisekarte(username)
    zugreifer.insertNewItem(speisekartenId,itemName,itemPreis,itemBeschreibung,category)
    return redirect("/restaurant")

@app.route("/restaurant/changeItem/<int:item_id>", methods=['POST','GET'])
def changeItem(item_id: int):
    if(not 'restaurant_username' in session):
        print(item_id)
        return render_template('restaurant_login.html')
    print(zugreifer.getItemById(item_id))
    if request.method == 'POST':
        itemName = request.form['itemname']
        itemPreis = request.form['itempreis']
        itemBeschreibung = request.form['itembeschreibung']
        itemBild = request.form['itembild']
        category = request.form['category']
        zugreifer.changeItemById(item_id,itemName,itemPreis,itemBeschreibung, category)
        print("changeItem(): Item(Id:"+str(item_id)+") changed")
        return redirect("/restaurant")
    else:
        item = zugreifer.getItemById(item_id)
        return render_template("restaurant_changeItem.html", item = item)


@app.route("/restaurant/openingTime")
def openingTime():
    if(not 'restaurant_username' in session):
        return render_template('restaurant_login.html')
    list = zugreifer.getOpeningTimesForRestaurant(session['restaurant_username'])
    mondaysList = []
    tuesdayList = []
    wednesdayList = []
    thursdayList = []
    fridayList = []
    saturdayList = []
    sundayList = []
    for openingTime in list:
        if(openingTime.day == 'Montag'):
            mondaysList.append(openingTime)
        if(openingTime.day == 'Dienstag'):
            tuesdayList.append(openingTime)
        if(openingTime.day == 'Mittwoch'):
            wednesdayList.append(openingTime)
        if(openingTime.day == 'Donnerstag'):
            thursdayList.append(openingTime)
        if(openingTime.day == 'Freitag'):
            fridayList.append(openingTime)
        if(openingTime.day == 'Samstag'):
            saturdayList.append(openingTime)
        if(openingTime.day == 'Sonntag'):
            sundayList.append(openingTime)    
    return render_template('openingTime.html',
        mondaysList=mondaysList,
        tuesdayList=tuesdayList,
        wednesdayList=wednesdayList,
        thursdayList=thursdayList, 
        fridayList=fridayList, 
        saturdayList=saturdayList, 
        sundayList=sundayList)


@app.route("/restaurant/openingTime/add", methods=['POST'])
def addOpeningTime():
    if(not 'restaurant_username' in session):
        return render_template('restaurant_login.html')
    username  = session['restaurant_username']
    day = request.form['day']
    fromTime = request.form['from']
    toTime = request.form['to']
    errors = [];
    list = zugreifer.getOpeningTimesForRestaurant(username)
    mondaysList = []
    tuesdayList = []
    wednesdayList = []
    thursdayList = []
    fridayList = []
    saturdayList = []
    sundayList = []
    for openingTime in list:
        if(openingTime.day == 'Montag'):
            mondaysList.append(openingTime)
        if(openingTime.day == 'Dienstag'):
            tuesdayList.append(openingTime)
        if(openingTime.day == 'Mittwoch'):
            wednesdayList.append(openingTime)
        if(openingTime.day == 'Donnerstag'):
            thursdayList.append(openingTime)
        if(openingTime.day == 'Freitag'):
            fridayList.append(openingTime)
        if(openingTime.day == 'Samstag'):
            saturdayList.append(openingTime)
        if(openingTime.day == 'Sonntag'):
            sundayList.append(openingTime)  

    if(not re.match("\d\d:\d\d", fromTime)):
        errors.append("Von soll das Format HH:MM haben")
        return render_template('openingTime.html',
         errors=errors,
         mondaysList = mondaysList,
         tuesdayList = tuesdayList,
         wednesdayList = wednesdayList,
         thursdayList = thursdayList,
         fridayList = fridayList,
         saturdayList = saturdayList,
         sundayList = sundayList)  

    if(not re.match("\d\d:\d\d", toTime)):
        errors.append("Bis soll das Format HH:MM haben")
        return render_template('openingTime.html',
         errors=errors,
         mondaysList = mondaysList,
         tuesdayList = tuesdayList,
         wednesdayList = wednesdayList,
         thursdayList = thursdayList,
         fridayList = fridayList,
         saturdayList = saturdayList,
         sundayList = sundayList)  

    time_object_from = datetime.strptime(fromTime, '%H:%M').time()
    time_object_to = datetime.strptime(toTime, '%H:%M').time();
    if(time_object_from > time_object_to):
        errors.append('Von soll kleiner als Bis sein')

    res1 = zugreifer.selectOpeningTimeGreaterThanFrom(username, day, time_object_from)
    res2 = zugreifer.selectOpeningTimesLessThanTo(username, day, time_object_to)
    res3 = zugreifer.selectOpeningTimesIncludeOtherTimes(username, day, time_object_from, time_object_to);

    if((res1 is not None) or (res2 is not None) or (res3 is not None)):
        errors.append("Die Zeiten dürfen sich nicht überlappen")
    
    if(len(errors) > 0):
        return render_template('openingTime.html',
         errors=errors,
         mondaysList = mondaysList,
         tuesdayList = tuesdayList,
         wednesdayList = wednesdayList,
         thursdayList = thursdayList,
         fridayList = fridayList,
         saturdayList = saturdayList,
         sundayList = sundayList)     
    else:   
        zugreifer.addOpeningTimes(username, day, time_object_from, time_object_to)
        return redirect('/restaurant/openingTime')


@app.route("/restaurant/openingTime/delete-day/<int:id>", methods=['POST'])
def delete_day(id):
    if(not 'restaurant_username' in session):
        return render_template('restaurant_login.html')
    zugreifer.deleteOpeningTimeWithId(id)
    return redirect("/restaurant/openingTime")

@app.route("/restaurant/login", methods =['POST', 'GET'])
def restaurant_login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        #versuch login auszuführen
        if zugreifer.existUsername(username):
            if zugreifer.checkLogindata(username,password):
                session['restaurant_username'] = username;
                return redirect("/restaurant")
            else:
                message = "Benutzername oder Passwort ist falsch. Bitte versuchen Sie erneut."
                return render_template('restaurant_login.html', message = message)
        else:
            message = "Benutzername existiert nicht."
            return render_template('restaurant_login.html', message = message)
    #elif request.method == 'GET':
    return render_template('restaurant_login.html')
    
@app.route("/restaurant/registrieren", methods =['POST', 'GET'])
def restaurant_register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        passwordControll = request.form['passwordControll']
        restaurantName = request.form['restaurantName']
        street = request.form['street']
        houseNumber = request.form['houseNumber']
        plz = request.form['zipcode']
        city = request.form['city']
        address = street + " " + houseNumber + ", " + plz + " " + city
        if password == passwordControll:
            #usernamedopplung pruefen
            if zugreifer.existUsername(username) == False:
                zugreifer.insertNewRestaurant(username, password, restaurantName, address)
                zugreifer.insertNewSpeisekarte(username)
                session['restaurant_username'] = username
                return redirect('/restaurant')
            else:
                return render_template('restaurant_register.html',message="Benutzername schon vergeben!")
        else:
            message = "Beide Passworts sollen gleich sein!"   
            return render_template('restaurant_register.html', message = message)
    #Wenn Methode != POST, password != passwordControll
    return render_template('restaurant_register.html',message = "")

@app.route("/restaurant/postcodes", methods =['POST', 'GET'])
def restaurant_postcodes():
    if(not 'restaurant_username' in session):
        return render_template('restaurant_login.html')
    username = session['restaurant_username']
    return render_template("restaurant_postcodes.html" , postcodes= zugreifer.getPostcodesForRestaurant(username), message = None)

@app.route("/restaurant/postcodes/delete_Postcode/<int:postcodeId>", methods=['POST'])
def delete_Postcode(postcodeId):
    if(not 'restaurant_username' in session):
        return render_template('restaurant_login.html')
    zugreifer.deletePostcodeWithId(postcodeId)
    return redirect("/restaurant/postcodes")

@app.route("/restaurant/postcode/add_Postcode", methods=['POST'])
def add_Postcode():
    if(not 'restaurant_username' in session):
        return render_template('restaurant_login.html')
    postcode = request.form['postcode_To_Add']
    username = session['restaurant_username']
    messages = list()
    if(len(postcode)==5):
        if zugreifer.existPostcodeForRestaurant(postcode, username):
            messages.append("Diese Postleitzahl beliefern Sie bereits")
            return render_template("restaurant_postcodes.html" , postcodes= zugreifer.getPostcodesForRestaurant(username), messages =messages )
        else:
            zugreifer.addPostcode(postcode,username)
    else:
        messages.append("Die Postleitzahl muss genau 5 Zeichen lang sein")
        return render_template("restaurant_postcodes.html" , postcodes= zugreifer.getPostcodesForRestaurant(username), messages = messages )
    return redirect("/restaurant/postcodes")

    
    print(itemBild)
    speisekartenId = zugreifer.getSpeisekarte(username)
    zugreifer.insertNewItem(speisekartenId,itemName,itemPreis,itemBeschreibung,category)
    return redirect("/restaurant")

@app.route("/customer/login", methods =['POST', 'GET'])
def customer_login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        #versuch login auszuführen
        if zugreifer.existsCustomersUsername(username):
            if zugreifer.checkCustomerLoginData(username,password):
                session['customer_username'] = username;
                return redirect("/customer")
            else:
                message = "Passwort ist falsch"
                return render_template('customer_login.html', message = message)
        else:
            message = "Benutzername existiert nicht"
            return render_template('customer_login.html', message = message)
    #elif request.method == 'GET':
    return render_template('customer_login.html')

@app.route("/customer/registrieren", methods =['POST', 'GET'])
def customer_register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        passwordControll = request.form['passwordControll']
        firstName = request.form['firstName']
        lastName = request.form['lastName']
        street = request.form['street']
        houseNumber = request.form['houseNumber']
        plz = request.form['plz']
        city = request.form['city']
        address = street + " " + houseNumber + ", " + plz + " " + city
        if password == passwordControll:
            #usernamedopplung pruefen
            print(zugreifer.existsCustomersUsername(username))
            if zugreifer.existsCustomersUsername(username) == 0:
                zugreifer.insertNewKunde(username, password,firstName, lastName, address, plz)
                session['customer_username'] = username
                return redirect('/customer')
            else:
                return render_template('customer_register.html',message="Benutzername schon vergeben!")
        else:
            return render_template('customer_register.html',message="Beide Passworts sollen gleich sein!")
    #Wenn Methode != POST, password != passwordControll
    return render_template('customer_register.html',message = "")


@app.route("/customer")
def customer():
    if(not 'customer_username' in session):
        return redirect('/customer/login')
    username = session['customer_username']
    customer = zugreifer.getDetailsForCustomer(username)
    time = datetime.now().strftime("%H:%M:%S")
    day = datetime.now().strftime("%A")
    if day == 'Monday':
        day = 'Montag'
    elif day == 'Tuesday':
        day = 'Dienstag'
    elif day == 'Wednesday':
        day = 'Mittwoch'
    elif day == 'Thursday':
        day = 'Donnerstag'
    elif day == 'Friday':
        day = 'Freitag'
    elif day == 'Saturday':
        day = 'Samstag'
    else:
        day = 'Sonntag'  
    print(time)  
    print(str(time))
    restaurants = zugreifer.getListOfRestaurantsForCustomer(customer.plz, day, time)                        
    return render_template('customer.html', customer=customer, restaurants = restaurants);

@app.route("/customer/speisekarte/<username>")
def restaurantMenu(username):
    if(not 'customer_username' in session):
        return redirect('/customer/login')
    if('chosen_restaurant' in session and username != session['chosen_restaurant']):
        zugreifer.deleteItemsFromBasket(session['customer_username'])
    session['chosen_restaurant'] = username
    restaurant_name = zugreifer.getRestaurantName(username)
    menuItems = zugreifer.getAllMenuItemsForRestaurant(username)
    drinks = []
    desserts = []
    mainCourses = []
    starters = []
    for item in menuItems:
        print(item.category)
        if item.category == 'Getränk':
            drinks.append(item)
        elif item.category == 'Nachtisch':
            desserts.append(item)
        elif item.category == 'Vorspeise':
            starters.append(item)
        else: 
            mainCourses.append(item)
    print(desserts)
    print(starters)        
    return render_template('customer_menu.html', drinks=drinks, desserts=desserts, mainCourses=mainCourses, starters=starters,restaurant_name=restaurant_name)

@app.route('/customer/speisekarte/')
def restaurantMenu2():
    return redirect("/customer/speisekarte/" + session['chosen_restaurant'])


@app.route("/customer/add/warenkorb/<int:itemId>", methods=['POST'])
def addToCart(itemId):
    customer_username = session['customer_username']
    zugreifer.addItemToBasket(customer_username, itemId)
    return restaurantMenu(session['chosen_restaurant'])


@app.route('/customer/basket')
def getBasket():
    if(not 'customer_username' in session):
        return redirect('/customer/login')
    if(not 'chosen_restaurant' in session):
        return render_template('restaurant_not_chosen.html', message="Sie sollen ein Restaurant auswählen!")
    restaurant_name = zugreifer.getRestaurantName(session['chosen_restaurant'])
    orderDetails = zugreifer.getItemsFromBasket(session['customer_username'])
    return render_template('basket.html', orderDetails = orderDetails, restaurant_name = restaurant_name)


@app.route('/customer/basket/update/<int:id>', methods=['POST'])
def updateBasket(id):
    zugreifer.deleteItemFromBasket(id)
    return getBasket()


@app.route('/customer/order/finish', methods=['POST'])
def finishOrder():
    zusatz = request.form['zusatz']
    now = datetime.now()
    eingangsUhrzeit = now.strftime('%H:%M:%S')
    today = date.today()
    zugreifer.insertNewOrder(session['customer_username'], session['chosen_restaurant'], zusatz, today, eingangsUhrzeit)
    zugreifer.deleteItemsFromBasket(session['customer_username'])
    flash(session['chosen_restaurant'] + ": Sie haben eine neue Bestellung erhalten")
    session.pop('chosen_restaurant', None)
    return redirect('/customer')
