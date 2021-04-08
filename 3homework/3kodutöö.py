#Kiirendus peab toimuma sujuvalt - kiirenduse muutuse suurus ei tohi olla suurem, kui 1[m/s^3]
#Viimasesse tsooni (x >= 500) jõudes peab jääma sõiduk koheselt seisma

import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import minimize

class ModelPredictiveControl:
    def __init__(self):
        self.horizon = 10

    def kiirendus(self, thrust, brake):
        return (3 * thrust) - (5 * brake) - 0.1

    #goal is to receive prev_temp and an input and to output the next temp (simulation)
    def plant_model(self, u, prev_speed):
        if u < 0:
            thrust = 0
            brake = abs(u)
        else:
            thrust = u
            brake = 0
        acceleration = self.kiirendus(thrust, brake)

        prev_speed += acceleration / dT

        return prev_speed

    def cost_function(self, u, input):
        cost = 0.0

        current_location, speed = input

        for i in range(0, self.horizon):
            speed = self.plant_model(u[i], speed)

            current_location += speed / dT
            if current_location < 200:
                ideal_speed = 25 / 3.6
            elif 200 <= current_location < 300:
                ideal_speed = 10 / 3.6
            elif 300 <= current_location < 500:
                ideal_speed = 30 / 3.6
            elif current_location >= 500:
                ideal_speed = 0


            cost += abs(speed - ideal_speed)
        return cost


mpc = ModelPredictiveControl()
dT = 10

# Set bounds.
bounds = []
for i in range(mpc.horizon):
    bounds += [[-1, 1]]

# Create Inputs to be filled.
u = np.ones(mpc.horizon)

sim_time = 120

u_list = []
speed_list = []
t_list = []
location_list = []
speed = 0.0
current_location = 0.0

for i in range(sim_time * dT):
    # Non-linear optimization.
    #set of inputs that make the lowest cost
    input = [current_location, speed]
    u_solution = minimize(mpc.cost_function,
                          x0=u,
                          args=input,
                          method='SLSQP',
                          bounds=bounds,
                          options={'maxiter': 200, 'ftol': 1e-07, 'iprint': 1, 'disp': True,
                                   'eps': 1e-03, 'finite_diff_rel_step': None},
                          tol = 1e-8)

    # --------------------------
    # Calculate data for Plot 1.

    current_location += speed / dT
    u = u_solution.x
    speed = mpc.plant_model(u[0], speed)
    t_list += [i]
    u_list += [u[0]]
    speed_list += [speed * 3.6]
    location_list += [current_location]
    np.delete(u, 0)
    np.append(u, 0)




    print(current_location)



#------------------------------------------------
# Plot 2 - MPC
# Subplot 1
plt.figure(figsize=(8,8))
plt.subplot(211)
plt.title("MPC")
plt.ylabel("Juhtimissignaal")
# Enter data
plt.plot(location_list, u_list, 'k')
plt.ylim(-1.5, 1.5)

# Subplot 2
plt.subplot(212)
plt.ylabel("Kiirus")
# Enter data
plt.plot(location_list, speed_list)
plt.ylim(0,40)
plt.show()
