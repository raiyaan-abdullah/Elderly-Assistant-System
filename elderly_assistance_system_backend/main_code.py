import schedule
import time
import requests
from datetime import datetime
import datetime as dt
from dateutil.relativedelta import relativedelta
from easy_ocr_test import easy_ocr
import serial
from django import db
import sqlite3


conn=sqlite3.connect('db.sqlite3')

c=conn.cursor()

count=0

def validity(Time):
    time_now=datetime.now().time()
    time_now = datetime.combine(dt.date.today(), time_now)
    timedelta_obj = relativedelta(time_now, Time)
    if timedelta_obj.hours==0 and -55<=timedelta_obj.minutes<=55:
        return 1
    else:
        return 0

#need to modify these code so that for every medicine name the serial write is that drawer number
def solenoid_activate(medicine):
    with serial.Serial('COM4', 9800, timeout=1) as ser:
        time.sleep(2)
        if medicine=='Provair':
            ser.write(b'P')   # send the pyte string 'H'
            time.sleep(2)   # wait 0.5 seconds
        elif medicine=='E-CAP':
            ser.write(b'E')   # send the pyte string 'H'
            time.sleep(2)   # wait 0.5 seconds
        elif medicine=='Fexo':
            ser.write(b'F')   # send the pyte string 'H'
            time.sleep(2)   # wait 0.5 seconds
            

def call_ocr_code():
    c.execute("SELECT * FROM medicine_medicine") #got todays routine medicine list
    medicine_objects=c.fetchall()
    loopCount=0
    for obj in medicine_objects:
        #time_list.append(obj.time)
        datetime_object=datetime_object=datetime.strptime(obj[2], '%H:%M:%S')
        if(validity(dt.datetime.combine(dt.date.today(), datetime_object.time()))):  #check the medicine is correct for taking or not
            Date='"{}"'.format(dt.datetime.now().date())
            c.execute("SELECT * FROM medicine_history_medicinehistory WHERE medicine_id="+str(obj[0])+" AND date="+Date)
            con_medicine=c.fetchone()
            #print(con_medicine[1])
                    
            if con_medicine[1]==1:
                print("You have already taken your scheduled medicines.",obj[1])
                return 0
            else:
                #solenoid_activate(obj[1])
                print("Time for ",obj[1]," ",obj[2])
                easy_ocr(obj[1],obj[0],obj[2])


         
        else:
            loopCount+=1
        #missing_medicine_counter(obj)
    if loopCount==len(medicine_objects):
        #print(loopCount)
        print("Wrong time for medication")
        return 0


def create_data():
    required_medicine=[] #The medicine history data that will be sent to server
    keys_to_remove = ["name","time","started"]

    fetch_url = 'http://127.0.0.1:8000/api/medicine/'
    destination_url = 'http://127.0.0.1:8000/api/medicine-history/'
    
    '''
    Example of data to be sent
    {
        "name": "Ranitid",
        "date":"2020-04-15",
        "time": "15:23:00",
        "consumed": True,
        "time_of_consumption": "15:23:00"
        
    }
    '''

    received = requests.get(fetch_url).json() #The medicine list data received sent from server
    today = datetime.today().strftime('%Y-%m-%d')
    new_keys = {"date" : today, "consumed" : "False", "time_of_consumption" : "00:00:00"}

    for medicine in received:
        for key in keys_to_remove:
            medicine.pop(key)
        medicine['medicine_id'] = medicine.pop('id')
        medicine.update(new_keys)
        required_medicine.append(medicine)
        
        
        
    for medicine in required_medicine:
        sent_data = requests.post(destination_url, data = medicine)
        print(sent_data)
        
#schedule.every(5).minutes.do(create_data)

#create_data()

def medicine_code():
    while 1:
        #schedule.run_pending()
        #time.sleep(1)
        if call_ocr_code()==0:
            #return "You have already taken your scheduled medicines."
            break
        
#medicine_code()