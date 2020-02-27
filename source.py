#######################
## Muhsin Wahi-Anwar ##
#### Feb 22, 2020 #####
#######################

from tkinter import *
from tkinter import filedialog
from PIL import Image, ImageTk
import math
import os
import pytesseract
import fitz
import io


class CropNamer():

    def __init__(self, master, canvasSize = (1300, 800)):
        ##initializes a bunch of 
        self.master = master
        self.defaultSize = canvasSize

        self.rotationInDegrees = 0
        self.strRotation = StringVar()

        self.boxCoords = {"topLeft":{"x": 0, "y": 0}, "botRight":{"x": 0, "y": 0}}#storage for coords *in relation to the corner*
        self.fileName = ""
        self.folderPath = filedialog.askdirectory(parent=master)#asks for a folder to operate in

        ##looks for the first "scan" file in the folder
        directory = os.fsencode(self.folderPath)#encodes that folderpath into os for actual operation
        for file in os.listdir(directory):
            #looks through the given folder
            self.fileName = os.fsdecode(file)
            #file-name only string variable

            if self.fileName[:4].lower() == "scan":
                self.__selectionWindow()
                break
        mainloop()

    def __selectionWindow(self):

        filePath = self.folderPath + "/" + self.fileName
        self.strRotation.set(str(self.rotationInDegrees) + " degrees counter-clockwise")

        ###IMAGE PROCESSING###
        image = self.uploadImage(filePath)
        
        if image.size[0] >= self.defaultSize[0] or image.size[1] >= self.defaultSize[1]:
        #compares width and height of screen/default to the image size
            

            largeSideIndex = 0 if image.size[0]/self.defaultSize[0] >= image.size[1]/self.defaultSize[1] else 1 
            #chooses which side has the largest-picture-edge-size to screen-edge-size ratio
            
            sizeFactor = math.ceil(float(image.size[largeSideIndex]) / float(self.defaultSize[largeSideIndex])) 
            #reduces the size by a factor so the user can interact
            print(sizeFactor, image.size)
            image = image.resize((image.size[0] // sizeFactor, image.size[1] //sizeFactor), Image.ANTIALIAS)
            #Resize the image using a resize function
            print(sizeFactor, image.size)

        tk_image = ImageTk.PhotoImage(image)
        #stores a displayable version of the image

        #######################

        ### CREATE CANVAS ###
        self.canvas = Canvas(self.master, width=image.size[0], height=image.size[1])#makes the canvas as large as the resized picture
        self.canvas.create_image(0, 0, anchor=NW, image= tk_image)#puts the image in the canvas

        #Image mouse-clicking functionality
        self.canvas.bind("<Button-1>", self.__changeTopCoord)#stores the top-left coordinate
        self.canvas.bind("<ButtonRelease-1>", self.__changeBotCoord)#stores the top-right coordinate
        self.canvas.bind("<B1-Motion>", lambda event: self.__moveMouse(event, tk_image))#displays the rectangle to indicate where the user selected
        self.canvas.pack(expand = YES, fill = BOTH)#Puts the canvas in the window, expanding the window to fit it 
        #####################

        #####BUTTON AND LABEL CONFIGURATION#####
        self.btnReset = Button(self.master, text="Reset", command = lambda : self.canvas.create_image(0, 0, anchor=NW, image= tk_image))
        self.btnReset.pack(side = RIGHT)#This button resets the image, for some reason doesnt display image at all without it
        
        self.btnSubmit = Button(self.master, text="Submit", command = lambda : self.__process(sizeFactor))
        self.btnSubmit.pack(side = RIGHT)#this button submits the rectangle data into the method that crops, reads, and renames the other scanned images


        def addToRotation():
            ##Specifically increases the rotation value variable by a right angle
            ##So the final squares are read the correct way
            self.rotationInDegrees += 90
            if self.rotationInDegrees >= 360:
                self.rotationInDegrees = 0
            self.strRotation.set(str(self.rotationInDegrees) + " degrees counter-clockwise")
                
        self.btnRotate = Button(self.master, text="Rotate", command = addToRotation)#Adds 90 degrees to counterclockwise rotation
        self.btnRotate.pack(side = RIGHT)

        self.lblRotation = Label(self.master, textvariable = self.strRotation)#shows the degree of counter-clockwise rotation
        self.lblRotation.pack(side = RIGHT)
        ##############################

    def __changeTopCoord(self, event):
        ##Changes the top left coordinate of the box, adding it to the box-coordinate dict
        self.boxCoords["topLeft"]["x"], self.boxCoords["topLeft"]["y"] = event.x, event.y
        return "Top-left coordinate changed succesfully!"

    def __moveMouse(self, event, tk_image):
        ##Refreshes the image, then
        #Uses the top-left of the boxCoord variable and mouse position as coordinates
        #and displays a rectangle, to show the appearance of selecting an area
        self.canvas.create_image(0, 0, anchor=NW, image= tk_image)
        self.canvas.create_rectangle(self.boxCoords["topLeft"]["x"], self.boxCoords["topLeft"]["y"], event.x, event.y)
        return "Rectangle displayed"

    def __changeBotCoord(self, event):
        #Occurs when the mouse is clicked off,
        #Actually changes the dictionary coordinates to the mouse's de-click point
        self.boxCoords["botRight"]["x"], self.boxCoords["botRight"]["y"] = event.x, event.y
        return "Bottom-right coordinate changed successfully!"
        

    def uploadImage(self, filePath):
        img = "Error"
        if filePath.endswith(".jpg") or filePath.endswith(".jpeg"): #Directly gets jpg image
            print("JPG")
            img = Image.open(filePath)
            return img
        elif filePath.endswith(".pdf"):
            print("PDF")
            
            doc = fitz.Document(filePath)#Loads file using PyMu
            page = doc.loadPage(0)
            xref = page.getImageList()[0][0]#First image -> first image attribute : xref x
            baseImage = doc.extractImage(xref)
            img = Image.open(io.BytesIO(baseImage['image']))
            return img
        return img

    def __process(self, multiplier):

        directory = os.fsencode(self.folderPath)
        
        #Rescales the rectangle coordiantes for scanning    
        self.boxCoords["topLeft"]["x"], self.boxCoords["topLeft"]["y"] = self.boxCoords["topLeft"]["x"] * multiplier, self.boxCoords["topLeft"]["y"] * multiplier
        self.boxCoords["botRight"]["x"], self.boxCoords["botRight"]["y"] = self.boxCoords["botRight"]["x"] * multiplier, self.boxCoords["botRight"]["y"] * multiplier
        
        for file in os.listdir(directory):#Iterates through the folder
            filename = os.fsdecode(file)#Get the file name
            scannedMap = {}#placeholder for the map image
            if filename[:4].lower() == "scan":
                #for use in the final naming process
                extension = filename[filename.index("."):]
                    
                ##OPENS IMAGE##
                scannedMap = self.uploadImage(self.folderPath + "/" + filename)
                ##Crop image and get the name using text recognition##
                nameBox = scannedMap.crop((self.boxCoords["topLeft"]["x"], self.boxCoords["topLeft"]["y"], self.boxCoords["botRight"]["x"], self.boxCoords["botRight"]["y"])).rotate(self.rotationInDegrees)
                newName = pytesseract.image_to_string(nameBox)

                print(newName + extension)
                os.rename(self.folderPath + "/" + filename,self.folderPath + "/" +  newName+extension)
        self.master.destroy()
        return "Process success"

def main():
    root = Tk()
    CropNamer(root)
main()

