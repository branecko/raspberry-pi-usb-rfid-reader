# to allow read from /dev/hidraw0 create file with conent:
# create file: /etc/udev/rules.d/99-hidraw-permissions.rules
# add this:
# KERNEL=="hidraw*", SUBSYSTEM=="hidraw", MODE="0664", GROUP="plugdev"

# to create cron run: crontab -e in terminal
# add line at the end: @reboot python3 /home/pi/filename.py &

import sys
import time
# sudo pip3 install PyMySQL
import pymysql
# sudo pip3 install requests
import requests

# variables
DBHOST="localhost"
DBUSER="username"
DBPASS="superstrongpwd123"
DBNAME="dbname"
DBTABLE="raspberrypi"
DB_COLNAMES="`value`" # can use more name by "`col1`, `col2`"

API_BASEURL="http://myurl.com/api/"

# dumb note for myself: 1 = true and 0 = false in python
SAVE_TO_DB = 1
CALL_API = 0

def postCall( code ):
    r = requests.post(API_BASEURL, data = {'code': code})
    print(r.url) #debug
    print(r.content) #debug


def saveToDb( str ):
    db = pymysql.connect( DBHOST, DBUSER, DBPASS, DBNAME )
    # prepare a cursor object using cursor() method
    cursor = db.cursor()
    sql = "INSERT INTO `" + DBTABLE + "` ("+DB_COLNAMES+") VALUES ('" + str + "')" #add more values if needed
    try:
        # Execute the SQL command
        cursor.execute(sql)
        # Commit your changes in the database
        db.commit()
    except:
        # Rollback in case there is any error
        db.rollback()

    # disconnect from server
    db.close()
    

fp = open('/dev/hidraw0', 'rb') #change hidraw device as connected
newCode = ''

while True:
    buffer = fp.read(1)
    for c in buffer:
        if c > 0:
            if c == 30 : newCode = newCode + '1'
            elif c == 31 : newCode = newCode + '2'
            elif c == 32 : newCode = newCode + '3'
            elif c == 33 : newCode = newCode + '4'
            elif c == 34 : newCode = newCode + '5'
            elif c == 35 : newCode = newCode + '6'
            elif c == 36 : newCode = newCode + '7'
            elif c == 37 : newCode = newCode + '8'
            elif c == 38 : newCode = newCode + '9'
            elif c == 39 : newCode = newCode + '0'
            elif c == 40 :
                print('code:' + newCode) # debug
                
                if SAVE_TO_DB : saveToDb(newCode)
                
		if CALL_API : postCall(newCode)
                
		# reset code
                newCode = ''
