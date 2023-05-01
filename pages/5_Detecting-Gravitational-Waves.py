import numpy as np
import altair as alt
import wave
from scipy.io import wavfile
import streamlit as st
import pandas as pd

import matplotlib
matplotlib.use('Agg')
matplotlib.rcParams['text.usetex'] = False
import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection
from matplotlib import animation
from matplotlib.patches import Circle

from matplotlib.backends.backend_agg import RendererAgg
lock = RendererAgg.lock

""" 
Remember the exercise in **Make-Waves** where you changed different parameters in a wave to see its effect on the waveform and its sound? What was the parameter that caused no change in the sound?


Yes, it was the _phase_ of the wave. The value that is determined by the starting point of the wave's creation, whether it was at a peak, a valley, or somewhere in between.       

But do not discount the phase as a boring, irrelevant parameter just yet!

While the gravitational wave amplitude and frequency tell us about the black holes that caused it, phase plays an important role in the actual detection of gravitational waves!

To understand why, let's dig into how LIGO works.

LIGO is the Laser _Interferometer_ Gravitational-wave Observatory. It is an _Interferometer_, which studies the interference between two laser beams that are shot along the two 4-km long arms of the L-shaped detector.


When the two beam paths are exactly equal in length, the light coming from the beams is designed to be exactly out of phase when it recombines at the center. This makes it interfere destructively, giving us zero signal at our photodetector.

However, a passing gravitational wave changes the length of one arm with respect to the other ever-so-slightly. This means the recombined laser beams are no longer perfectly out of phase, giving us a net signal that we can record as a gravitational wave.

The _phase difference_ between the laser beams coming from the two arms is hence what determines their relative displacement due to a gravitational wave, and thus the strength of that gravitational wave. 

In the following exercise, you will find an incoming light wave (orange) coming from one of the arms, which in this case is fixed. 

But you can shift the phase of the second light wave (blue) to be exactly matched that is interfere constructively, or exactly mismatched that is interfere destructively with the first wave - or some phase in between!

The moment you set a certain phase, the gravitational-wave photodetector will show the strength of the signal as a red output beam. If it's blank, the laser is in phase, the arms are of the same length, and there is no gravitational wave. But if you change the phase, see how the signal builds in the detector. At what point of phase does it become the strongest?        
"""
st.image("graphics/ligo.gif")

time = np.arange(0,10, 0.01)
t = np.linspace(0,4,4*44100)
A = 7.
freq = 1.
omega = 2*np.pi*freq
omega_audio = omega * 200
#phi1 = st.slider('Phase 1', min_value=0., max_value=np.pi)
phi1 = 0.0
W1 = A * np.sin(omega*time + phi1)
W1_audio = A * np.sin(omega_audio*t + phi1)
#source = ColumnDataSource(data=dict(x=time, y=W1))
source = pd.DataFrame({
'time': time,
'Wave amplitude': W1
})

wave_fixed = alt.Chart(source).mark_line(color='gold').encode(x='time', y=alt.Y('Wave amplitude', scale=alt.Scale(domain=[-20, 20]))).interactive()
st.altair_chart(wave_fixed, use_container_width=True)

col_phase, col_polar = st.columns([2,1])
with col_phase:
    phi2_deg = st.slider('Variable Phase (degrees)', min_value=0, max_value=360, step=5)
    phi2 = phi2_deg * np.pi/180
with col_polar:
    r = np.linspace(0, 1, 100)
    theta = np.ones(100) * phi2

    r0 = r
    theta0 = np.zeros(100)

    fig, ax = plt.subplots(subplot_kw={'projection': 'polar'})

    ax.patch.set_facecolor('red')
    ax.patch.set_alpha(abs(1-np.sin(phi2/2)))
    #ax.patch.set_alpha(np.cos(phi2)**2)

    ax.plot(theta, r, linewidth=4, color="blue")
    ax.plot(theta0, r0, linewidth=4, color="gold")
    ax.set_rmax(1)
    ax.set_rticks([])  # Less radial ticks
    #ax.set_rlabel_position(-22.5)  # Move radial labels away from plotted line
    ax.grid(True)

    ax.set_title("Phase", va='bottom', fontsize=20)
    plt.tight_layout()
    fig

W2 = A * np.sin(omega*time + phi2)
W2_audio = A * np.sin(omega_audio*t + phi2)

#source = ColumnDataSource(data=dict(x=time, y=W2))
source = pd.DataFrame({
'time': time,
'Wave amplitude': W2
})

wave_var = alt.Chart(source).mark_line(color='blue').encode(x='time', y=alt.Y('Wave amplitude', scale=alt.Scale(domain=[-20, 20]))).interactive()
st.altair_chart(wave_var, use_container_width=True)


# Set up plot
#plot2 = figure(height=200, width=800, title="Variable Phase Wave",
#      tools="crosshair,pan,reset,save,wheel_zoom",
#      x_range=[0, 4], y_range=[-20, 20])

#plot2.line('x', 'y', source=source, line_color='blue', line_width=3, line_alpha=0.6)

#plot2

# Phase difference plot:
W3 = W1 + W2

#source = ColumnDataSource(data=dict(x=time, y=W3))
source = pd.DataFrame({
'time': time,
'Wave amplitude': W3
})

wave_result = alt.Chart(source).mark_line(color='green').encode(x='time', y=alt.Y('Wave amplitude', scale=alt.Scale(domain=[-20, 20]))).interactive()
st.altair_chart(wave_result, use_container_width=True)


# Set up plot
#plot3 = figure(height=200, width=800, title="Resultant Wave after Interference",
#      tools="crosshair,pan,reset,save,wheel_zoom",
#      x_range=[0, 4], y_range=[-20, 20])
#plot3.xaxis.ticker = [0, np.pi, 2*np.pi]
#plot3.xaxis.major_label_overrides = {1: '0', 2: 'pi', 3: '2pi'}

#plot3.line('x', 'y', source=source, line_color='green', line_width=3, line_alpha=0.6)

#plot3

# t = np.linspace(0,l,l*rate)
# data = np.sin(2*np.pi*freq*t)*amp
W3_audio = (W1_audio + W2_audio) * 10000
W3_audio = W3_audio.astype('int16')
#        t, W_audio = const_note(freq*100, 4, amp = W3)
wavfile.write("temp/phase_audio.wav",44100,W3_audio)
st.audio("temp/phase_audio.wav")

