import tkinter as tk
from pykpn.slx.platform import SlxPlatform
from pykpn.gui.tetrisEngine import tetrisEngine
from pykpn.gui.testSuite import dataProvider

class controlPanel(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent
        self.__platform = None      
        self.__mappingIDs = []
        self.__choices =  {'default', 'mainPanel', 'optionPanel'}
        
        self.loadExButton = tk.Button(self, text='Load Exynos', command=self.__loadExynos)
        self.loadExButton.grid(sticky='EW', row = 0, column = 0, columnspan=2)
        
        self.loadPaButton = tk.Button(self, text='Load Parallella', command=self.__loadParallella)
        self.loadPaButton.grid(sticky='EW',row = 1, column = 0, columnspan=2)
        
        self.loadMdButton = tk.Button(self, text='Load MultiDSP', command=self.__loadMultiDSP)
        self.loadMdButton.grid(sticky='EW',row = 2, column = 0, columnspan=2) 
        
        self.provideButton = tk.Button(self, text='Provide options', command=self.provideOptions, state='disabled')
        self.provideButton.grid(sticky='EW', row=3, column=0, columnspan=2)
        
        self.__tnTarget = tk.StringVar(self)
        self.__tnTarget.set('default')
        tnTargetMenu = tk.OptionMenu(self, self.__tnTarget, *self.__choices)
        tnTargetMenu.grid(sticky='EW', row=4, column=0)
        self.toggleTNButton = tk.Button(self, text='Toggle task names', command=self.__toggleTaskNames, state='disabled')
        self.toggleTNButton.grid(sticky='EW', row=4, column=1)
        
        self.__peTarget = tk.StringVar(self)
        self.__peTarget.set('default')
        peTargetMenu = tk.OptionMenu(self, self.__peTarget, *self.__choices)
        peTargetMenu.grid(sticky='EW', row=5, column=0)
        self.togglePENButton = tk.Button(self, text='Toggle PE names', command=self.__togglePENames, state='disabled')
        self.togglePENButton.grid(sticky='EW', row=5, column=1)
        
        self.__dadTarget = tk.StringVar(self)
        self.__dadTarget.set('default')
        dadTargetMenu = tk.OptionMenu(self, self.__dadTarget, *self.__choices)
        dadTargetMenu.grid(sticky='EW', row=6, column=0)
        self.toggleDADButton = tk.Button(self, text='Toggle drag and drop names', command=self.__toggleDragAndDrop, state='disabled')
        self.toggleDADButton.grid(sticky='EW', row=6, column=1)
        
        self.ExitButton = tk.Button(self, text='Exit', command=root.destroy)
        self.ExitButton.grid(sticky='EW',row = 7, column = 0, columnspan=2)
        
    def __loadExynos(self):
        platform =  SlxPlatform('SlxPlatform', '/home/felix/eclipse-workspace/pykpn/pykpn/apps/audio_filter/exynos/exynos.platform', '2017.04')
        self.parent.mDataProvider = dataProvider(platform)
        self.parent.initialMapping = self.parent.mDataProvider.generateRandomMapping()
        self.parent.engineInstance.setPlatform(platform, self.parent.initialMapping)
        for key in self.parent.initialMapping.to_coreDict():
            if self.parent.initialMapping.to_coreDict()[key] != []:
                self.parent.usedCores.append(key)
        self.loadExButton['state'] = 'disabled'
        self.loadPaButton['state'] = 'disabled'
        self.loadMdButton['state'] = 'disabled'
        self.provideButton['state'] = 'normal'
        self.toggleDADButton['state'] = 'normal'
        self.togglePENButton['state'] = 'normal'
        self.toggleTNButton['state'] = 'normal'
                  
    def __loadParallella(self):
        platform =  SlxPlatform('SlxPlatform', '/home/felix/eclipse-workspace/pykpn/pykpn/apps/audio_filter/parallella/parallella.platform', '2017.04')
        self.parent.mDataProvider = dataProvider(platform)
        self.parent.initialMapping = self.parent.mDataProvider.generateRandomMapping()
        self.parent.engineInstance.setPlatform(platform, self.parent.initialMapping)
        for key in self.parent.initialMapping.to_coreDict():
            if self.parent.initialMapping.to_coreDict()[key] != []:
                self.parent.usedCores.append(key)
        self.loadExButton['state'] = 'disabled'
        self.loadPaButton['state'] = 'disabled'
        self.loadMdButton['state'] = 'disabled'
        self.provideButton['state'] = 'normal'
        self.toggleDADButton['state'] = 'normal'
        self.togglePENButton['state'] = 'normal'
        self.toggleTNButton['state'] = 'normal'
    
    def __loadMultiDSP(self):
        platform =  SlxPlatform('SlxPlatform', '/home/felix/eclipse-workspace/pykpn/pykpn/apps/audio_filter/multidsp/multidsp.platform', '2017.04')
        self.parent.mDataProvider = dataProvider(platform)
        self.parent.initialMapping = self.parent.mDataProvider.generateRandomMapping()
        self.parent.engineInstance.setPlatform(platform, self.parent.initialMapping)
        for key in self.parent.initialMapping.to_coreDict():
            if self.parent.initialMapping.to_coreDict()[key] != []:
                self.parent.usedCores.append(key)
        self.loadExButton['state'] = 'disabled'
        self.loadPaButton['state'] = 'disabled'
        self.loadMdButton['state'] = 'disabled'
        self.provideButton['state'] = 'normal'
        self.toggleDADButton['state'] = 'normal'
        self.togglePENButton['state'] = 'normal'
        self.toggleTNButton['state'] = 'normal'
        
    def provideOptions(self):
        options = []
        i = 0
        while i < self.parent.possibleOptions:
            options.append(self.parent.mDataProvider.generateRandomMapping())
            i += 1
        self.parent.engineInstance.setMappingOption(options)
    
    def __togglePENames(self):
        self.parent.engineInstance.togglePENames(self.__peTarget.get())
        
    def __toggleTaskNames(self):
        self.parent.engineInstance.toggleTaskNames(self.__tnTarget.get())
    
    def __toggleDragAndDrop(self):
        self.parent.engineInstance.toggleDragAndDrop(self.__dadTarget.get())
        

class mainWindow(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent
        self.possibleOptions = 4
        self.initialMapping = None
        self.mDataProvider = None
        self.usedCores = []
        self.mControlPanel = controlPanel(self) 
        self.mControlPanel.grid(row = 0, column = 0, sticky = 'NSEW')
        self.gameFrame = tk.Frame(self, width = 1200, height = 800)
        self.engineInstance = tetrisEngine(self.gameFrame, 1200, 800, self.possibleOptions, self.myCallback)
        self.engineInstance.toggleTaskNames('optionPanel')
        self.engineInstance.togglePENames('optionPanel')
        self.engineInstance.toggleDragAndDrop('mainPanel')
        self.gameFrame.grid(row = 0, column = 1)
        
    def myCallback(self):
        self.mControlPanel.provideOptions()
    

if __name__ == '__main__':
    root = tk.Tk()
    myMainWindow = mainWindow(root)
    myMainWindow.grid(row = 0, column = 0)
    root.mainloop()
    
    
    