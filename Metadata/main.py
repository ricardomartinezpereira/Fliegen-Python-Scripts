
from PIL import Image
from PIL.ExifTags import TAGS
import pdfx
import os

print("***************************************************************")
print("*****************  EXTRACT METADATA PROGRAM   *****************")
print("***************************************************************\n")

try:

    # lists the files which we are going to extract metadata from
    files = os.listdir("./files")

    # if there is no files, display this message and end the program
    if len(files) == 0:
        print("\n*****************  NOT FILES FOUND   *****************\n")
        exit(0)
    
    option = input("TYPE NUMBER OF THE ACTION YOU WANT TO PERFORM?\n1- DISPLAY ON THE SCREEN: \n2- SAVE DATA IN A FILE:\nENTER NUMBER OF ACTION: ")

    # stores data that will be shown to the user
    text = ""

    print("\nLOADING...")

    for item in files:

        # extract the extension of files, example: .jpg, .png, .pdf
        extension = item[-4:]

        text += f"\n*****************  ({item}) METADATA   *****************\n\n"

        if extension == ".jpg" or extension == ".png":

            # following two lines open the file and extract the exif data
            img = Image.open(f"./files/{item}")
            metadata = img.getexif()

            for tagid in metadata:

                tagname = TAGS.get(tagid, tagid)
                value = metadata.get(tagid)

                # adds the data
                text += f"\t{tagname} : {value}\n"
            
            img.close()
            
        elif extension == ".pdf":

            pdf = pdfx.PDFx(f"./files/{item}")
            metadata = pdf.get_metadata()

            for key in metadata:

                # adds the data
                text += f"\t{key} : {metadata[key]}\n"
        
        else:
            print(f"\n*****************  ({item}) NOT SUPPORTED   *****************\n")


    # if user option is 1 display data on the screen
    if option.lower() == "1":
        print(text)
        print("********************  END OF PROGRAM   ********************\n")

    # if user option is 2 creates a file and save data there
    elif option.lower() == "2":
        os.mkdir("./results")
        f = open("./results/metadata.txt","a")
        f.write(text)
        f.close()
        print("\n*****************  EXTRACTION COMPLETED SUCCESSFULLY   *****************\n")

    else:
        print(f"\n*****************  OPTION NOT SUPPORTED   *****************\n")

except FileNotFoundError:
    print("\n*****************  NOT FILES FOUND   *****************\n")
    exit(0)
    
        


