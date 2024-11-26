import matplotlib.pyplot as plt
import numpy as np


class Ball:
    def __init__(self, s, v, a, m, k, g):
        self.m = m
        self.k = k
        self.g = g
        
        self.s = s
        self.v = v
        self.a = a
    
    
    def updateVSA(self, dt):
        """Update v, s and a in order based on dt. Simulate falling with air resistance.
        """
        # Dette er fysikken:
        self.v = v = self.v + self.a*dt
        self.s = self.s + v*dt
        self.a = self.g - (self.k/self.m)*v*abs(v)

        
    def simulate(obj, T, res):
        time, dt = np.linspace(0, T, res, retstep=True)
        
        s = np.array([])
        v = np.array([])
        a = np.array([])
        
        print(time)
        for _ in time:
            obj.updateVSA(dt)
            s = np.append(s, obj.s)
            v = np.append(v, obj.v)
            s = np.append(a, obj.a)
        
        print(s)
        return time, s, v, a
            
            
            


# Initial Values 
g = 9.81
myfallingBall = Ball(
   s = 0,
   v = 0,
   a = g,
   
   m = 1,
   k = 0.001,
   g = g,
)

fallTime = 40 #sec
res = 1000

time, s, v, a = myfallingBall.simulate(fallTime, res)

plt.plot(time, s)
plt.title('Pressure over time')
plt.show()

plt.plot(time, v)
plt.title('Pressure over time')
plt.show()

plt.plot(time, a)
plt.title('Pressure over time')
plt.show()

            