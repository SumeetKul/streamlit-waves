import numpy as np
import altair as alt
import wave
from scipy.io import wavfile
import streamlit as st
import pandas as pd
#from scipy import signal


def const_note(freq, l, amp=10000, rate=44100):
    t = np.linspace(0,l,l*rate)
    data = np.sin(2*np.pi*freq*t)*amp
    return t, data.astype('int16') # two byte integers

def var_note(freq, l, amp, rate=44100):
    t = np.linspace(0,l,l*rate)
    data = np.sin(2*np.pi*freq*t)*amp
    return t, data.astype('int16') # two byte integers


st.header("Introduction to Waves")



"""
Greetings! Say hello to this tutorial with a wave of your hand:
"""
st.image("graphics/wave.gif")

"""
You just made a wave! A wave is caused by anything that moves back and forth, _oscillating_ in a periodic pattern as time goes by. We can make a chart of these oscillations with time, giving us a waveform of evenly spaced, alternating peaks and troughs. 


The peaks and troughs represent the extreme points of whatever is oscillating: your hand, water in a pond, or a pendulum. 

"""
time = np.arange(0,10, 0.01)

A = 5
f = 0.44
omega = 2*np.pi*f
phi = np.pi/2

W = A * np.sin(omega*time + phi)

source = pd.DataFrame({
'time': time,
'Wave amplitude': W
})

wave_1 = alt.Chart(source).mark_line().encode(x='time', y=alt.Y('Wave amplitude', scale=alt.Scale(domain=[-6, 6])))
st.altair_chart(wave_1, use_container_width=True)

if st.checkbox("See the Math behind this"):

    """
    ---------------------------------------------------
    $ W = A \sin (2 \pi f t + \phi)$

    Here, 

    **A** is the wave amplitude, **f** is the wave frequency, and **$\phi$** is the phase. **t** denotes the time.
    
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

"""
#### Sound #1
"""
t, W_audio = const_note(440, 4)
wavfile.write("const_waves_audio.wav",44100,W_audio)
st.audio("audio/const_waves_audio.wav")


"""
Do you notice anything about the tone? Is it constant or varying?
"""


"""
#### You can make your own wave here by varying the amplitude, frequency and phase!
"""

A = st.slider('Amplitude', min_value=0, max_value=10)
freq = st.slider('Frequency', min_value=1., max_value=5.)
omega = 2*np.pi*freq
phi = st.slider('Phase', min_value=0., max_value=np.pi)

W = A * np.sin(omega*time + phi)

#        source = ColumnDataSource(data=dict(x=time, y=W))
source = pd.DataFrame({
'time': time,
'Wave amplitude': W
})

wave_var = alt.Chart(source).mark_line().encode(x='time', y=alt.Y('Wave amplitude', scale=alt.Scale(domain=[-6, 6])))
st.altair_chart(wave_var, use_container_width=True)

"""
#### Sound #2
"""

t, W_audio = const_note(freq*100, 4, amp = A*4000)
wavfile.write("temp/const_waves_exercise_audio.wav",44100,W_audio)
st.audio("temp/const_waves_exercise_audio.wav")

#t_audio = np.linspace(0,4,4*4096)
#f_audio = 2*np.pi/omega * 2e5 # scale to KHz.
#W_audio = A * np.sin(2*np.pi*f_audio*t_audio + phi)
#wavfile.write("temp/mywave_audio.wav",1024, W_audio)
#st.audio("temp/ex2.wav")

"""
 Listen carefully to the audio of the wave as you change the parameters.
What makes the audio sound louder? What makes it sound deeper?
Does changing the phase modify the sound?
"""

