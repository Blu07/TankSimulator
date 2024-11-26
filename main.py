import matplotlib.pyplot as plt
import numpy as np


class Tank:
    def __init__(self, h, r, rho, g, xPres, atmPres, outH, outR):
        # Physical Properties 
        self.height = h
        self.r = r
        
        self.extraPressure = xPres
        
        # Liqud State
        self.lqHeight = h
        self.volume = np.pi * r**2 * self.lqHeight
        
        # Liquid Properties
        self.rho = rho
        self.g = g
        self.atmPres = atmPres
        
        # Hole in and out
        self.outH = outH    # Height above bottom of tank
        self.outR = outR    # Hole radius
    
    
    def updateLqHeight(self):
        """Updates the registered height of the liquid based on the current volume
        """
        self.lqHeight = self.volume / (np.pi * self.r**2)
    
    def updateVolume(self):
        """Updates the registered volume of the liquid based on the current volume
        """
        self.volume = np.pi * self.r**2 * self.lqHeight

    

    def changeHeight(self, dH: int):
        self.height += dH
        
        
    def changeVolume(self, dV: int):
        self.volume = max(self.volume + dV, 0) # Update Volume, is never under 0
        self.lqHeight = self.volume/(np.pi * self.r**2)
        
        print(f"volume is {self.volume}, set height to {self.lqHeight}")
   
   
    def changeLqHeight(self, dH: int):
        self.volume += dH
        self.volume = np.pi * self.r**2 * self.lqHeight
    
    
    def getPressure(self, atHeight: int = 0):
        return self.atmPres + self.rho * self.g * (self.lqHeight - atHeight)
    

    
    def stepSimulation(self, step):
        pressureAtHole = self.getPressure(self.outH)
        
        presDiff = pressureAtHole - self.atmPres
        
        if presDiff >= 0:
            
            # Calculate flow rate (Q) in m^3/s
            A = np.pi * self.outR**2 # Area cross of flow out
                # k = np.sqrt(2*self.g)
                # v = k * np.sqrt(self.height - self.outH) # Velocity out based on HEIGHT
            v = np.sqrt((2 * presDiff) / self.rho) # Velocity out based on PRESSURE
            Q = A*v 

            # To get the flow per step
            flowThrough = -Q * step
        
            self.changeVolume(flowThrough)
        

    
    
    def createSimulationRecord(self, T, res):
        
        time, step = np.linspace(0, T, res, retstep=True)
        xList = []
        
        for _ in time:
            self.stepSimulation(step)
            xList.append(self.volume) # Change which metric to record
            
        return time, xList
            
        

h = 4.10
r = 1
rho = 1000
g = 9.81
P1 = 101.5e3

outH = 1
outR = 0.01
    

myTank = Tank(
    h=h,
    r=r,
    rho=rho,
    g=g,
    atmPres=P1,
    xPres=0,
    outH=outH,
    outR=outR
)

simTime = 10 # sec
simRes = 1000000

time, x = myTank.createSimulationRecord(simTime*1000, simRes)

plt.plot(time, x)
plt.title('Volume over time')
plt.ylim((0, 15))
plt.show()


            