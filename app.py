from flask import Flask, render_template, render_template, redirect, request
import zugreifer
from module_openingTime import *
import os

app = Flask(__name__)
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
    return render_template('speisekarte.html', items=zugreifer.getItemsVonSpeisekarte(zugreifer.getSpeisekarte(1)))

@app.route("/restaurant/delete_Item/<int:itemId>", methods=['POST'])
def delete_Item(itemId):
    zugreifer.removeItemFromSpeisekarte(itemId)
    return redirect("/restaurant")

@app.route("/restaurant/newItem")
def newItem():
    return render_template('newItem.html')
    
@app.route("/restaurant/newItem/safe", methods=['POST'])
def newItem_safe():
    restaurantId = int(1)
    itemName = request.form['itemname']
    itemPreis = request.form['itempreis']
    itemBeschreibung = request.form['itembeschreibung']
    itemBild = request.form['itembild']
    print(itemBild)
    speisekartenId = zugreifer.getSpeisekarte(restaurantId)
    zugreifer.insertNewItem(speisekartenId,itemName,itemPreis,itemBeschreibung,"BILD")
    return redirect("/restaurant")


@app.route("/restaurant/openingTime")
def openingTime():
    list = zugreifer.getOpeningTimesForRestaurant(1)
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
    print(mondaysList)
    print(tuesdayList)
    print(wednesdayList)    
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
    id  = 1
    day = request.form['day']
    fromTime = request.form['from']
    toTime = request.form['to']
    zugreifer.addOpeningTimes(1, day, fromTime, toTime)
    return redirect('/restaurant/openingTime')


@app.route("/restaurant/openingTime/delete-day/<int:id>", methods=['POST'])
def delete_day(id):
    print('ja')
    zugreifer.deleteOpeningTimeWithId(id)
    return redirect("/restaurant/openingTime")
