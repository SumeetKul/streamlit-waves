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

st.header("Waves in Nature")


# Real-life waves: varying frequencies and amplitudes:

"""
Waves are thus all around us - they make up the sound of music, and the cacophony of noise. But they do not typically look like the perfect, sinusoidal oscillations shown in the graphs above. 

Think of an ambulance siren. Its loudness varies, as does its frequency or pitch. 

"""

st.audio("audio/ambulance-siren.mp3")

"""
The waveform of a siren looks like this. Can you see the variation in frequency and amplitude here?
"""

t = np.arange(4096)/1024
A_siren = np.sin(2*np.pi*0.5*t)
f_siren = np.sin(2*np.pi*0.7*t)

w_siren = A_siren*np.sin(2*np.pi*f_siren*t)

#source = ColumnDataSource(data=dict(x=t, y=w_siren))
source = pd.DataFrame({
'time': t,
'Wave amplitude': w_siren
})

wave_var = alt.Chart(source).mark_line().encode(x='time', y=alt.Y('Wave amplitude', scale=alt.Scale(domain=[-2, 2])))
st.altair_chart(wave_var, use_container_width=True)


# Set up plot
#plot = figure(height=600, width=1000, title="Ambulance Siren",
#      tools="crosshair,pan,reset,save,wheel_zoom",
#      x_range=[0, 4], y_range=[-2, 2])

#plot.line('x', 'y', source=source, line_width=3, line_color='crimson', line_alpha=0.6)

#plot

"""
What happens when you have a constant frequency but varying amplitude?
"""

t = np.arange(0,10,0.01)
A_amp = 2 + np.sin(2*np.pi*0.5*t)
f_amp = 5

w_amp = A_amp*np.sin(2*np.pi*f_amp*t)

# source = ColumnDataSource(data=dict(x=t, y=w_amp))
source = pd.DataFrame({
'time': t,
'Wave amplitude': w_amp
})

wave_var = alt.Chart(source).mark_line().encode(x='time', y=alt.Y('Wave amplitude', title="Varying Amplitude", scale=alt.Scale(domain=[-4, 4])))
st.altair_chart(wave_var, use_container_width=True)

# Set up plot
#plot = figure(height=600, width=1000, title="Varying Amplitude",
#      tools="crosshair,pan,reset,save,wheel_zoom",
#      x_range=[0, 8], y_range=[-4, 4])

#plot.line('x', 'y', source=source, line_color='green', line_width=3, line_alpha=0.6)

#plot

"""
#### Sound #3
"""

t_audio = np.linspace(0,4,4*44100)
A_audio = 2+np.sin(2*np.pi*1*t_audio)
t, W_audio = const_note(500, 4, amp=A_audio * 10000)
wavfile.write("temp/var_amp_audio.wav",44100,W_audio)
st.audio("temp/var_amp_audio.wav")

if st.checkbox("See the Math behind varying amplitude waves"):

    """
    ---------------------------------------------------
    $ W = A(t) \sin (2 \pi f t + \phi) $

    $ A(t) = \sin (2 \pi f_{amp} t) $

    Here, 

    **A(t)** is the time-varying (oscillating) wave amplitude. The Amplitude itself can be a sinusoidally oscillating function, with it's own frequency, $f_{amp}$, which is different from the frequency of the wave itself (**f**). **$\phi$**, as before, is the phase.

    ---------------------------------------------------
    """

"""
Can you think of any real-life examples where you encounter such a sound?

Now, let us keep the amplitude constant but change the frequency, to make the frequency steadily increase or decrease with time:
"""

#if st.checkbox("Decreasing frequency:"):
""" **Decreasing** frequency """

t = np.arange(0,10,0.01)
A = 3
f_red = np.flip(np.power(2, t/10))

w_red = A*np.sin(2*np.pi*f_red*t)

#source = ColumnDataSource(data=dict(x=t, y=w_red))
source = pd.DataFrame({
'time': t,
'Wave amplitude': w_red
})

wave_var = alt.Chart(source).mark_line(color='red').encode(x='time', y=alt.Y('Wave amplitude', scale=alt.Scale(domain=[-4, 4]))).interactive()
st.altair_chart(wave_var, use_container_width=True)

# Set up plot
#plot = figure(height=600, width=1000, title="Redshift",
#tools="crosshair,pan,reset,save,wheel_zoom",
#x_range=[0, 10], y_range=[-4, 4])

#plot.line('x', 'y', line_color='red', source=source, line_width=3, line_alpha=0.6)

#plot
"""
#### Sound #4
"""

t_audio = np.flip(np.linspace(np.log(100),np.log(1000),4*44100))
f_audio = np.exp(t_audio)
t, W_audio = const_note(f_audio*2, 4, amp=5000)
wavfile.write("temp/redshift_audio.wav",44100,W_audio)
st.audio("temp/redshift_audio.wav")

#if st.checkbox("Increasing frequency:"):
""" **Increasing** frequency """

t = np.arange(0,10,0.01)
A = 3
f_blue = np.power(2, t/10)

w_blue = A*np.sin(2*np.pi*f_blue*t)

#source = ColumnDataSource(data=dict(x=t, y=w_blue))
source = pd.DataFrame({
'time': t,
'Wave amplitude': w_blue
})

wave_var = alt.Chart(source).mark_line(color='blue').encode(x='time', y=alt.Y('Wave amplitude', scale=alt.Scale(domain=[-4, 4])))
st.altair_chart(wave_var, use_container_width=True)

# Set up plot
#plot = figure(height=600, width=1000, title="Blueshift",
#tools="crosshair,pan,reset,save,wheel_zoom",
#x_range=[0, 10], y_range=[-4, 4])

#plot.line('x', 'y', line_color='blue', source=source, line_width=3, line_alpha=0.6)

#plot
"""
#### Sound #5
"""
t_audio = np.linspace(np.log(200),np.log(800),4*44100)
f_audio = np.exp(t_audio)
t, W_audio = const_note(f_audio*2, 4, amp=5000)
wavfile.write("temp/blueshift_audio.wav",44100,W_audio)
st.audio("temp/blueshift_audio.wav")


if st.checkbox("See the Math behind varying frequency waves"):

    """
    ---------------------------------------------------
    $ W = A \sin (2 \pi f(t) t + \phi) $

    $ f(t) = e^{t} $

    Here, 

    the wave amplitude **A** is fixed, but the frequency **f(t)** is an exponentially increasing function of time. **$\phi$**, as before, is the phase.

    ---------------------------------------------------
    """


"""
Does this remind you of the whistle of an approaching or receding train? 
Even though the frequency of a train whistle is constant just like our first wave example, the frequency of the sound you hear changes as the train moves towards you or away from you, due to a phenomenon called the ‘Doppler effect’.
"""
