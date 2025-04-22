import numpy as np
from scipy.integrate import solve_ivp
import matplotlib.pyplot as plt

# Step voltage function - returns V0 when t >= t0, otherwise 0
def step_voltage(t, V0=1.0, t0=0):
    return V0 if t >= t0 else 0

# Function defining the series LRC system differential equations
def series_lrc_system(t, y, L, R, C, V_func):
    # y[0] is current, y[1] is derivative of current
    dydt = np.zeros(2)
    dydt[0] = y[1]  # dI/dt = y[1]
    # L * d²I/dt² + R * dI/dt + (1/C) * I = dV/dt
    # Rearranged to solve for d²I/dt²:
    dydt[1] = (V_func(t) - R * y[1] - (1/C) * y[0]) / L
    return dydt

# Circuit parameters
L = 1.0  # Inductance in henries
C = 1.0  # Capacitance in farads

# Different resistance values for different damping scenarios
R_under = 0.5  # Underdamped (R < 2*sqrt(L/C))
R_crit = 2.0   # Critically damped (R = 2*sqrt(L/C))
R_over = 4.0   # Overdamped (R > 2*sqrt(L/C))

# Time span
t_span = (0, 20)
t_eval = np.linspace(*t_span, 1000)
initial_conditions = [0, 0]  # No initial current or derivative

# Solve for each damping case
results_under = solve_ivp(
    lambda t, y: series_lrc_system(t, y, L, R_under, C, lambda t: step_voltage(t, 1.0)),
    t_span, initial_conditions, t_eval=t_eval, method='RK45')

results_crit = solve_ivp(
    lambda t, y: series_lrc_system(t, y, L, R_crit, C, lambda t: step_voltage(t, 1.0)),
    t_span, initial_conditions, t_eval=t_eval, method='RK45')

results_over = solve_ivp(
    lambda t, y: series_lrc_system(t, y, L, R_over, C, lambda t: step_voltage(t, 1.0)),
    t_span, initial_conditions, t_eval=t_eval, method='RK45')

# Calculate the natural frequency for reference
omega_n = 1 / np.sqrt(L * C)
f_n = omega_n / (2 * np.pi)
print(f"Natural frequency: {f_n:.3f} Hz")

# Create plot to compare all three cases with improved styling
plt.figure(figsize=(12, 8))
plt.plot(results_under.t, results_under.y[0], 'b-', linewidth=2, 
         label=f'Underdamped (R={R_under})')
plt.plot(results_crit.t, results_crit.y[0], 'r-', linewidth=2, 
         label=f'Critically damped (R={R_crit})')
plt.plot(results_over.t, results_over.y[0], 'g-', linewidth=2, 
         label=f'Overdamped (R={R_over})')

# Add reference line for steady-state value
plt.axhline(y=1.0, linestyle='--', color='k', alpha=0.5, 
            label='Steady-state (1.0 A)')

# Add annotations to highlight features
plt.annotate('Oscillations', xy=(5, 0.8), xytext=(5, 0.4),
             arrowprops=dict(facecolor='blue', shrink=0.05), color='blue')

plt.annotate('No overshoot', xy=(3, 0.6), xytext=(5, 0.2),
             arrowprops=dict(facecolor='green', shrink=0.05), color='green')

# Add plot details
plt.xlabel('Time (s)', fontsize=12)
plt.ylabel('Current (A)', fontsize=12)
plt.title('Step Response of Series LRC Circuit', fontsize=14)
plt.grid(True, alpha=0.7)
plt.legend(fontsize=10)
plt.tight_layout()

# Set appropriate y-axis limits
plt.ylim(-0.6, 1.5)  # Show the full range of oscillations
# After creating each plot, add:
plt.savefig('figure_1.png', dpi=300, bbox_inches='tight')
plt.show()