import numpy as np
import matplotlib.pyplot as plt

def calculate_frequency_response(L, R, C, freq_range):
    # Calculate impedance at each frequency
    Z = []
    for f in freq_range:
        omega = 2 * np.pi * f
        Z_L = 1j * omega * L        # Inductor impedance
        Z_C = 1 / (1j * omega * C)  # Capacitor impedance
        Z_total = R + Z_L + Z_C     # Total series impedance
        Z.append(abs(Z_total))      # Magnitude of impedance
    
    return np.array(Z)

# Circuit parameters
L = 1.0  # Inductance in henries
C = 1.0  # Capacitance in farads

# Different resistance values
R_under = 0.5  # Low R gives sharp resonance peak
R_crit = 2.0   # Medium R
R_over = 4.0   # High R flattens the response

# Frequency range (logarithmic scale to better show resonance)
freq_range = np.logspace(-1, 1, 1000)  # 0.1 Hz to 10 Hz

# Calculate resonant frequency
f_resonant = 1 / (2 * np.pi * np.sqrt(L * C))
print(f"Resonant frequency: {f_resonant:.3f} Hz")

# Calculate frequency responses for different R values
Z_under = calculate_frequency_response(L, R_under, C, freq_range)
Z_crit = calculate_frequency_response(L, R_crit, C, freq_range)
Z_over = calculate_frequency_response(L, R_over, C, freq_range)

# Create plot with better styling
plt.figure(figsize=(10, 6))
plt.loglog(freq_range, Z_under, 'b-', linewidth=2, label=f'Underdamped R={R_under} Ω')
plt.loglog(freq_range, Z_crit, 'orange', linewidth=2, label=f'Critical damped R={R_crit} Ω')
plt.loglog(freq_range, Z_over, 'g-', linewidth=2, label=f'Overdamped R={R_over} Ω')

# Mark the resonant frequency with a vertical line
plt.axvline(x=f_resonant, color='r', linestyle='--', linewidth=1.5,
            label=f'Resonant frequency: {f_resonant:.3f} Hz')

# Add plot details with improved formatting
plt.xlabel('Frequency (Hz)', fontsize=12)
plt.ylabel('Impedance (Ω)', fontsize=12)
plt.title('Frequency Response of Series LRC Circuit', fontsize=14)
plt.grid(True, which="both", ls="--", alpha=0.7)
plt.legend(fontsize=10)
plt.tight_layout()

# Set appropriate axis limits
plt.xlim(0.1, 10)
plt.ylim(0.4, 100)  # Adjust as needed to match your plot
plt.savefig('figure_2.png', dpi=300, bbox_inches='tight')

plt.show()