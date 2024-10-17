import matplotlib.pyplot as plt
import numpy as np


class Tank:
    def __init__(self, h, r, rho, g, P1, outH, outR):
        self.height = h
        self.r = r
        
        self.lqHeight = h
        self.volume = np.pi * r**2 * self.lqHeight
        print(self.volume, self.lqHeight)
        
        self.rho = rho
        self.g = g
        self.P1 = P1
        
        self.outH = outH
        self.outR = outR
    
    
    def updateLqHeight(self):
        self.lqHeight = self.volume / (np.pi * self.r**2)
    
    def updateVolume(self):
        self.volume = np.pi * self.r**2 * self.lqHeight

    


    def changeHeight(self, dH: int):
        self.height += dH
        
        
    def changeVolume(self, dV: int):
        self.volume += dV
        self.lqHeight = self.volume / (np.pi * self.r**2)
        print(f"volume is {self.volume}, set height to {self.lqHeight}")
   
   
    def changeLqHeight(self, dH: int):
        self.volume += dH
        self.volume = np.pi * self.r**2 * self.lqHeight
    
    
    def getPressure(self, atHeight: int = 0):
        return self.P1 + self.rho * self.g * (self.lqHeight - atHeight)
    
    
    def simulate(self, T, res):
        time, step = np.linspace(0, T, res, retstep=True)
        pressures = []
        
        for _ in time:
            pressureAtHole = self.getPressure(self.outH)
            
            # Calculate flow rate (Q) in m^3/s
            A = np.pi * self.outR**2
            v = np.sqrt((2 * pressureAtHole) / self.rho)
            Q = A*v

            # To get the flow per step, multiply by the step size
            flowOut = Q * step
            
            if pressureAtHole >= 0:
                self.changeVolume(-flowOut)
            
            pressures.append(self.getPressure())
            
        return time, pressures
            
        

h = 4.10
r = 1
rho = 1000
g = 9.81
P1 = 101.5e3

    
    

myTank = Tank(
    h=h,
    r=r,
    rho=rho,
    g=g,
    P1=P1,
    outH=0.1,
    outR=0.01
)

time, pressures = myTank.simulate(20000, 300)

plt.plot(time, pressures)
plt.title('Pressure over time')
plt.show()

def f(t):
    return 30000 + 120 * t

time_values = np.linspace(0, 100, 500)
a_values = f(time_values)

# Plot the graph
plt.figure()
plt.plot(time_values, a_values)
plt.xlabel('Dager (t)')
plt.ylabel('Befolkning')
plt.title('Graf av befolkning f(t) = 30000 + 120t')
plt.show()

            