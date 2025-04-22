import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import hilbert

def generate_message_signal(t, freq=0.1):
    # Generate a simple message signal (e.g., an audio tone)
    return np.sin(2 * np.pi * freq * t)

def am_modulate(message, carrier_freq, t, modulation_index=0.5):
    # Modulate the message onto a carrier
    carrier = np.sin(2 * np.pi * carrier_freq * t)
    return (1 + modulation_index * message) * carrier

def envelope_detector_improved(modulated_signal):
    """
    Better envelope detector using Hilbert transform
    This provides a much more accurate envelope extraction
    """
    # Get the analytic signal (signal + j*hilbert_transform)
    analytic_signal = hilbert(modulated_signal)
    # Magnitude of analytic signal gives the envelope
    envelope = np.abs(analytic_signal)
    # Remove DC offset (approximation)
    envelope = envelope - np.mean(envelope)
    # Scale to match original amplitude
    scaling_factor = np.max(np.abs(modulated_signal)) / np.max(np.abs(envelope))
    return envelope * scaling_factor

# Time and frequency parameters - improved resolution
t = np.linspace(0, 1, 50000)  # Higher resolution for better results
message_freq = 5    # Hz - frequency of the message signal
carrier_freq = 100  # Hz - frequency of the carrier wave

# Generate message and modulated signals
message = generate_message_signal(t, message_freq)
modulated = am_modulate(message, carrier_freq, t, modulation_index=0.8)

# Demodulate with improved detector
demodulated = envelope_detector_improved(modulated)

# Create plot with multiple subplots
fig, axs = plt.subplots(3, 1, figsize=(12, 10))

# Plot message signal
axs[0].plot(t, message, 'b-')
axs[0].set_title('Message Signal (5 Hz)', fontsize=12)
axs[0].set_ylabel('Amplitude', fontsize=10)
axs[0].set_xlim(0, 0.5)  # Show only half of the signal for better visibility
axs[0].grid(True, alpha=0.7)

# Plot modulated signal
axs[1].plot(t, modulated, 'g-')
axs[1].set_title('Amplitude Modulated Signal (100 Hz carrier)', fontsize=12)
axs[1].set_ylabel('Amplitude', fontsize=10)
axs[1].set_xlim(0, 0.5)
axs[1].grid(True, alpha=0.7)

# Plot demodulated signal and original message for comparison
axs[2].plot(t, demodulated, 'r-', label='Demodulated')
axs[2].plot(t, message, 'b--', label='Original Message')
axs[2].set_title('Demodulated Signal vs Original Message', fontsize=12)
axs[2].set_xlabel('Time (s)', fontsize=10)
axs[2].set_ylabel('Amplitude', fontsize=10)
axs[2].set_xlim(0, 0.5)
axs[2].legend(fontsize=10)
axs[2].grid(True, alpha=0.7)

plt.tight_layout()
plt.savefig('figure_3.png', dpi=300, bbox_inches='tight')

plt.show()

# Also create a zoomed plot to show carrier wave
plt.figure(figsize=(10, 6))
plt.plot(t, modulated, 'g-')
plt.title('Zoomed View of AM Signal', fontsize=14)
plt.xlabel('Time (s)', fontsize=12)
plt.ylabel('Amplitude', fontsize=12)
plt.xlim(0, 0.05)  # Show only a small portion to see carrier waves clearly
plt.grid(True, alpha=0.7)
plt.tight_layout()
plt.show()