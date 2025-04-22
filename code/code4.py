import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider

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

# Create figure with larger size for better visibility
fig, ax = plt.subplots(figsize=(10, 6))
plt.subplots_adjust(bottom=0.25)  # Make room for slider

# Fixed parameters
L = 1.0  # Inductance
R = 0.1  # Resistance (low for sharp resonance)

# Variable capacitance
C_min, C_max = 0.1, 10.0
C_init = 1.0

# Frequency range
freq_range = np.logspace(-1, 1, 1000)

# Initial frequency response
Z = calculate_frequency_response(L, R, C_init, freq_range)

# Use semilogx for better visualization of the frequency response
line, = ax.semilogx(freq_range, Z, 'b-', linewidth=2)

# Resonant frequency marker
f_res = 1 / (2 * np.pi * np.sqrt(L * C_init))
resonance_marker, = ax.plot([f_res], [min(Z)], 'ro')

# Add text annotation for resonant frequency
resonance_text = ax.text(f_res, min(Z)*0.8, f'f_res = {f_res:.3f} Hz', 
                        ha='center', va='bottom', color='red', fontsize=10,
                        bbox=dict(facecolor='white', alpha=0.7, edgecolor='none'))

# Set up the plot with improved styling
ax.set_xscale('log')
ax.set_xlabel('Frequency (Hz)', fontsize=12)
ax.set_ylabel('Impedance (Ω)', fontsize=12)
ax.set_title('LRC Circuit Frequency Response', fontsize=14)
ax.grid(True, which="both", ls="--", alpha=0.7)

# Set fixed y-axis limits to prevent jumping during updates
ax.set_ylim(0, 70)  # Based on your screenshot

# Add slider for capacitance - make it more visible
ax_slider = plt.axes([0.25, 0.1, 0.65, 0.03], facecolor='lightgoldenrodyellow')
slider = Slider(ax_slider, 'Capacitance (F)', C_min, C_max, 
               valinit=C_init, valstep=0.1, color='blue')

# Update function for slider with improved handling
def update(val):
    C = slider.val
    Z = calculate_frequency_response(L, R, C, freq_range)
    line.set_ydata(Z)
    
    # Update resonant frequency marker
    f_res = 1 / (2 * np.pi * np.sqrt(L * C))
    min_Z = min(Z)
    
    # Update marker position
    resonance_marker.set_data([f_res], [min_Z])
    
    # Update text position and content
    resonance_text.set_position((f_res, min_Z*0.8))
    resonance_text.set_text(f'f_res = {f_res:.3f} Hz')
    
    # Don't change y-limits during update to prevent jumping
    # This fixes the non-interactivity issue
    
    fig.canvas.draw_idle()

# Connect the update function to the slider
slider.on_changed(update)

plt.savefig('figure_4.png', dpi=300, bbox_inches='tight')
# Force an initial draw
plt.show()
# NOTE: Interactive on stand-alone script