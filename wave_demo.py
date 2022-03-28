import streamlit as st
import numpy as np
from astropy.table import Table
import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection
from matplotlib import animation
from matplotlib.patches import Circle
from bokeh.layouts import column, row
from bokeh.models import ColumnDataSource, Slider, TextInput
from bokeh.plotting import figure
from pycbc.waveform import get_td_waveform, get_fd_waveform
from twirl.binary import Binary
from twirl.artists import BinaryBlackHole
import wave
from scipy.io import wavfile
import soundfile as sf

#from gwpy.timeseries import TimeSeries
import pandas as pd

"""
In September 2015, LIGO _observed_ two black holes spiraling into one another, and colliding to form one, larger black hole.

"""

#print(f'saving to {args.outfile}')
outfile = f"temp/gw150914.gif"
st.image(outfile)


"""
But rather than directly observing this event, LIGO detected Gravitational Waves, ripples in the fabric of spacetime given out by the motion of these dense and massive black holes. This is what the two LIGO detectors, one in Livingston, Louisiana, and the other in Hanford, Washington recorded on September 14, 2015.
"""

st.image("GW150914.png")

"""
How does this signal translate into two black holes colliding? What makes a Gravitational _Wave_? To understand, let’s dive into the nature and properties of waves.

"""

st.header("Introduction to Waves")



"""
Greetings! Say hello to this tutorial with a wave of your hand:
"""
st.image("wave.gif")

"""
You just made a wave! A wave is anything that moves back and forth, _oscillating_ in a periodic pattern as time goes by. We can make a chart of these oscillations with time, giving us a waveform of evenly spaced, alternating peaks and troughs. 


The peaks and troughs represent the extreme points of whatever is oscillating: your hand, water in a pond, or [....]

"""
time = np.arange(0,10, 0.01)

A = 5
omega = 4
phi = np.pi/2

W = A * np.sin(omega*time + phi)

fig = plt.figure(figsize=(10,6))

plt.plot(time, W)
plt.xlabel("time (seconds)")

fig

if st.checkbox("See the Math behind this"):

    """
    ---------------------------------------------------
    $ W = A \sin (\omega t + \phi)$

    Here, 

    **A** is the wave amplitude, **$\omega$** is the wave frequency, and **$\phi$** is the phase.

    ---------------------------------------------------
    """

"""
The wave **amplitude** represents the height of the peaks and troughs, i.e. the extent through which you are moving your hand.

The wave **frequency** represents the number of peaks and troughs in a given amount of time, i.e. how vigorously you are moving your hand.

If you are excited, you probably have a large amplitude as well as frequency.

Finally, the wave **phase** is just a measure of what point you start off your wave: whether at the center, extreme left, extreme right, or somewhere in between!

All sound, whether music or noise, is waves created by vibrating air around us. The air above a drum vibrates when you strike it, and these vibrations travel as a wave through the air between the drum and your ear, shaking your eardrum at the same frequency and registering as sound in our brain.

You may hear the sound wave plotted above makes here. 
"""
t_audio = np.arange(0,1,0.01e-3)
W_audio = A * np.sin(omega*1e5*t_audio + phi)
sf.write("temp/ex1_audio.wav",W_audio,4096)
st.audio("temp/ex1_audio.wav")


"""
Do you notice anything about the tone? Is it constant or varying?
"""


"""
#### You can make your own wave here by varying the amplitude, frequency and phase!
"""

A = st.slider('Amplitude', min_value=0, max_value=10)
omega = st.slider('Frequency', min_value=1, max_value=5)
phi = st.slider('Phase', min_value=0., max_value=np.pi)

W = A * np.sin(omega*time + phi)

source = ColumnDataSource(data=dict(x=time, y=W))


# Set up plot
plot = figure(height=600, width=1000, title="My Wave",
      tools="crosshair,pan,reset,save,wheel_zoom",
      x_range=[0, 10], y_range=[-12, 12])

plot.line('x', 'y', source=source, line_width=3, line_alpha=0.6)

plot

t_audio = np.arange(0,1,0.01e-3)
W_audio = A * np.sin(omega*1e5*t_audio + phi)
sf.write("temp/mywave_audio.wav",W_audio,4096)
st.audio("temp/mywave_audio.wav")

"""
 Listen carefully to the audio of the wave as you change the parameters.
What makes the audio sound louder? What makes it sound deeper?
Does changing the phase modify the sound?
"""

"""
Waves are thus all around us - they make up the sound of music, and the cacophony of noise. But they do not typically look like the perfect, sinusoidal oscillations shown in the graphs above. 

Think of an ambulance siren. Its loudness varies, as does its frequency or pitch. 

"""

st.audio("ambulance-siren.m4a")




#chirp_option = st.sidebar.selectbox("Select Chirp tutorial", ["Chirp Demo", "Chirp Game"])

#if chirp_option == "Chirp Demo":
#        
#        """
#
#        ### This is a chirp
#        """
#        
#        m1 = 30
#        m2 = 28
#        
#        """
#        Mass 1 = 30 $M_{\odot}$ \n
#        Mass 2 = 28 $M_{\odot}$
#        """
#        
#        hp, hc = get_td_waveform(approximant="IMRPhenomD",
#                 mass1=m1,
#                 mass2=m2,
#                 coa_phase=np.pi,
#                 delta_t=1.0/2048,
#                 f_lower=40.)
#        
#        h = np.sqrt(hp**2 + hc**2)
#        
#        n_samples = hp.shape[0]
#        sample_rate = 2048
#        
#        seglen = n_samples/sample_rate
#        
#        time = np.linspace(-seglen, 0, n_samples)
#        
#        source = ColumnDataSource(data=dict(x=time, y=hp))
#
#
#        # Set up plot
#        plot = figure(height=600, width=1000, title="my sine wave",
#              tools="crosshair,pan,reset,save,wheel_zoom")
#
#        plot.line('x', 'y', source=source, line_width=3, line_alpha=0.6)
#        #plot.xlabel("time (seconds)")
#        #plot.ylabel("Gravitational Wave strength")
#        plot
#
#
#        #f = plt.figure(figsize=(12,4))
#        #plt.plot(time,hp)
#        #plt.xlabel("time (seconds)")
#        #plt.ylabel("Gravitational Wave strain")
#        #f
#        #ts = TimeSeries.from_pycbc(hp)
#
#if chirp_option == "Chirp Game":
#        """
#        
#        ### You can make your own chirp!
#        """
#        
#        m1 = st.slider('Mass 1', min_value=20, max_value=50)
#        m2 = st.slider('Mass 2', min_value=10, max_value=40)
#        
#        hp, hc = get_td_waveform(approximant="IMRPhenomD",
#                 mass1=m1,
#                 mass2=m2,
#                 coa_phase=np.pi,
#                 delta_t=1.0/2048,
#                 f_lower=20.)
#        
#        hp1, hc1 = get_td_waveform(approximant="IMRPhenomD",
#                 mass1=30,
#                 mass2=28,
#                 coa_phase=np.pi,
#                 delta_t=1.0/2048,
#                 f_lower=20.)
#        
#        n_samples = hp.shape[0]
#        sample_rate = 2048
#        
#        seglen = n_samples/sample_rate
#        
#        time = np.linspace(-seglen, 0, n_samples)
#        
#        ref_samples = hp1.shape[0]
#        sample_rate = 2048
#        
#        seglen1 = ref_samples/sample_rate
#        
#        time1 = np.linspace(-seglen1, 0, ref_samples)
#        
#        hp_norm = hp / np.linalg.norm(hp)
#        hp1_norm = hp1 / np.linalg.norm(hp1)
#        #conv = np.convolve(hp, hp1)
#        match = np.round(np.max(abs(np.correlate(hp_norm, hp1_norm))), 2)
#         
#        def result_statement(match):
#            if 0.0 < match <= 0.25:
#                rs = "Different chirps, try again!"
#            elif 0.25 < match <= 0.5:
#                rs = "Slight overlap, try again!"
#            elif 0.5 < match <= 0.75:
#                rs = "Getting closer... try again!"
#            elif 0.75 < match < 1.0:
#                rs = "Almost there... try again!"
#            elif match == 1.0:
#                rs = "Perfect!"
#            return rs
#                
#        source = ColumnDataSource(data=dict(x=time, y=hp))
#        source1 = ColumnDataSource(data=dict(x1=time1, y1=hp1))
#
#        # Set up plot
#        plot = figure(height=600, width=1000, title="GW match chirp",
#              tools="crosshair,pan,reset,save,wheel_zoom", x_range=[-2, 0])
#
#        plot.line('x', 'y', source=source, line_width=3, line_alpha=0.9)
#        plot.line('x1', 'y1', source=source1, line_width=3, line_color='black', line_alpha=0.6, line_dash='dashed')
#        #plot.xlabel("time (seconds)")
#        #plot.ylabel("Gravitational Wave strength")
#        plot
#
#
#        f = plt.figure(figsize=(12,4))
#        plt.plot(time1,hp1)
#        plt.plot(time, hp, c='black', linestyle="--", label=f"{result_statement(match)}")
#        plt.xlabel("time (seconds)")
#        plt.xlim(-2.0,0.0)
#        plt.ylabel("Gravitational Wave strain")
#        plt.legend(fontsize=24)
#        f
#        


