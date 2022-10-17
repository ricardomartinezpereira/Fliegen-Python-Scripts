
from email import encoders
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
import smtplib
import ssl
import csv
import json


class SendMassMails:

  def __init__(self):

    self.__message = MIMEMultipart("alternative")

    try:

      # getting config data from config.json file
      file = open("./config.json")
      json_file = json.load(file)
      file.close()

      # storing config data into these variables
      self.__host = json_file["host"]
      self.__port = json_file["port"]
      self.__password = json_file["password"]
      self.__username = json_file["username"]
 
    except Exception:
      print("(./config.json) file not found!")
      exit(0)


  def __getEmailsFromCsv(self):

    try:

      # getting emails stored in emails.csv file
      csvfile = open("./emails.csv", newline="")
      spamreader = csv.reader(csvfile, delimiter=" ", quotechar="|")
      emails = []

      for row in spamreader:
        emails.append(row[0])

      csvfile.close()

      # returns all emails as an array
      return emails

    except Exception:
      print("File with mails not found!")
      exit(0)


  def createMailContent(self, subject, fromm, html, files=[]):

    # settings mails info
    self.__message["Subject"] = subject
    self.__message["From"] = f"{fromm} <{self.__username}>"

    #part1 = MIMEText(text, "plain")
    part2 = MIMEText(html, "html")
    part3 = MIMEBase("application", "octet-stream")

    # attaching files to the mail message
    for f in files:
      part3.set_payload( open(f, "rb").read() )
      encoders.encode_base64(part3)
      filename = f"filename={os.path.basename(f)}"
      part3.add_header("Content-Disposition", f"attachment; {filename}")
      self.__message.attach(part3)

    #self.__message.attach(part1)
    self.__message.attach(part2)
  

  def SendMails(self):

    try:

      context = ssl.create_default_context()

      # setting the smtp object and login
      smtp = smtplib.SMTP(self.__host, self.__port)
      smtp.starttls(context= context)
      smtp.login(self.__username, self.__password)

      print("Sending mails...")

      # storing all emails where we will send the mail
      for email in self.__getEmailsFromCsv():
        self.__message["To"] = email

      # sending the mail to all emails
      smtp.sendmail(self.__username, self.__message["To"], self.__message.as_string())
      print("Mails sent to receivers!")

    except Exception as e:
      print(f"Error sending the mails {email}!")
      print(e)

    finally:
      smtp.quit()
    


try:

  obj = SendMassMails()

  # subject of the mail
  subject = "Informacion Importante."

  # html content that we will send to the mail
  html = open("./html_content.html", "r").read()

  # title of the mail
  fromm = "Send Mass Email Test"

  # files attach to the mail
  files = ["./image.png"]

  # obj.createMailContent(subject, fromm, html, files)

  obj.createMailContent(subject, fromm, html)

  obj.SendMails()

except Exception as e:
  print("(./html_content.html) file not found!")
  print(e)
  exit(0)










