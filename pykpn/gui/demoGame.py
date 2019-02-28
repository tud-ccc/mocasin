import tkinter as tk
from tkinter import messagebox
import random as rnd
from pykpn.gui.drawAPI import drawAPI

class controlPanel(tk.LabelFrame):
    def __init__(self, parent, *args, **kwargs):
        tk.LabelFrame.__init__(self, parent,text="Controls", *args, **kwargs)
        self.parent = parent
        
        self.timeHandle = None
        
        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)
        self.rowconfigure(2, weight=1)
        self.rowconfigure(3, weight=1)
        
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.columnconfigure(2, weight=1)
        self.columnconfigure(3, weight=1)
        self.columnconfigure(4, weight=1)
        self.columnconfigure(5, weight=1)
        
        self.levellabel = tk.Label(self, text="Level:\n", background="white", bd=2, relief='groove', font='bold')
        self.levellabel.grid(row=0, column=0, rowspan=2, sticky='nesw', pady=5, padx=5)
        
        self.timelabel = tk.Label(self, text="Time:\n", background="white", bd=2, relief='groove', font='bold')
        self.timelabel.grid(row=2, column=0, rowspan=2, sticky='nesw', pady=5, padx=5)
        
        self.amountlabel = tk.Label(self, text="Mappings:\n", background="white", bd=2, relief='groove', font='bold')
        self.amountlabel.grid(row=4, column=0, rowspan=2, sticky='nesw', pady=5, padx=5)
        
        self.__upButton = tk.Button(self, text="Up (W)", command=self.__up, state='disabled')
        self.__upButton.grid(row=0, column=2, sticky='nesw')
        
        self.__downButton = tk.Button(self, text="Down (S)", command=self.__down, state='disabled')
        self.__downButton.grid(row=2, column=2, sticky='nesw')
        
        self.__leftButton = tk.Button(self, text="Left (A)", command=self.__left, state='disabled')
        self.__leftButton.grid(row=1, column=1, sticky='nesw')
        
        self.__rightButton = tk.Button(self, text="Right (D)", command=self.__right, state='disabled')
        self.__rightButton.grid(row=1, column=3, sticky='nesw')
        
        self.__rotateButton = tk.Button(self, text="Rotate (Space)", command=self.__rotate, state='disabled')
        self.__rotateButton.grid(row=0, column=4, sticky='nesw')
        
        self.__applyButton = tk.Button(self, text="Apply (Enter)", command=self.apply, state='disabled')
        self.__applyButton.grid(row=1, column=4, sticky='nesw')
        
        self.__newButton = tk.Button(self, text="New mapping (Q)", command=self.__new, state='disabled')
        self.__newButton.grid(row=2, column=4, sticky='nesw')
        
        self.__startButton = tk.Button(self, text="Start", command=self.__start)
        self.__startButton.grid(row=3, column=4, sticky='nesw')
        
        self.__endButton = tk.Button(self, text="End game", command=self.__end, state='disabled')
        self.__endButton.grid(row=4, column=4, sticky='new')
        
            
    def __start(self):
        self.parent.start()
        self.enable()
     
    def __end(self):
        self.after_cancel(self.timeHandle)
        self.parent.gameOver(False)
        self.disable()
    
    def enable(self):
        self.__upButton.config(state='normal')
        self.__downButton.config(state='normal')
        self.__leftButton.config(state='normal')
        self.__rightButton.config(state='normal')
        self.__rotateButton.config(state='normal')
        self.__applyButton.config(state='normal')
        self.__newButton.config(state='normal')
        self.__endButton.config(state='normal')
        self.__startButton.config(state='disabled')
    
    def disable(self):
        self.__upButton.config(state='disabled')
        self.__downButton.config(state='disabled')
        self.__leftButton.config(state='disabled')
        self.__rightButton.config(state='disabled')
        self.__rotateButton.config(state='disabled')
        self.__applyButton.config(state='disabled')
        self.__newButton.config(state='disabled')
        self.__endButton.config(state='disabled')
        self.__startButton.config(state='normal')
    
    def __up(self):
        self.parent.optionPanel.moveUp()
        
    def __down(self):
        self.parent.optionPanel.moveDown()
        
    def __left(self):
        self.parent.optionPanel.moveLeft()
        
    def __right(self):
        self.parent.optionPanel.moveRight()
        
    def __rotate(self):
        self.parent.optionPanel.rotate()
        
    def apply(self):
        if self.parent.finalize():
            self.amount += 1
            print(self.amount)
            self.amountlabel.config(text="Mappings:\n" + str(self.amount))
        
    def __new(self):
        self.parent.setOption(True)
    
    def startLevel(self, level, time):
        self.amount = 0
        if self.timeHandle != None:
            self.after_cancel(self.timeHandle)
        self.timeLeft = time
        self.levellabel.config(text="Level:\n" + str(level))
        self.timelabel.config(text="Time:\n" + str(time))
        self.amountlabel.config(text="Mappings:\n" + str(self.amount))
        self.timeHandle = self.after(1000, self.__actualize)
        
    def __actualize(self):
        self.timeLeft -= 1
        self.timelabel.config(text="Time:\n" + str(self.timeLeft))
        if self.timeLeft <= 0:
            self.parent.gameOver()
            self.timelabel.config(text="Time:\n")
            self.levellabel.config(text="Time:\n")
        else:
            self.timeHandle = self.after(1000, self.__actualize)

class visualisationPanel(tk.Frame):
    def __init__(self, parent, pHeight, pWidth, white=False, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent
        
        self.__mCanvas = tk.Canvas(self, width=pWidth, height=pHeight)
        if white:
            self.__mCanvas.config(border=5, relief="ridge")
        self.__mCanvas.grid()
        self.__mApiInstance = drawAPI(self.__mCanvas, 5, 10, pWidth, pHeight)
        self.__mApiInstance.setFakePlatform(fakePlatform())
        self.__currentMappingIDs = []
        self.__currentMappings = []
        self.__connectionHandles = []
            
    def setMapping(self, mapping, withConnection = False):
        if self.__currentMappingIDs != []:
            for identifier in self.__currentMappingIDs:
                self.__mApiInstance.removeMapping(identifier)
            self.__currentMappingIDs = []
            self.__currentMappings = []
        self.__currentMappingIDs.append(self.__mApiInstance.addFakeMapping(mapping))
        self.__currentMappings.append(mapping)
        if withConnection:
            self.__drawConnection(mapping)
    
    def addMapping(self, mapping, withConnection):
        self.__currentMappingIDs.append(self.__mApiInstance.addFakeMapping(mapping))
        self.__currentMappings.append(mapping)
        if(withConnection):
            self.__drawConnection(mapping)
    
    def __drawConnection(self, mapping):
        for handle in self.__connectionHandles:
            self.__mCanvas.delete(handle)
        
        for mapping in self.__currentMappings:
            coordsT0 = None
            coordsT1 = None
            coordsT2 = None
            coordsT3 = None
        
            for key in mapping.getNameHandles():
                if mapping.getNameHandles()[key] == "T0":
                    coordsT0 = self.__mCanvas.coords(key)
                elif mapping.getNameHandles()[key] == "T1":
                    coordsT1 = self.__mCanvas.coords(key)
                elif mapping.getNameHandles()[key] == "T2":
                    coordsT2 = self.__mCanvas.coords(key)
                elif mapping.getNameHandles()[key] == "T3":
                    coordsT3 = self.__mCanvas.coords(key)

            if mapping.getShape() == "lright" or mapping.getShape() == "lleft":
                color = mapping.getColor()
                self.__connectionHandles.append(self.__mCanvas.create_line(coordsT0[0], coordsT0[1], coordsT1[0], coordsT1[1], fill = color, width=5))
                self.__connectionHandles.append(self.__mCanvas.create_line(coordsT1[0], coordsT1[1], coordsT2[0], coordsT2[1], fill = color, width=5))
                self.__connectionHandles.append(self.__mCanvas.create_line(coordsT2[0], coordsT2[1], coordsT3[0], coordsT3[1], fill = color, width=5))
            elif mapping.getShape() == "square":
                color = mapping.getColor()
                self.__connectionHandles.append(self.__mCanvas.create_line(coordsT0[0], coordsT0[1], coordsT1[0], coordsT1[1], fill = color, width=5))
                self.__connectionHandles.append(self.__mCanvas.create_line(coordsT1[0], coordsT1[1], coordsT0[0], coordsT0[1], fill = color, width=5))
                self.__connectionHandles.append(self.__mCanvas.create_line(coordsT2[0], coordsT2[1], coordsT3[0], coordsT3[1], fill = color, width=5))
                self.__connectionHandles.append(self.__mCanvas.create_line(coordsT3[0], coordsT3[1], coordsT2[0], coordsT2[1], fill = color, width=5))
            elif mapping.getShape() == "stick":
                color = mapping.getColor()
                self.__connectionHandles.append(self.__mCanvas.create_line(coordsT0[0], coordsT0[1], coordsT1[0], coordsT1[1], fill = color, width=5))
                self.__connectionHandles.append(self.__mCanvas.create_line(coordsT1[0], coordsT1[1], coordsT2[0], coordsT2[1], fill = color, width=5))
                self.__connectionHandles.append(self.__mCanvas.create_line(coordsT2[0], coordsT2[1], coordsT3[0], coordsT3[1], fill = color, width=5))
            elif mapping.getShape() == "triangle":
                color = mapping.getColor()
                self.__connectionHandles.append(self.__mCanvas.create_line(coordsT0[0], coordsT0[1], coordsT2[0], coordsT2[1], fill = color, width=5))
                self.__connectionHandles.append(self.__mCanvas.create_line(coordsT1[0], coordsT1[1], coordsT2[0], coordsT2[1], fill = color, width=5))
                self.__connectionHandles.append(self.__mCanvas.create_line(coordsT3[0], coordsT3[1], coordsT2[0], coordsT2[1], fill = color, width=5))
    
    def getMapping(self):
        return self.__currentMappings[0]
        
    def moveLeft(self):
        description = self.__currentMappings[0].getMappingDescription()
        newDescription = {}
        for key in description:
            number = int(key.split(' ')[1])
            if description[key] != [] and number % 5 == 0 :
                print("Impossible")
                return
            elif description[key] != []:
                newKey = "Core " + str(number -1)
                newDescription.update({newKey : description[key]})
        
        for key in description:
            if not key in newDescription:
                newDescription.update({key : []})
        shape = self.__currentMappings[0].getShape()
        orientation = self.__currentMappings[0].getOrientation()
        self.setMapping(fakeMapping(newDescription, shape, orientation))
    
    def moveRight(self):
        description = self.__currentMappings[0].getMappingDescription()
        newDescription = {}
        for key in description:
            number = int(key.split(' ')[1])
            if description[key] != [] and (number + 1) % 5 == 0 :
                print("Impossible")
                return
            elif description[key] != []:
                newKey = "Core " + str(number + 1)
                newDescription.update({newKey : description[key]})
        
        for key in description:
            if not key in newDescription:
                newDescription.update({key : []})
        shape = self.__currentMappings[0].getShape()
        orientation = self.__currentMappings[0].getOrientation()
        self.setMapping(fakeMapping(newDescription, shape, orientation))
    
    def moveUp(self):
        description = self.__currentMappings[0].getMappingDescription()
        newDescription = {}
        for key in description:
            number = int(key.split(' ')[1])
            if description[key] != [] and number <= 4:
                print("Impossible")
                return
            elif description[key] != []:
                newKey = "Core " + str(number - 5)
                newDescription.update({newKey : description[key]})
            
        for key in description:
            if not key in newDescription:
                newDescription.update({key : []})
        shape = self.__currentMappings[0].getShape()
        orientation = self.__currentMappings[0].getOrientation()
        self.setMapping(fakeMapping(newDescription, shape, orientation))  
    
    def moveDown(self):
        description = self.__currentMappings[0].getMappingDescription()
        newDescription = {}
        for key in description:
            number = int(key.split(' ')[1])
            if description[key] != [] and number >= 20:
                print("Impossible")
                return
            elif description[key] != []:
                newKey = "Core " + str(number + 5)
                newDescription.update({newKey : description[key]})
        
        for key in description:
            if not key in newDescription:
                newDescription.update({key : []})
        shape = self.__currentMappings[0].getShape()
        orientation = self.__currentMappings[0].getOrientation()
        self.setMapping(fakeMapping(newDescription, shape, orientation))

    def rotate(self):
        if self.__currentMappings[0] == None:
            return
        description = self.__currentMappings[0].getMappingDescription()
        newDescription = {}
        shape = self.__currentMappings[0].getShape()
        orientation = self.__currentMappings[0].getOrientation()
        newOrientation = None
        
        if shape == "square":
            return
        elif shape == "triangle":
            for key in description:
                number = int(key.split(' ')[1])
                if description[key] == ["T2"] and (number >= 20 or number <= 4 or number % 5 == 0 or (number+1) % 5 == 0):
                    print("Impossible")
                    return
                elif description[key] == ["T0"]:
                    if orientation == "up":
                        newKey = "Core " + str(number + 6)
                        newDescription.update({newKey : ["T0"]})
                    elif orientation == "down":
                        newKey = "Core " + str(number - 6)
                        newDescription.update({newKey : ["T0"]})
                    elif orientation == "left":
                        newKey = "Core " + str(number - 4)
                        newDescription.update({newKey : ["T0"]})
                    elif orientation == "right":
                        newKey = "Core " + str(number + 4)
                        newDescription.update({newKey : ["T0"]})
                elif description[key] == ["T1"]:
                    if orientation == "up":
                        newKey = "Core " + str(number - 4)
                        newDescription.update({newKey : ["T1"]})
                    elif orientation == "down":
                        newKey = "Core " + str(number + 4)
                        newDescription.update({newKey : ["T1"]})
                    elif orientation == "left":
                        newKey = "Core " + str(number - 6)
                        newDescription.update({newKey : ["T1"]})
                    elif orientation == "right":
                        newKey = "Core " + str(number + 6)
                        newDescription.update({newKey : ["T1"]})
                elif description[key] == ["T2"]:
                    newDescription.update({key : ["T2"]})
                    if orientation == "up":
                        newOrientation = "right"
                    elif orientation == "down":
                        newOrientation = "left"
                    elif orientation == "left":
                        newOrientation = "up"
                    elif orientation == "right":
                        newOrientation = "down"
                elif description[key] == ["T3"]:
                    if orientation == "up":
                        newKey = "Core " + str(number + 4)
                        newDescription.update({newKey : ["T3"]})
                    elif orientation == "down":
                        newKey = "Core " + str(number - 4)
                        newDescription.update({newKey : ["T3"]})
                    elif orientation == "left":
                        newKey = "Core " + str(number + 6)
                        newDescription.update({newKey : ["T3"]})
                    elif orientation == "right":
                        newKey = "Core " + str(number - 6)
                        newDescription.update({newKey : ["T3"]})
                    
        elif shape == "lright":
            for key in description:
                number = int(key.split(' ')[1])
                if description[key] == ["T2"] and (
                    (orientation == "up" and (number >= 20  or (number + 2) % 5 == 0)) or
                    (orientation == "right" and (number % 5 == 0 or number >= 15)) or
                    (orientation == "down" and (number <= 4 or (number - 1) % 5 == 0)) or
                    (orientation == "left" and (number <= 9 or (number + 1) % 5 == 0))
                    ):
                    print("Impossible")
                    return
                elif description[key] == ["T0"]:
                    if orientation == "up":
                        newKey = "Core " + str(number + 12)
                        newDescription.update({newKey : ["T0"]})
                    elif orientation == "down":
                        newKey = "Core " + str(number - 12)
                        newDescription.update({newKey : ["T0"]})
                    elif orientation == "right":
                        newKey = "Core " + str(number + 8)
                        newDescription.update({newKey : ["T0"]})
                    elif orientation == "left":
                        newKey = "Core " + str(number - 8)
                        newDescription.update({newKey : ["T0"]})
                elif description[key] == ["T1"]:
                    if orientation == "up":
                        newKey = "Core " + str(number + 6)
                        newDescription.update({newKey : ["T1"]})
                    elif orientation == "down":
                        newKey = "Core " + str(number - 6)
                        newDescription.update({newKey : ["T1"]})
                    elif orientation == "right":
                        newKey = "Core " + str(number + 4)
                        newDescription.update({newKey : ["T1"]})
                    elif orientation == "left":
                        newKey = "Core " + str(number - 4)
                        newDescription.update({newKey : ["T1"]})
                elif description[key] == ["T2"]:
                    newDescription.update({key : ["T2"]})
                    if orientation == "up":
                        newOrientation = "right"
                    elif orientation == "down":
                        newOrientation = "left"
                    elif orientation == "left":
                        newOrientation = "up"
                    elif orientation == "right":
                        newOrientation = "down"
                elif description[key] == ["T3"]:
                    if orientation == "up":
                        newKey = "Core " + str(number + 4)
                        newDescription.update({newKey : ["T3"]})
                    elif orientation == "down":
                        newKey = "Core " + str(number - 4)
                        newDescription.update({newKey : ["T3"]})
                    elif orientation == "right":
                        newKey = "Core " + str(number - 6)
                        newDescription.update({newKey : ["T3"]})
                    elif orientation == "left":
                        newKey = "Core " + str(number + 6)
                        newDescription.update({newKey : ["T3"]})
        elif shape == "lleft":
            for key in description:
                number = int(key.split(' ')[1])
                if description[key] == ["T2"] and (
                    (orientation == "up" and ((number + 2) % 5 == 0 or (number + 1) % 5 == 0)) or
                    (orientation == "right" and  number >= 15) or
                    (orientation == "down" and (number % 5 == 0 or (number - 1) % 5 == 0)) or
                    (orientation == "left" and number <= 9)
                    ):
                    print("Impossible")
                    return
                elif description[key] == ["T0"]:
                    if orientation == "up":
                        newKey = "Core " + str(number + 12)
                        newDescription.update({newKey : ["T0"]})
                    elif orientation == "down":
                        newKey = "Core " + str(number - 12)
                        newDescription.update({newKey : ["T0"]})
                    elif orientation == "right":
                        newKey = "Core " + str(number + 8)
                        newDescription.update({newKey : ["T0"]})
                    elif orientation == "left":
                        newKey = "Core " + str(number - 8)
                        newDescription.update({newKey : ["T0"]})
                elif description[key] == ["T1"]:
                    if orientation == "up":
                        newKey = "Core " + str(number + 6)
                        newDescription.update({newKey : ["T1"]})
                    elif orientation == "down":
                        newKey = "Core " + str(number - 6)
                        newDescription.update({newKey : ["T1"]})
                    elif orientation == "right":
                        newKey = "Core " + str(number + 4)
                        newDescription.update({newKey : ["T1"]})
                    elif orientation == "left":
                        newKey = "Core " + str(number - 4)
                        newDescription.update({newKey : ["T1"]})
                elif description[key] == ["T2"]:
                    newDescription.update({key : ["T2"]})
                    if orientation == "up":
                        newOrientation = "right"
                    elif orientation == "down":
                        newOrientation = "left"
                    elif orientation == "left":
                        newOrientation = "up"
                    elif orientation == "right":
                        newOrientation = "down"
                elif description[key] == ["T3"]:
                    if orientation == "up":
                        newKey = "Core " + str(number - 4)
                        newDescription.update({newKey : ["T3"]})
                    elif orientation == "down":
                        newKey = "Core " + str(number + 4)
                        newDescription.update({newKey : ["T3"]})
                    elif orientation == "right":
                        newKey = "Core " + str(number + 6)
                        newDescription.update({newKey : ["T3"]})
                    elif orientation == "left":
                        newKey = "Core " + str(number - 6)
                        newDescription.update({newKey : ["T3"]})
        elif shape == "stick":
            for key in description:
                number = int(key.split(' ')[1])
                if description[key] == ["T2"] and (
                    (orientation == "up" and (number % 5 == 0 or (number + 1) % 5 == 0 or (number + 2) % 5 == 0)) or
                    (orientation == "right" and (number <= 4 or number >= 15)) or
                    (orientation == "down" and (number % 5 == 0 or (number + 1) % 5 == 0 or (number - 1) % 5 == 0)) or
                    (orientation == "left" and (number <= 9 or number >= 20))
                    ):
                    print("Impossible")
                    return
                elif description[key] == ["T0"]:
                    if orientation == "up":
                        newKey = "Core " + str(number + 12)
                        newDescription.update({newKey : ["T0"]})
                    elif orientation == "down":
                        newKey = "Core " + str(number - 12)
                        newDescription.update({newKey : ["T0"]})
                    elif orientation == "right":
                        newKey = "Core " + str(number + 8)
                        newDescription.update({newKey : ["T0"]})
                    elif orientation == "left":
                        newKey = "Core " + str(number - 8)
                        newDescription.update({newKey : ["T0"]})
                elif description[key] == ["T1"]:
                    if orientation == "up":
                        newKey = "Core " + str(number + 6)
                        newDescription.update({newKey : ["T1"]})
                    elif orientation == "down":
                        newKey = "Core " + str(number - 6)
                        newDescription.update({newKey : ["T1"]})
                    elif orientation == "right":
                        newKey = "Core " + str(number + 4)
                        newDescription.update({newKey : ["T1"]})
                    elif orientation == "left":
                        newKey = "Core " + str(number - 4)
                        newDescription.update({newKey : ["T1"]})
                elif description[key] == ["T2"]:
                    newDescription.update({key : ["T2"]})
                    if orientation == "up":
                        newOrientation = "right"
                    elif orientation == "down":
                        newOrientation = "left"
                    elif orientation == "left":
                        newOrientation = "up"
                    elif orientation == "right":
                        newOrientation = "down"
                elif description[key] == ["T3"]:
                    if orientation == "up":
                        newKey = "Core " + str(number - 6)
                        newDescription.update({newKey : ["T3"]})
                    elif orientation == "down":
                        newKey = "Core " + str(number + 6)
                        newDescription.update({newKey : ["T3"]})
                    elif orientation == "right":
                        newKey = "Core " + str(number - 4)
                        newDescription.update({newKey : ["T3"]})
                    elif orientation == "left":
                        newKey = "Core " + str(number + 4)
                        newDescription.update({newKey : ["T3"]})
        else: 
            raise RuntimeError("Unknown shape!")
        
        for key in description:
            if not key in newDescription:
                newDescription.update({key : []})
        self.setMapping(fakeMapping(newDescription, shape, newOrientation))
        
    def setUsedCores(self, usedCores):
        self.__mApiInstance.setUsedCores(usedCores)

    def clear(self):
        for identifier in self.__currentMappingIDs:
            self.__mApiInstance.removeMapping(identifier)
        for identifier in self.__connectionHandles:
            self.__mCanvas.delete(identifier)
        self.__mApiInstance.setUsedCores([])
        self.__connectionHandles = []
        self.__currentMappingIDs = []
        self.__currentMappings = []

class mainWindow(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent
        self.generator = fakeMappingGenerator()
        self.usedCores = []
        self.usedCandidates = {}
        
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.columnconfigure(2, weight=1)
        
        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)
        self.rowconfigure(2, weight=1)
        
        self.currentLevel = None
        self.started = False
        
        tk.Label(self, text="Running on chip", font='Helvetica 12 bold').grid(row=0, column=0)
        tk.Label(self, text="Next mapping to apply", font='Helvetica 12 bold').grid(row=0, column=2)
        
        self.appliedPanel = visualisationPanel(self, 700, 600)
        self.appliedPanel.grid(row=1, column=0, rowspan=2)
        
        arrow = tk.Canvas(self, width = 100, height = 200)
        arrow.grid(row=1, column=1, padx=5)
        arrow.create_line(5, 100, 95, 100, arrow=tk.FIRST, arrowshape=(8,15,10),width=30)
        
        self.optionPanel = visualisationPanel(self, 450, 350, True)
        self.optionPanel.grid(row=1, column=2)
        
        self.controlPanel = controlPanel(self)
        self.controlPanel.grid(row=2, column=2)
        
        self.focus_set()
        self.bind("<Key>", self.__keyPressed)
    
    def __keyPressed(self, event):
        if not self.started:
            return
        if event.keysym == 'Return':
            self.controlPanel.apply()
        elif event.keysym == 'w':
            self.optionPanel.moveUp()
        elif event.keysym == 'a':
            self.optionPanel.moveLeft()
        elif event.keysym == 's':
            self.optionPanel.moveDown()
        elif event.keysym == 'd':
            self.optionPanel.moveRight()
        elif event.keysym == 'q':
            self.setOption(True)
        elif event.keysym == 'space':
            self.optionPanel.rotate()
    
    def setOption(self, reduceTime = False):
        self.optionPanel.setMapping(self.generator.generateMapping())
        
        if reduceTime:
            self.controlPanel.timeLeft -= 1
    
    def finalize(self):
        mapping = self.optionPanel.getMapping()
        
        if self.usedCandidates == {}:
            for key in mapping.getMappingDescription():
                self.usedCandidates.update({key : 0})
        
        for key in mapping.getMappingDescription():
            if key in self.usedCores and len(mapping.getMappingDescription()[key]) > 0:
                return False
        
        for key in mapping.getMappingDescription():
            if mapping.getMappingDescription()[key] != []:
                self.usedCandidates[key] += 1
        
        for key in self.usedCandidates:
            if self.usedCandidates[key] >= self.currentLevel and not key in self.usedCores:
                self.usedCores.append(key)
        
        self.setOption()
        self.appliedPanel.addMapping(mapping, True)
        self.appliedPanel.setUsedCores(self.usedCores)
        
        if (self.controlPanel.amount + 1) >= self.currentLevel * 5:
            self.controlPanel.amountlabel.config(text="Mappings:\n" + str(self.currentLevel * 5))
            self.controlPanel.after_cancel(self.controlPanel.timeHandle)
            self.appliedPanel.clear()
            self.optionPanel.clear()
            self.usedCores = []
            self.usedCandidates = {}
            self.newLevel()
            return False
        return True
        
    def start(self):
        self.started = True
        info = messagebox.showinfo("Level 1", "Apply 5 mappings to the platform.\nOnly one task per core.\nYou have 30 seconds.")
        if info:
            self.setOption()
            self.currentLevel = 1
            self.controlPanel.startLevel(self.currentLevel, 30)
    
    def newLevel(self):
        self.currentLevel += 1
        if self.currentLevel == 2:
            info = messagebox.showinfo("Level 2", "Level 1 completed!\nNow apply 10 mappings to the platform.\nTwo tasks per core.\nYou have 60 seconds.") 
        elif self.currentLevel == 3:
            info = messagebox.showinfo("Level 3", "Level 2 completed!\nNow apply 15 mappings to the platform.\nThree tasks per core.\nYou have 60 seconds.")
        elif self.currentLevel > 3:
            info = messagebox.showinfo("Congratulation", "You won!")
            self.gameOver(False)
            info = False
        if info:
            self.controlPanel.startLevel(self.currentLevel, 60)
            self.setOption()
    
    def gameOver(self, show = True):
        if show:
            messagebox.showinfo("Game over", "Time is up. You lost!")
        self.started = False
        self.appliedPanel.clear()
        self.optionPanel.clear()
        self.usedCores = []
        self.usedCandidates = {}
        self.controlPanel.levellabel.config(text="Level:\n")
        self.controlPanel.timelabel.config(text="Time:\n")
        self.controlPanel.amountlabel.config(text="Mappings:\n")
        self.controlPanel.disable()
            
    
class fakePlatform():
    def __init__(self):
        self.__coreDictionary = {}
        self.__coreClasses = []
        self.__equalList = [["network_on_chip"]]
        self.__platformDescription = [("network_on_chip", ["Core 0","Core 1","Core 2","Core 3", "Core 4",
                                                           "Core 5","Core 6","Core 7","Core 8","Core 9",
                                                           "Core 10","Core 11","Core 12","Core 13","Core 14",
                                                           "Core 15","Core 16","Core 17","Core 18","Core 19",
                                                           "Core 20","Core 21","Core 22","Core 23","Core 24",
                                                           ])]
        
    def getPlatformDescription(self):
        """Returns the platformDescription.
        :returns: The __platformDescription value.
        :rtype list[(str, [list])]:
        """
        return self.__platformDescription
    
    def addCoreClass(self,length):
        """Adds a size of processing elements to the list of existing sizes of processing elements.
        :param int length: The size of the processing element that should be appended.
        """
        i = 0
        isInserted = False
        if self.__coreClasses == []:
                self.__coreClasses.append(length)
                return
        for entry in self.__coreClasses:
            if entry == length:
                return
            elif entry < length:
                i += 1
            else:
                self.__coreClasses.insert(i, length)
                isInserted = True
        if not isInserted:
            self.__coreClasses.insert(i, length)
        return
    
    def getCoreClasses(self):
        """Returns the list of existing sizes of processing elements.
        :returns: The __coreClasses value.
        :rtype list[int]:
        """
        return self.__coreClasses
       
    def updateCoreDict(self, key, value):
        """Adds an entry to the coreDictionary.
        :param str key: The name of the processing element.
        :param list[int] value: A list of integers containing start x and y value, end x and y value, the handle and the color of the processing element in this order.
        """
        self.__coreDictionary.update({key : value})
        
    def getCoreDict(self):
        """Returns the dictionary of existing processing elements.
        :returns: The __coreDictionary value.
        :rtype dict{str, list[int]}
        """
        return self.__coreDictionary
    
    def clearHandles(self):
        """Clears the dictionary containing all information about the drawn cores in case the platform has to be redrawn
        """
        self.__coreDictionary.clear()

class fakeMapping():
    def __init__(self, mappingDescription, shape, orientation):
        self.__mappingDescription = mappingDescription
        self.__mShape = shape
        self.__mOrientation = orientation
        self.__mappingId = None
        self.__color = None
        self.__circleHandles = []
        self.__nameHandles = {}
    
    def setIdentifier(self, identifier):
        self.__mappingId = identifier
    
    def setColor(self, color):
        self.__color = color
    
    def getShape(self):
        return self.__mShape
    
    def getOrientation(self):
        return self.__mOrientation
    
    def addCircleHandle(self, handle):
        """Adds a ne handle to the list of circle handles.
        :param int handle: The handle that should be added.
        """
        self.__circleHandles.append(handle)
        return
    
    def getCircleHandles(self):
        """Returns the list of circle handles.
        :returns: The list of circle handles.
        :rtype list[int]:
        """
        return self.__circleHandles
    
    def addNameHandle(self, handle, name):
        """Adds an entry to the __nameHandles dict.
        :param int handle: The handle that should be added as key.
        :param str name: The process name that should be added as value.
        """
        self.__nameHandles.update({handle : name})
        return
    
    def getNameHandles(self):
        """Returns the __nameHandle dict.
        :returns: The __nameHandle dictionary.
        :rtype {int, str}:
        """
        return self.__nameHandles
    
    def clearHandles(self):
        """Resets the __circleHandles list and the __nameHandles dictionary.
        """
        self.__circleHandles.clear()
        self.__nameHandles.clear()
    
    def getColor(self):
        """Returns the color value of the mappingInformation object.
        :returns: The Tkinter color value __color.
        :rtype str:
        """
        return self.__color
    
    def getMappingDescription(self):
        """Returns the mapping description dictionary of the mappingInformation object.
        :returns: The __mappingDescription dictionary.
        :rtype dict{int, str}: 
        """
        return self.__mappingDescription
    
    def getMappingId(self):
        """Returns the ID of the mappingInformation object.
        :returns: The __mappingId value.
        :rtype int:
        """
        return self.__mappingId

class fakeMappingGenerator():
    def __init__(self):
        return
        
    def generateMapping(self):
        decider = rnd.randint(0, 4)
        mappingDescription = {}
        shape = ""
        if decider == 0:
            mappingDescription = {"Core 0": [],"Core 1": [],"Core 2": [],"Core 3": [],"Core 4": [],
                                  "Core 5": [],"Core 6": [],"Core 7": ["T0"],"Core 8": [],"Core 9": [],
                                  "Core 10": [],"Core 11": ["T1"],"Core 12": ["T2"],"Core 13": ["T3"],"Core 14": [],
                                  "Core 15": [],"Core 16": [],"Core 17": [],"Core 18": [],"Core 19": [],
                                  "Core 20": [],"Core 21": [],"Core 22": [],"Core 23": [],"Core 24": []}
            shape = "triangle"
        elif decider == 1:
            mappingDescription = {"Core 0": [],"Core 1": [],"Core 2": [],"Core 3": [],"Core 4": [],
                                  "Core 5": [],"Core 6": [],"Core 7": ["T0"],"Core 8": [],"Core 9": [],
                                  "Core 10": [],"Core 11": [],"Core 12": ["T1"],"Core 13": [],"Core 14": [],
                                  "Core 15": [],"Core 16": [],"Core 17": ["T2"],"Core 18": [],"Core 19": [],
                                  "Core 20": [],"Core 21": [],"Core 22": ["T3"],"Core 23": [],"Core 24": []}
            shape = "stick"
        elif decider == 2:
            mappingDescription = {"Core 0": [],"Core 1": [],"Core 2": [],"Core 3": [],"Core 4": [],
                                  "Core 5": [],"Core 6": [],"Core 7": [],"Core 8": [],"Core 9": [],
                                  "Core 10": [],"Core 11": [],"Core 12": ["T0"],"Core 13": ["T1"],"Core 14": [],
                                  "Core 15": [],"Core 16": [],"Core 17": ["T2"],"Core 18": ["T3"],"Core 19": [],
                                  "Core 20": [],"Core 21": [],"Core 22": [],"Core 23": [],"Core 24": []}
            shape = "square" 
        elif decider == 3:
            mappingDescription = {"Core 0": [],"Core 1": [],"Core 2": [],"Core 3": [],"Core 4": [],
                                  "Core 5": [],"Core 6": [],"Core 7": ["T0"],"Core 8": [],"Core 9": [],
                                  "Core 10": [],"Core 11": [],"Core 12": ["T1"],"Core 13": [],"Core 14": [],
                                  "Core 15": [],"Core 16": [],"Core 17": ["T2"],"Core 18": ["T3"],"Core 19": [],
                                  "Core 20": [],"Core 21": [],"Core 22": [],"Core 23": [],"Core 24": []}
            shape = "lright"
        elif decider == 4:
            mappingDescription = {"Core 0": [],"Core 1": [],"Core 2": [],"Core 3": [],"Core 4": [],
                                  "Core 5": [],"Core 6": [],"Core 7": ["T0"],"Core 8": [],"Core 9": [],
                                  "Core 10": [],"Core 11": [],"Core 12": ["T1"],"Core 13": [],"Core 14": [],
                                  "Core 15": [],"Core 16": ["T3"],"Core 17": ["T2"],"Core 18": [],"Core 19": [],
                                  "Core 20": [],"Core 21": [],"Core 22": [],"Core 23": [],"Core 24": []}
            shape = "lleft"
        else:
            raise RuntimeError("Your random package is not working!")
        mapping = fakeMapping(mappingDescription, shape, "up")
        return mapping


if __name__ == '__main__':
    root = tk.Tk()
    myMainWindow = mainWindow(root)
    myMainWindow.grid(row = 0, column = 0)
    root.mainloop()
    
    
    