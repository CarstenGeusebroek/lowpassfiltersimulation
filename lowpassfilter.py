#Alle wiskunde en natuurkunde die hierbij hoort staat uitgelegd in ons verslag

import numpy as np
import matplotlib.pyplot as plt

# PWM parameters
pwm_frequency = 490
period = 1 / pwm_frequency
duty_cycle = 0.2              
input_voltage = 5.0           
average_pwm = duty_cycle * input_voltage  

# Low-pass filter parameters zoals ze in het echt zijn
R = 320                     # 320 Ω resistor
C = 100e-6                      # 100 µF capacitor
RC_constant = R * C

# Simulatie parameters
sampling_rate = 2000       
dt = 1 / sampling_rate        
total_time = 0.25              

output_voltage = 0.0         
time_points = np.arange(0, total_time, dt)
pwm_values = []             
output_voltages = []          

plt.ion()  
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(8, 6))
plt.subplots_adjust(left=None, bottom=None, right=None, top=None, wspace=None, hspace=0.4)

ax1.set_xlim(0, total_time)
ax1.set_ylim(-0.5, input_voltage + 0.5)
ax1.set_xlabel("Time (s)")
ax1.set_ylabel("PWM Signal (V)")
ax1.set_title("PWM Signal")
pwm_line, = ax1.plot([], [], 'r-', lw=1)

ax2.set_xlim(0, total_time)
ax2.set_ylim(0, input_voltage)
ax2.set_xlabel("Time (s)")
ax2.set_ylabel("Filtered Output Voltage (V)")
ax2.set_title("Filtered Output Voltage of PWM Signal")
output_line, = ax2.plot([], [], 'b-', lw=2)

#Horizontal line for the average
ax2.axhline(y=average_pwm, color='g', linestyle='--', label=f"Average PWM = {average_pwm:.2f} V")
ax2.legend()

alpha = dt / (RC_constant + dt)

for t in time_points:
    #Calculate the current voltage from the pwm signal
    pwm_value = input_voltage if (t % period) < (duty_cycle * period) else 0.0
    pwm_values.append(pwm_value)
    
    #Simulate the output voltage with respect to time
    output_voltage = alpha * pwm_value + (1-alpha) * output_voltage
    output_voltages.append(output_voltage)
    
    # Update the plots
    pwm_line.set_data(time_points[:len(pwm_values)], pwm_values)
    output_line.set_data(time_points[:len(output_voltages)], output_voltages)
    
    # Redraw the plots
    ax1.draw_artist(ax1.patch)
    ax1.draw_artist(pwm_line)
    ax2.draw_artist(ax2.patch)
    ax2.draw_artist(output_line)
    fig.canvas.flush_events()  # Update plot

plt.ioff()  # Turn off interactive mode
plt.show()  # Keep the plot open after the loop
