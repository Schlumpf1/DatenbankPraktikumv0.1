from flask import Flask, render_template, render_template, redirect, request, jsonify, session
import zugreifer
from module_openingTime import *
import os
import re
from datetime import datetime


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
    return redirect("/restaurant")

@app.route("/home")
def home1():
    return "Hallo"

@app.route("/restaurant")
def restaurant():
    return render_template('speisekarte.html', items=zugreifer.getItemsVonSpeisekarte(zugreifer.getSpeisekarte(session['username'])))

@app.route("/restaurant/delete_Item/<int:itemId>", methods=['POST'])
def delete_Item(itemId):
    zugreifer.removeItemFromSpeisekarte(itemId)
    return redirect("/restaurant")

@app.route("/restaurant/newItem")
def newItem():
    return render_template('newItem.html')
    
@app.route("/restaurant/newItem/safe", methods=['POST'])
def newItem_safe():
    username = session['username']
    itemName = request.form['itemname']
    itemPreis = request.form['itempreis']
    itemBeschreibung = request.form['itembeschreibung']
    itemBild = request.form['itembild']
    print(itemBild)
    speisekartenId = zugreifer.getSpeisekarte(username)
    zugreifer.insertNewItem(speisekartenId,itemName,itemPreis,itemBeschreibung,"BILD")
    return redirect("/restaurant")


@app.route("/restaurant/openingTime")
def openingTime():
    list = zugreifer.getOpeningTimesForRestaurant(session['username'])
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
    username  = session['username']
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

    if(not re.match("\d\d:\d\d", toTime)):
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

    time_object_from = datetime.strptime(fromTime, '%H:%M').time()
    time_object_to = datetime.strptime(toTime, '%H:%M').time();
    if(time_object_from > time_object_to):
        errors.append('Von soll kleiner als Bis sein')

    res1 = zugreifer.selectOpeningTimeGreaterThanFrom(username, day, time_object_from)
    print(res1)
    res2 = zugreifer.selectOpeningTimesLessThanTo(username, day, time_object_to)
    print(res2)
    res3 = zugreifer.selectOpeningTimesIncludeOtherTimes(username, day, time_object_from, time_object_to);
    print(res3)
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
                session['username'] = username;
                return redirect("/restaurant")
            
        
    #elif request.method == 'GET':
    return render_template('restaurant_login.html')
    
@app.route("/restaurant/registrieren", methods =['POST', 'GET'])
def restaurant_register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        passwordControll = request.form['passwordControll']
        restaurantName = request.form['restaurantName']
        adresse = request.form['adresse']
        if password == passwordControll:
            #usernamedopplung pruefen
            if zugreifer.existUsername(username) ==False:
                zugreifer.insertNewRestaurant(username, password, restaurantName, adresse)
                return redirect('/restaurant')
            else:
                render_template('restaurant_register.html',message="Username already in use!")
        else:
            return jsonify(error='Username already exists!'), 402
    #Wenn Methode != POST, password != passwordControll
    return render_template('restaurant_register.html',message = "")

