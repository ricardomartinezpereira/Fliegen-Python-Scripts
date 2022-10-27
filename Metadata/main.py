
from PIL import Image
from PIL.ExifTags import TAGS
import exif
import pdfx
import os


files_location = "./files/"

selected_option = ""

text = ""


def get_files():

    # lists the files which we are going to extract metadata from
    list_of_files = os.listdir("./files")

    # if there is no files, display this message and end the program
    if len(list_of_files) == 0:
        print(" ===============  NOT FILES FOUND   =============== ")
        exit(0)
    
    return list_of_files


def show_title():

    print("===============================================================")
    print("===============================================================")
    print("=================  EXTRACT METADATA PROGRAM   =================")
    print("===============================================================")
    print("===============================================================")  


def get_options():

    global selected_option

    print("\n\n")
    option_msg = """TYPE NUMBER OF THE ACTION YOU WANT TO PERFORM?
        \n1- DISPLAY ON THE SCREEN: 
        \n2- SAVE DATA IN A FILE:
        \n3- DELETE METADATA FROM IMAGES:
        \n>> """

    selected_option = input(option_msg)


def get_metadata_from_images(file):

    extracted_data = ""

    try:

        # following two lines open the file and extract the exif data
        img = Image.open(f"{files_location}{file}")
        metadata = img.getexif()

        for tagid in metadata:

            tagname = TAGS.get(tagid, tagid)
            value = metadata.get(tagid)

            # adds the data
            extracted_data += f"\t{tagname} : {value}\n"
        
        img.close()

        return extracted_data

    except FileNotFoundError:
        print("\n===============  NOT FILES FOUND   ===============\n")
        exit(0)


def get_metadata_from_pdf(file):

    extracted_data = ""

    try:

        pdf = pdfx.PDFx(f"{files_location}{file}")
        metadata = pdf.get_metadata()

        for key in metadata:

            # adds the data
            extracted_data += f"\t{key} : {metadata[key]}\n"
        
        return extracted_data

    except FileNotFoundError:
        print("\n===============  NOT FILES FOUND   ===============\n")
        exit(0)


def delete_metadata_img(file):
    
    global files_location

    img = exif.Image(open(f"{files_location}{file}", "rb"))
    img.delete_all()
    file = open(f"./results/NO_METADATA_{file}", "wb")
    file.write(img.get_file())
    file.close()


def extract_metadata():

    global text
    global selected_option
    global files_location

    # stores data that will be shown to the user
    text = ""

    list_of_files = get_files()

    for file in list_of_files:

        # extract the extension of files, example: .jpg, .png, .pdf
        extension = os.path.splitext(file)[1].lower()

        text += f"\n\n===============  ({file}) METADATA   ===============\n\n"

        if extension == ".jpg" or extension == ".png":
            text += get_metadata_from_images(file)

        elif extension == ".pdf":
            text += get_metadata_from_pdf(file)
        
        else:
            print(f"\n=============== EXTENSION ({extension}) NOT SUPPORTED   ===============\n")


    # if user option is 1 display data on the screen
    if selected_option.lower() == "1":
        print(text)
        print("===============  END OF PROGRAM   ===============\n")

    # if user option is 2 creates a file and save data there
    elif selected_option.lower() == "2":
        os.mkdir("./results")
        f = open("./results/metadata.txt","a")
        f.write(text)
        f.close()
        print("\n===============  EXTRACTION COMPLETED SUCCESSFULLY   ===============\n")

    elif selected_option.lower() == "3":
        
        for file in list_of_files:

            # extract the extension of files, example: .jpg, .png, .pdf
            extension = os.path.splitext(file)[1].lower()

            if extension == ".jpg" or extension == ".png":
                delete_metadata_img(file)

            elif extension == ".pdf":
                pass

        
        print("\n===============  METADATA DELETED  ===============")
        print("===============  YOUT CAN FIND FILES WITHOUT METADATA IN (./results)   ===============\n")
        

    else:
        print(f"\n===============  OPTION NOT SUPPORTED   ===============\n")



#####         #####         ######         ###   #####      ###
######       ######        ###  ###        ###   ######     ###
###  ##     ##  ###       ###    ###       ###   ###  ##    ###
###   ##   ##   ###      ###      ###      ###   ###   ##   ###
###    ## ##    ###     ### ###### ###     ###   ###    ##  ###
###     ###     ###    ###          ###    ###   ###     ## ### 
###             ###   ###            ###   ###   ###      #####    

if __name__ == "__main__":

    show_title()

    get_options()

    extract_metadata()

    