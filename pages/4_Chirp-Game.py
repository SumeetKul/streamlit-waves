import streamlit as st
import numpy as np
from astropy.table import Table

#import streamlit_analytics

import matplotlib
matplotlib.use('Agg')
matplotlib.rcParams['text.usetex'] = False
import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection
from matplotlib import animation
from matplotlib.patches import Circle

from matplotlib.backends.backend_agg import RendererAgg
lock = RendererAgg.lock

import altair as alt
from bokeh.layouts import column, row
from bokeh.models import ColumnDataSource, Slider, TextInput
from bokeh.plotting import figure


import pandas as pd
from pycbc.waveform import get_td_waveform, get_fd_waveform
from pycbc.filter import matchedfilter
import binary
import artists
import wave
from scipy.io import wavfile
from scipy import signal
import lal

def const_note(freq, l, amp=10000, rate=44100):
    t = np.linspace(0,l,l*rate)
    data = np.sin(2*np.pi*freq*t)*amp
    return t, data.astype('int16') # two byte integers

def var_note(freq, l, amp, rate=44100):
    t = np.linspace(0,l,l*rate)
    data = np.sin(2*np.pi*freq*t)*amp
    return t, data.astype('int16') # two byte integers

#streamlit_analytics.start_tracking()

#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%#
################################################# Part 2: Chirp Game #######################################################################################
#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%#

"""
#### Find the masses of binary black holes from some of the standout Gravitational-wave events detected by LIGO-Virgo.
"""

t = Table.read("chirp_events/GW_event_info.dat", format='ascii')

event_option = st.selectbox("Select Gravitational-wave event", t["name"])

event = t[t["name"]==event_option]
mass1_event = event["mass1"][0]
mass2_event = event["mass2"][0]

f"""
**{event["description"][0]}**

The gravitational-wave waveform for {event["name"][0]} can be seen as the blue waveform in the plot below.

Adjust the two black hole masses using the sliders, and see the binary black hole system in motion! You can also see the corresponding waveform for this binary you've created as the dashed black waveform in the plot.

Your task is to explore the mass parameters of the binary black hole to match your waveform with the {event["name"][0]} waveform. This will tell you how heavy {event["name"][0]}'s masses were!

As you try different mass combinations, keep a keen eye on what is happening to the dashed-line chirp. How do the amplitude and duration of the chirp vary with the individual black hole masses? What kind of chirp does a pair of lightweight or heavyweight black holes give? What if the black hole masses are extremely unbalanced?
"""

m1 = st.slider("Mass 1", min_value=5, max_value=50, value=20)
m2 = st.slider('Mass 2', min_value=5, max_value=50, value=20)

hp1, hc1 = get_td_waveform(approximant="IMRPhenomD",
	 mass1=m1,
	 mass2=m2,
	 coa_phase=np.pi,
	 delta_t=1.0/2048,
	 f_lower=20.)

#@st.cache(hash_funcs={lal.LIGOTimeGPS: (-3, -800000000)})
def load_event(mass1_event, mass2_event):
    hp, hc = get_td_waveform(approximant="IMRPhenomD",
	     mass1=mass1_event,
	     mass2=mass2_event,
	     coa_phase=np.pi,
	     delta_t=1.0/2048,
	     f_lower=20.)
    return hp, hc

hp, hc = load_event(mass1_event, mass2_event)
n_samples = hp.shape[0]
sample_rate = 2048

seglen = n_samples/sample_rate

time = np.linspace(-seglen, 0, n_samples)

hc1.resize(n_samples)
#print(hp1)
ref_samples = hp1.shape[0]
#sample_rate = 1024

seglen1 = ref_samples/sample_rate

time1 = np.linspace(-seglen1, 0, ref_samples)

match = np.round(matchedfilter.match(hc, hc1)[0],2)
#print(match)
st.text(f"match = {int(match*100)}%")
def result_statement(match):
    if 0.0 < match <= 0.25:
        rs = "Different chirps, try again!"
        rc = "red"
    elif 0.25 < match <= 0.5:
        rs = "Slight overlap, try again!"
        rc = "darkorange"
    elif 0.5 < match <= 0.75:
        rs = "Getting closer... try again!"
        rc = "orange"
    elif 0.75 < match < 1.0:
        rs = "Almost there... try again!"
        rc = "gold"
    elif match == 1.0:
        st.balloons()
        #st.success("Match found!")
        rs = "Perfect!"
        rc = "green"
    else:
        rs = "Calculating Match..."
        rc = "black"
    return rs, rc

source = ColumnDataSource(data=dict(x=time, y=hp))
#source = pd.DataFrame({
#'time': time,
#'Gravitational Wave amplitude': hp
#})

source1 = ColumnDataSource(data=dict(x1=time1, y1=hp1))
#source1 = pd.DataFrame({
#'time': time,
#'Gravitational Wave amplitude': hp1
#})

col_anim, col_plot = st.columns([1,2])
with col_plot:
	# Set up plot
        plot = figure(height=300, width=800, title="GW match chirp",
               tools="crosshair,pan,reset,save,wheel_zoom", x_range=[-4, 0])

        plot.title.text = result_statement(match)[0]
        plot.title.align = "center"
        plot.title.text_color =  result_statement(match)[1]
        plot.title.text_font_size = "25px"

        #wave_orig = alt.Chart(source).mark_line(color='blue').encode(x='time', y=alt.Y('Gravitational Wave amplitude', scale=alt.Scale(domain=[-20, 20]))).interactive()
        #st.altair_chart(wave_orig, use_container_width=True)

        plot.line('x', 'y', source=source, line_width=3, line_alpha=0.9)
        plot.line('x1', 'y1', source=source1, line_width=3, line_color='black', line_alpha=0.6, line_dash='dashed')
        #plot.xlabel("time (seconds)")
        #plot.ylabel("Gravitational Wave strain")
        plot

with col_anim:
	# ANIMATION
	with lock:

		fig,ax = plt.subplots(figsize=(4,4))
		ax.set_axis_off()

		fps = 30.
		length = 8.

		omega = 40./(m1 + m2)

		# create a Binary instance for the event
		binary = binary.Binary(
		    m1 = m1,
		    m2 = m2,
		    alpha = 50.,
		    beta = 20.,
		    gamma = 95.,
		    omega = omega,
		    frame_rate = fps
		    )

		# evolve the binary over one orbit
		n_frames = int(length*fps)

		binary.evolve(n_frames)

		# make BBH artist
		bbh = artists.BinaryBlackHole(
		    binary = binary,
		    ax = ax,
		    name='orbit',
		    BH_scale = 1./100
		)

		artist_dict = {}
		def init():
		    artist_dict.update(bbh.setup_artists())
		    #df = pd.DataFrame.from_dict(artist_dict)
		# configure plot axes, title
		    ax.set_xlim([-1,1])
		    ax.set_ylim([-1,1])
		    #if args.name is not None:
		    #    print('putting names on events')
		    #    ax.set_title(args.name)
		    return artist_dict

		def animate(i):
		    artist_dict.update(bbh.get_artists(i))
		    #df = pd.DataFrame.from_dict(artist_dict)
		    return artist_dict
		#print(init())                
		#bbh_animation = alt.Chart(df).mark_line().encode(
		#x=alt.X('1:T',axis=None),
		#y=alt.Y('0:Q',axis=None))

		#print(f'saving to {args.outfile}')
		outfile = f"temp/chirpgame_anim.gif"
		anim = animation.FuncAnimation(fig,animate,init_func=init,frames=n_frames)
		anim.save(outfile,fps=fps,writer='imagemagick')
		#anim.save(outfile,fps=fps)


		st.image(outfile)

f""" ##### Listen to the sound made by the Black Holes in the event {event["name"][0]} """
#""" ##### Original Event Sound """

event_url = event["infosheet"][0]


# This is based on https://www.gw-openscience.org/GW150914data/LOSC_Event_tutorial_GW150914.html#Frequency-shift-the-audio-files
# function that shifts frequency of a band-passed signal
def freqshift(data,fshift=100,sample_rate=4096):
    """Frequency shift the signal by constant
    """
    x = np.fft.fft(data)
    T = len(data)/float(sample_rate)
    df = 1.0/T
    nbins = int(fshift/df)
    # print T,df,nbins,x.real.shape
    #y = np.roll(x.real,nbins) + 1j*np.roll(x.imag,nbins)
    y = np.roll(x,nbins)
    y[0:nbins]=0.
    z = np.fft.ifft(y)
    return z

import scipy
def freq_mult_hilbert(x, freq_mult):
    z = scipy.signal.hilbert(x)
    z_mag = np.abs(z)
    z_arg = np.unwrap(np.angle(z))
    z_arg_new = z_arg * freq_mult
    z_new = z_mag * np.exp(1j * z_arg_new)
    x_new = -np.real(scipy.signal.hilbert(np.real(z_new)))
    return x_new
    #return np.real(z_new)

# Based on https://www.gw-openscience.org/GW150914data/LOSC_Event_tutorial_GW150914.html#Make-sound-files
# function to keep the data within integer limits, and write to wavfile:
def write_wavfile(filename,fs,data):
    d_norm = data/np.max(np.abs(data)) * 32767 * 0.9
    d_left = np.int16(d_norm.real)
    d_right = np.int16(d_norm.imag)
    wavfile.write(filename,int(fs), np.transpose(np.array([d_left, d_right])))


fshift = 200
fs = 4096*2

tdata = hp
#template_data = np.int16(tdata/max(abs(tdata)) * 327670)
W_audio = freqshift(tdata, fshift=fshift, sample_rate = fs)
#W_audio = template_data
write_wavfile("temp/chirp_event_audio.wav", fs, W_audio)
st.audio("temp/chirp_event_audio.wav")

#tdata = hp1
#template_data = np.int16(tdata/max(abs(tdata)) * 327670)
#W_audio = freqshift(tdata, fshift=fshift, sample_rate = fs)
#W_audio = template_data
#write_wavfile("temp/chirp_template_audio.wav",fs,W_audio)
#st.audio("temp/chirp_template_audio.wav")

f"""
You may find more information about the {event["name"][0]} event [here]({event_url}).
"""
#        """
###### Now, explore and find the black hole masses for other events in the list, or proceed to a short trivia on how the gravitational-wave chirp changes with the mass of black holes:
#  """        

#        question1 = st.radio("True or False: Increasing the mass of the black holes increases the amplitude of the waveform (i.e. makes the gravitational wave louder.", ('True', 'False'))

#        if question1 == 'True':
#            st.success("Correct Answer!")
#            """ For a given pair of binary black holes at the same distance away from us, the heavier pair will give out louder gravitational-waves. This is because heavier black holes radiate more gravitational-wave energy."""



