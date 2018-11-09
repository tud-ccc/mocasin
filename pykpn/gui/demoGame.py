import tkinter as tk
from pykpn.slx.platform import SlxPlatform
from pykpn.slx.kpn import SlxKpnGraph
from pykpn.mapper.random import RandomMapping
from pykpn.gui.tetrisEngine import tetrisEngine
from pykpn.gui.testSuite import dataProvider

class controlPanel(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent
        self.__kpnInstance = SlxKpnGraph('SlxKpnGraph','/net/home/teweleit/eclipseWorkspace/pykpn/pykpn/apps/audio_filter.cpn.xml','2017.04')
        self.__platform = None      
        self.__mappingIDs = []
        
        self.loadExButton = tk.Button(self, text='Load Exynos', command=self.__loadExynos)
        self.loadExButton.grid(sticky='EW', row = 0, column = 0)
        self.loadPaButton = tk.Button(self, text='Load Parallella', command=self.__loadParallella)
        self.loadPaButton.grid(sticky='EW',row = 1, column = 0)
        self.loadMdButton = tk.Button(self, text='Load MultiDSP', command=self.__loadMultiDSP)
        self.loadMdButton.grid(sticky='EW',row = 2, column = 0) 
        self.provideButton = tk.Button(self, text='Provide options', command=self.__provideOptions, state='disabled')
        self.provideButton.grid(sticky='EW', row=3, column=0)
        self.ExitButton = tk.Button(self, text='Exit', command=root.destroy)
        self.ExitButton.grid(sticky='EW',row = 4, column = 0)
        
    def __loadExynos(self):
        platform =  SlxPlatform('SlxPlatform', '/net/home/teweleit/eclipseWorkspace/pykpn/pykpn/apps/audio_filter/exynos/exynos.platform', '2017.04')
        self.parent.initialMapping = RandomMapping(self.__kpnInstance, platform)
        self.parent.engineInstance.setPlatform(platform, self.parent.initialMapping)
        self.parent.mDataProvider = dataProvider(platform)
        for key in self.parent.initialMapping.to_coreDict():
            if self.parent.initialMapping.to_coreDict()[key] != []:
                self.parent.usedCores.append(key)
        self.loadPaButton['state'] = 'disabled'
        self.loadMdButton['state'] = 'disabled'
        self.provideButton['state'] = 'normal'
                  
    def __loadParallella(self):
        platform =  SlxPlatform('SlxPlatform', '/net/home/teweleit/eclipseWorkspace/pykpn/pykpn/apps/audio_filter/parallella/parallella.platform', '2017.04')
        self.parent.initialMapping = RandomMapping(self.__kpnInstance, platform)
        self.parent.engineInstance.setPlatform(platform, self.parent.initialMapping)
        self.parent.mDataProvider = dataProvider(platform)
        for key in self.parent.initialMapping.to_coreDict():
            if self.parent.initialMapping.to_coreDict()[key] != []:
                self.parent.usedCores.append(key)
        self.loadExButton['state'] = 'disabled'
        self.loadMdButton['state'] = 'disabled'
        self.provideButton['state'] = 'normal'
    
    def __loadMultiDSP(self):
        platform =  SlxPlatform('SlxPlatform', '/net/home/teweleit/eclipseWorkspace/pykpn/pykpn/apps/audio_filter/multidsp/multidsp.platform', '2017.04')
        self.parent.initialMapping = RandomMapping(self.__kpnInstance, platform)
        self.parent.engineInstance.setPlatform(platform, self.parent.initialMapping)
        self.parent.mDataProvider = dataProvider(platform)
        for key in self.parent.initialMapping.to_coreDict():
            if self.parent.initialMapping.to_coreDict()[key] != []:
                self.parent.usedCores.append(key)
        self.loadExButton['state'] = 'disabled'
        self.loadPaButton['state'] = 'disabled'
        self.provideButton['state'] = 'normal'
        
    def __provideOptions(self):
        options = []
        i = 0
        while i < self.parent.possibleOptions:
            options.append(self.parent.mDataProvider.generatePossibleMapping(self.parent.usedCores))
            i += 1
        self.parent.engineInstance.setMappingOption(options)
            
        

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
        self.gameFrame = tk.Frame(self, width = 1200, height = 600)
        self.engineInstance = tetrisEngine(self.gameFrame, 1200, 600, self.possibleOptions)
        self.gameFrame.grid(row = 0, column = 1)
        
    

if __name__ == '__main__':
    root = tk.Tk()
    myMainWindow = mainWindow(root)
    myMainWindow.grid(row = 0, column = 0)
    root.mainloop()