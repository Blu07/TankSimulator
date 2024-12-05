import matplotlib.pyplot as plt
import numpy as np
import copy
import argparse

from time import perf_counter

class Tank:
    def __init__(self, h, lqH, r, rho, xPres, outH, outR, outTank = None, inQ=0):
        # Physical Properties 
        self.height = h
        self.r = r
        
        # Liqud State
        self.lqHeight = lqH
        self.volume = np.pi * r**2 * self.lqHeight
        
        # Liquid Properties
        self.rho = rho
        self.presExtra = xPres
        
        # Hole in and out
        self.outTank: Tank = outTank
        
        self.outH = outH    # Height above bottom of tank
        self.outR = outR    # Hole radius
        
        self.outQ = 0
        self.inQ = inQ
    
    
        
    def changeVolume(self, dV: int):
        self.volume = max(self.volume + dV, 0) # Update Volume, is never under 0
        self.lqHeight = self.volume / (np.pi * self.r**2)
   
    def changeLqHeight(self, dH: int):
        self.lqHeight = max(self.lqHeight + dH, 0)
        self.volume = np.pi * self.r**2 * self.lqHeight
    

    
    def stepSimulation(self, step):
        pressureAtHole = self.presExtra + self.rho * 9.81 * (self.lqHeight - self.outH) # g = 9.81
        
        if self.outTank:
            presDiffOut = pressureAtHole - self.outTank.presExtra
        else:
            presDiffOut = pressureAtHole - 101.5e3 # Atmospheric pressure outside the last tank
        
        
        # Calculate flow rate (Q) in m^3/s
        A = np.pi * self.outR**2 # Area cross of flow out
            # k = np.sqrt(2*self.g)
            # vOut = k * np.sqrt(self.lqHeight - self.outH) # Velocity out based on HEIGHT
        vOut = np.sqrt(max(0, (2 * presDiffOut) / self.rho)) # Velocity out based on PRESSURE 
        self.outQ = max(A*vOut, 0) # can not flow back up (when negative Q)

        # Update the inQ of the child tank to match this tank's outQ
        if self.outTank:
            self.outTank.inQ = self.outQ
        
        
        # To get the flow per step
        flowThrough = (self.inQ - self.outQ) * step
        # print("flow through:", flowThrough)
    
        self.changeVolume(flowThrough)
        




if __name__ == "__main__":
    
    
    
    # Tank Configuration
    outHeight = 0.3
    outRadius = 0.02
    
    tankHeight = 4.10
    tankRadius = 2
    
    rho = 1000
    liquidHeight = 3.7
    
    extraPressure = 101.5e3
    
    


    parser = argparse.ArgumentParser()
    parser.add_argument('numTanks', type=int, help='Number of tanks.')
    args = parser.parse_args()
    numTanks = args.numTanks


    # Creates a list of all the tank objects from bottom tank to top tank.
    tankTemplate = Tank(
                h=tankHeight,
                r=tankRadius,
                lqH=liquidHeight,
                rho=rho,
                xPres=extraPressure, # atmospheric pressure inside tank
                outH=outHeight,
                outR=outRadius,
                outTank=None,
            )
    
    tanks: list[Tank] = [tankTemplate] # This is the last tank; the outTank is None.
    valueList: list[list] = [[]]
    
    # Copy the template, set the outTank to the last tank in tanks (being the heighest one up)
    for _ in range(1, numTanks):
        newTank = copy.copy(tankTemplate)
        newTank.outTank = tanks[-1]
        
        tanks.append(newTank)
        valueList.append([])
    
    # Go through every tank for every time step.
    timeList = [] # running generation; the x-axis of plot
    time = 0
    
    # Put all the formulas in the simulation into one equation, solve for "step".
    # This makes sure that the volume change per step is not larger than some threshold, giving a nice resolution compared to compution time for any configuration and number of tanks.
    stepMillis = min(np.sqrt(numTanks) / 100, 0.5) * ( (tankHeight - outHeight) * tankRadius**2) / (outRadius**2 * np.sqrt( (2 * 9.81 * (liquidHeight - outHeight))) )

    lowestVolume = tanks[0].outH * tanks[0].r**2 * np.pi
    
    start = perf_counter()

    while tanks[0].volume > lowestVolume:
        timeList.append(time)
        # print(f"Simulation time: {time/1000} sec")
        for i, tank in enumerate(tanks):
            tank.stepSimulation(stepMillis)
            valueList[i].append(tank.volume)
            
        time += stepMillis/1000 # Store seconds instead of milliseconds
    end = perf_counter()
    
    elapsed = end - start
    print(f'Time taken: {elapsed:.6f} seconds')
    
    # Plot every graph with the same x-axis with time
    for y in valueList:
        plt.plot(timeList, y)
        

    # COnfigure plot and display
    plt.title('Volume over time')
    plt.show()
        
        
    



# Testing shows this performance:
    # 10000 tanks:
    #   error: 3.2L
    #   time: 507 seconds
    # 1000 tanks:
    #   error = 1.2L,
    #   time = 6.75 seconds
    # 100 tanks:
    #   error: 0.15L
    #   time: 0.18 seconds
    # 10 tanks:
    #   error = 0.011L,
    #   time = 0.0064 seconds
    # 1 tank:
    #   error: ~0L
    #   time: 0.00036 seconds