import tkinter as tk
from pykpn.gui import drawAPI
from pykpn.platforms import platformDesigner, exynos_2chips, kalray_mppa

class visualisationPanel(tk.Frame):
    def __init__(self, parent, pHeight, pWidth, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent
        
        self.__mCanvas = tk.Canvas(self, height=pHeight, width=pWidth, background='white')
        self.__mCanvas.grid(row=0, column=0)
        self.__drawDevice = drawAPI.drawAPI(self.__mCanvas, 5, 10, 800, 600)
    
    def draw(self):
        platform = kalray_mppa.KalrayMppa()
        self.__drawDevice.setPlatform(platform)
        
    def reset(self):
        for handle in self.__mCanvas.find_all():
            self.__mCanvas.delete(handle)
        
class controlPanel(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent
        
        scheduling = tk.LabelFrame(self, text='Scheduling policy')
        tk.Button(scheduling, text='Set scheduling policy', command=self.__setPolicy).grid(row=1, column=0, columnspan=6, sticky='nsew')
        tk.Label(scheduling, text='Name').grid(row=0, column=0)
        self.__policyNameBox = tk.Text(scheduling, height=1, width=5)
        self.__policyNameBox.insert(0.0, 'FIFO')
        self.__policyNameBox.grid(row=0, column=1)
        tk.Label(scheduling, text='Cycles').grid(row=0, column=2)
        self.__policyCyclesBox = tk.Text(scheduling, height=1, width=5)
        self.__policyCyclesBox.insert(0.0, '50000')
        self.__policyCyclesBox.grid(row=0, column=3)
        scheduling.grid(row=0, column=0, columnspan=6, sticky='nsew', padx=5, pady=5)
        
        cluster = tk.LabelFrame(self, text='Add new Cluster')
        tk.Button(cluster, text='Add', command=self.__addCluster).grid(row=1, column=0, columnspan=6, sticky='nsew')
        tk.Label(cluster, text='PE Name').grid(row=0, column=0)
        self.__peNameBox = tk.Text(cluster, height=1, width=5)
        self.__peNameBox.insert(0.0, 'ARM')
        self.__peNameBox.grid(row=0, column=1)
        tk.Label(cluster, text='Amount').grid(row=0, column=2)
        self.__peAmountBox = tk.Text(cluster, height=1, width=5)
        self.__peAmountBox.insert(0.0, '9')
        self.__peAmountBox.grid(row=0, column=3)
        tk.Label(cluster, text='Frequency').grid(row=0, column=4)
        self.__peFrequencyBox = tk.Text(cluster, height=1, width=5)
        self.__peFrequencyBox.insert(0.0, '1000')
        self.__peFrequencyBox.grid(row=0, column=5)
        cluster.grid(row=1, column=0, columnspan=6, sticky='nsew', padx=5, pady=5)
        
        l1 = tk.LabelFrame(self, text='Add L1 Cache')
        tk.Button(l1, text='Add', command=self.__addL1Cache).grid(row=2, column=0, columnspan=6, sticky='nsew')
        tk.Label(l1, text='Cluster ID').grid(row=0, column=0)
        self.__CacheIdBox = tk.Text(l1, height=1, width=5)
        self.__CacheIdBox.grid(row=0, column=1)
        tk.Label(l1, text='Read Latency').grid(row=0, column=2)
        self.__CacheRLBox = tk.Text(l1, height=1, width=5)
        self.__CacheRLBox.insert(0.0, '1000')
        self.__CacheRLBox.grid(row=0, column=3)
        tk.Label(l1, text='Write Latency').grid(row=0, column=4)
        self.__CacheWLBox = tk.Text(l1, height=1, width=5)
        self.__CacheWLBox.insert(0.0, '1000')
        self.__CacheWLBox.grid(row=0, column=5)
        tk.Label(l1, text='Read throughput').grid(row=1, column=0)
        self.__CacheRTBox = tk.Text(l1, height=1, width=5)
        self.__CacheRTBox.insert(0.0, '1000')
        self.__CacheRTBox.grid(row=1, column=1)
        tk.Label(l1, text='Write throughput').grid(row=1, column=2)
        self.__CacheWTBox = tk.Text(l1, height=1, width=5)
        self.__CacheWTBox.insert(0.0, '1000')
        self.__CacheWTBox.grid(row=1, column=3)
        l1.grid(row=2, column=0, columnspan=6, sticky='nsew', padx=5, pady=5)
        
        
        connectCluster = tk.LabelFrame(self, text='Connect cluster')
        tk.Button(connectCluster, text='Connect', command=self.__connectCluster).grid(row=2, column=0, columnspan=6, sticky='nsew')
        tk.Label(connectCluster, text='Cluster IDs').grid(row=0, column=0)
        self.__clusterIdBox = tk.Text(connectCluster, height=1, width=5)
        self.__clusterIdBox.grid(row=0, column=1)
        tk.Label(connectCluster, text='Name').grid(row=0, column=2)
        self.__clusterNameBox = tk.Text(connectCluster, height=1, width=5)
        self.__clusterNameBox.insert(0.0, 'C0L3')
        self.__clusterNameBox.grid(row=0, column=3)
        tk.Label(connectCluster, text='Read Latency').grid(row=0, column=4)
        self.__clusterRLBox = tk.Text(connectCluster, height=1, width=5)
        self.__clusterRLBox.insert(0.0, '1000')
        self.__clusterRLBox.grid(row=0, column=5)
        tk.Label(connectCluster, text='Write Latency').grid(row=1, column=0)
        self.__clusterWLBox = tk.Text(connectCluster, height=1, width=5)
        self.__clusterWLBox.insert(0.0, '1000')
        self.__clusterWLBox.grid(row=1, column=1)
        tk.Label(connectCluster, text='Read throughput').grid(row=1, column=2)
        self.__clusterRTBox = tk.Text(connectCluster, height=1, width=5)
        self.__clusterRTBox.insert(0.0, '1000')
        self.__clusterRTBox.grid(row=1, column=3)
        tk.Label(connectCluster, text='Write throughput').grid(row=1, column=4)
        self.__clusterWTBox = tk.Text(connectCluster, height=1, width=5)
        self.__clusterWTBox.insert(0.0, '1000')
        self.__clusterWTBox.grid(row=1, column=5)
        connectCluster.grid(row=3, column=0, columnspan=6, sticky='nsew', padx=5, pady=5)
        
        self.__drawButton = tk.Button(self, text='Draw', command=self.parent.draw).grid(row=4, column=0, columnspan=3, sticky='nsew')
        self.__resetButton = tk.Button(self, text='Reset', command=self.parent.reset).grid(row=4, column=3, columnspan=3, sticky='nsew')


    def __setPolicy(self):
        name = self.__policyNameBox.get(0.0, tk.END)
        cycles = int(self.__policyCyclesBox.get(0.0, tk.END))
        
        if self.parent.mDesigner.setSchedulingPolicy(name, cycles): 
            print(name)
            print(cycles)
    
    def __addCluster(self):
        name = self.__peNameBox.get(0.0, tk.END)
        amount = int(self.__peAmountBox.get(0.0, tk.END))
        frequency = int(self.__peFrequencyBox.get(0.0, tk.END))
        
        if self.parent.mDesigner.addPeCluster(name, amount, frequency) >= 0:
            print(name)
            print(amount)
            print(frequency)
    
    def __addL1Cache(self):
        clusterID = int(self.__CacheIdBox.get(0.0, tk.END))
        rl = int(self.__CacheRLBox.get(0.0, tk.END))
        wl = int(self.__CacheWLBox.get(0.0, tk.END))
        rt = int(self.__CacheRTBox.get(0.0, tk.END))
        wt = int(self.__CacheWTBox.get(0.0, tk.END))
        
        if self.parent.mDesigner.addCacheForPEs(clusterID, rl, wl, rt, wt):
            print(clusterID)
            print(rl)
            print(wl)
            print(rt)
            print(wt)
        
    def __connectCluster(self):
        clusterIDs = []
        
        for clusterID in self.__clusterIdBox.get(0.0, tk.END).split(','):
            clusterIDs.append(int(clusterID))
        name = self.__clusterNameBox.get(0.0, tk.END)
        rl = int(self.__clusterRLBox.get(0.0, tk.END))
        wl = int(self.__clusterWLBox.get(0.0, tk.END))
        rt = int(self.__clusterRTBox.get(0.0, tk.END))
        wt = int(self.__clusterWTBox.get(0.0, tk.END))
        
        if self.parent.mDesigner.connectClusters(name, clusterIDs, rl, wl, rt, wt):
            print(clusterID)
            print(rl)
            print(wl)
            print(rt)
            print(wt)

class mainWindow(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent
        
        self.visPanel = visualisationPanel(self, 600, 800)
        self.visPanel.grid(row=0, column=1)
        
        self.contPanel = controlPanel(self)
        self.contPanel.grid(row=0, column=0)
        
        self.mDesigner = platformDesigner.platformDesigner('test')
    
    def draw(self):
        self.visPanel.draw()
    
    def reset(self):
        self.visPanel.reset()
        self.mDesigner.reset()
        

if __name__ == '__main__':
    root = tk.Tk()
    myMainWindow = mainWindow(root)
    myMainWindow.grid(row = 0, column = 0)
    root.mainloop()