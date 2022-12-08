# -------------Part 1: Imports--------------------------

import pyodbc
import requests
import csv
from flask import Flask
# from flask_restful import Resource, Api
from views import views
import time
import requests
url='http://api.coincap.io/v2/assets'
no_data=True


app=Flask(__name__)
app.register_blueprint(views, url_prefix="/")

app.run()

#--------------------------------------------------


# app2=Flask("VideoAPI")
# api=Api(app2)


# videos={
#     'video1': {'title': 'Hello World in python'},
#     'video2': {'title': 'Why Matlab is the best language ever'}

# }


# class Video(Resource):
#     def get(self):
#         return videos

# api.add_resource(Video, '/get')

# if __name__=='__main__':
#     app.run()
#     # app2.run()
# #---------------------------------------







#-------------Part 2: Database Connection--------------------------





server = 'abcd2727.database.windows.net'
database = 'function_test'
username = 'adminn'
password = '{Abc@12345}'   
driver= '{ODBC Driver 17 for SQL Server}'
connection=pyodbc.connect('DRIVER='+driver+';SERVER=tcp:'+server+';PORT=1433;DATABASE='+database+';UID='+username+';PWD='+ password)


#-------------Part 3: Database Functions-------------------------

def read():
    cursor=connection.cursor()
    cursor.execute('SELECT * FROM table1')
    
    
    for i in cursor:
        print(i)
    connection.commit()


# age=18
def update():
    cursor=connection.cursor()
    cursor.execute('''
    UPDATE bitcoin_average 
    SET bitcoin_average=(?)
    WHERE primary_key=1; 
    ''',(last_average))
    connection.commit()

# def Delete():
#     cursor=connection.cursor()
#     cursor.execute('''
#     DELETE FROM table1
#     WHERE name='john'
#     ''')

#Truncate
def Delete_all():
        cursor=connection.cursor()
        cursor.execute('''
                    TRUNCATE TABLE table1
                    
                ''')
        connection.commit()

#Drop
def Drop():
    cursor=connection.cursor()
    cursor.execute('''
    DROP TABLE table1
    ''')
    connection.commit()

#-------------Part 4: More Functions-------------------------
def Write_To_DB(connection,NAME, PRICE_IN_USD, MARKET_CAP):

    cursor=connection.cursor()
    cursor.execute('INSERT INTO table1(NAME, PRICE_IN_USD, MARKET_CAP) VALUES(?,?,?)',(NAME,PRICE_IN_USD, MARKET_CAP))
#     Read(connection)
    connection.commit()
    
def Update_DB(connection,NAME, PRICE_IN_USD, MARKET_CAP):
    cursor=connection.cursor()
    cursor.execute('UPDATE table1 SET NAME=(?),PRICE_IN_USD=(?), MARKET_CAP=(?);',(NAME,PRICE_IN_USD,MARKET_CAP))
    connection.commit()
    
def first_write():
    
    for i in outdata:
        NAME=i[0]
        PRICE_IN_USD=i[1]
        MARKET_CAP=i[2]
        
        
        Write_To_DB(connection,NAME,PRICE_IN_USD, MARKET_CAP)
#         else: 
#             Update_DB(connection, NAME,PRICE_IN_USD, MARKET_CAP )
    
#     no_data=False

def constant_update():
    headers={
    'Accept': 'application/json',
    'Content-Type': 'application/json'
        }


    response=requests.request("GET", url, headers=headers, data={})
    myjson= response.json()


    outdata=[]
    csvheader=['NAME', 'PRICE_IN_USD', 'MARKET_CAP']

    for x in myjson['data']:
        listing = [x['name'],x['priceUsd'],x['marketCapUsd']]
        outdata.append(listing)
    for i in outdata:
        NAME=i[0]
        PRICE_IN_USD=i[1]
        MARKET_CAP=i[2]
        Update_DB(connection, NAME,PRICE_IN_USD, MARKET_CAP )







#-------------Part 5: Main-------------------------
count=0
avg=0
last_average=15995.156547562
while True:
    time.sleep(0.5)
    Delete_all()
    
    headers={
        'Accept': 'application/json',
        'Content-Type': 'application/json'
            }


    response=requests.request("GET", url, headers=headers, data={})
    myjson= response.json()


    outdata=[]
    csvheader=['NAME', 'PRICE_IN_USD', 'MARKET_CAP']

    for x in myjson['data']:
        listing = [x['name'],x['priceUsd'],x['marketCapUsd']]
        outdata.append(listing)
        if x['name']=='Bitcoin':
            bitcoin=x['priceUsd']
            count+=1
            if count<=20:
                avg+=float(bitcoin)
            else:
                last_average=avg/20
                count=0
                avg=0
     
    update()
    first_write()

