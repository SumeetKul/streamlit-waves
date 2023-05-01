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

st.header("Chirps!")


"""
Now that we have seen waves that change in amplitude alone or frequency alone, let us see an example where _both_ these quantities **increase** with time:
"""

t = np.arange(0,10,0.01)
A_chirp = np.power(1.3, t)
f_chirp = np.exp(t/12)

w_chirp = A_chirp*np.sin(2*np.pi*f_chirp*t)

#source = ColumnDataSource(data=dict(x=t, y=w_chirp))
source = pd.DataFrame({
'time': t,
'Wave amplitude': w_chirp
})

wave_chirp = alt.Chart(source).mark_line(color='seagreen').encode(x='time', y=alt.Y('Wave amplitude', scale=alt.Scale(domain=[-20, 20]))).interactive()
st.altair_chart(wave_chirp, use_container_width=True)

# Set up plot
#plot = figure(height=600, width=1000, title="Chirp",
#tools="crosshair,pan,reset,save,wheel_zoom",
#x_range=[0, 10], y_range=[-20, 20])

#plot.line('x', 'y', line_color='black', source=source, line_width=3, line_alpha=0.6)

#plot

"""
#### Sound #6
"""
t_audio = np.linspace(np.log(100),np.log(500),4*44100)
f_audio = np.exp(t_audio)
A_audio = np.power(1.2, t_audio)
t, W_audio = const_note(f_audio*1.5, 4, amp=A_audio*4000)
wavfile.write("temp/chirp_ex_audio.wav",44100,W_audio)
st.audio("temp/chirp_ex_audio.wav")


"""
This is called a chirp, being similar to the sound some birds make.


Do you know of any other thing(s) that make such a sound?


Since 2015, we also know of the chirp as the sound two black holes make.

Exactly one hundred years before LIGO’s discovery, Albert Einstein came up with a revolutionary new theory of gravity, the General Theory of Relativity. In it, Einstein said that space and time are not separate entities, but intertwined into a continuous fabric of space-time.

All massive bodies, such as the Earth, the Sun, and even yourselves are embedded inside this fabric, causing it to bend and curve. 

And Gravity is not a force that acts between these massive bodies, but a manifestation of the curvature of the fabric of spacetime.

As the nobel-prize winning physicist John Wheeler, who also coined the term ‘Black Hole’, succinctly put it: “Matter tells spacetime how to curve, Spacetime tells matter how to move”.

When the densest objects in our Universe, such as neutron stars and black holes move around in this fabric, they send out ripples known as Gravitational Waves.

This is how the spiral dance of two black holes orbiting one another creates gravitational waves!


So why the chirping waveform?
"""

st.image("graphics/cbc.png")
cbc_url = "https://www.soundsofspacetime.org/the-basics-of-binary-coalescence.html"
st.write(f"Image credit: [Sounds of Spacetime]({cbc_url})")

"""
As the two black holes are revolving around each other, their motion radiates gravitational waves. This causes them to lost energy through these waves, pulling them closer towards each other. 

As the separation between the black holes decreases, the conservation of angular momentum implies that they start revolving faster! Think of a ballet dancer spinning faster as she pulls in her arms and legs close together.

The faster motion of black holes as they come together increases the _frequency_ of their emitted gravitational waves, since the black holes complete more and more orbits around each other in a given amount of time. 

At the same time, the _amplitude_ of the emitted gravitational wave also increases, since the spacetime around them gets more and more curved as they are drawn together.


"""

st.image("graphics/bbh_starfield.gif")
bbh_gif_url = "https://www.ligo.caltech.edu/video/ligo20160211v3"
st.write(f"GIF credit: [LIGO Caltech]({bbh_gif_url})")
"""

Each pair of black holes, called a **Binary Black Hole (BBH)** system, thus leaves a characteristic imprint of gravitational waveforms as they spiral in and collide into one.
"""


