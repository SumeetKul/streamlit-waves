import streamlit as st
import numpy as np
from astropy.table import Table
import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection
from pycbc.waveform import get_td_waveform, get_fd_waveform
#from gwpy.timeseries import TimeSeries
import pandas as pd



st.text("hello world, again!")

"""
# Test page
"""

event_names = ["GW150914","GW151226","GW190521"]

mass1 = [30,15,300]
mass2 = [28,8,66]

dataframe = pd.DataFrame(np.array([event_names, mass1, mass2]).T, columns=('Event', 'Mass 1', 'Mass 2'))
#t = Table([event_names, mass1, mass2], names=('Event', 'Mass 1', 'Mass 2'))

st.table(dataframe)

if st.checkbox("Wave Tutorial"):

	"""
	
	
	### This is a wave
	
	$ W = A \sin (\omega t + \phi)$
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
	
	"""
	
	Here, 
	
	**A** is the wave amplitude, which determines the height of the peaks.
	
	
	**$\omega$** is the wave frequency, which determines how many cycles of the wave you see every second.
	
	**$\phi$** is the phase, which determines at what point the wave starts at time = 0, whether it is the crest, the trough, or somewhere in between!
	
	
	"""
	
	st.subheader("You can make your own wave!")
	
	
	A = st.slider('Amplitude', min_value=0, max_value=10)
	omega = st.slider('Frequency', min_value=1, max_value=5)
	phi = st.slider('Phase', min_value=0., max_value=np.pi)
	
	W = A * np.sin(omega*time + phi)
	
	fig = plt.figure(figsize=(10,6))
	
	plt.plot(time, W)
	plt.xlabel("time (seconds)")
	
	fig


chirp_option = st.sidebar.selectbox("Select Chirp tutorial", ["Chirp Demo", "Chirp Game"])

if chirp_option == "Chirp Demo":
	
	"""

	### This is a chirp
	"""
	
	m1 = 30
	m2 = 28
	
	"""
	Mass 1 = 30 $M_{\odot}$ \n
	Mass 2 = 28 $M_{\odot}$
	"""
	
	hp, hc = get_td_waveform(approximant="IMRPhenomD",
	         mass1=m1,
	         mass2=m2,
	         coa_phase=np.pi,
	         delta_t=1.0/2048,
	         f_lower=40.)
	
	h = np.sqrt(hp**2 + hc**2)
	
	n_samples = hp.shape[0]
	sample_rate = 2048
	
	seglen = n_samples/sample_rate
	
	time = np.linspace(-seglen, 0, n_samples)
	
	f = plt.figure(figsize=(12,4))
	plt.plot(time,hp)
	plt.xlabel("time (seconds)")
	plt.ylabel("Gravitational Wave strain")
	f
	#ts = TimeSeries.from_pycbc(hp)

if chirp_option == "Chirp Game":
	"""
	
	### You can make your own chirp!
	"""
	
	m1 = st.slider('Mass 1', min_value=20, max_value=50)
	m2 = st.slider('Mass 2', min_value=10, max_value=m1)
	
	hp, hc = get_td_waveform(approximant="IMRPhenomD",
	         mass1=m1,
	         mass2=m2,
	         coa_phase=np.pi,
	         delta_t=1.0/2048,
	         f_lower=20.)
	
	hp1, hc1 = get_td_waveform(approximant="IMRPhenomD",
	         mass1=30,
	         mass2=28,
	         coa_phase=np.pi,
	         delta_t=1.0/2048,
	         f_lower=20.)
	
	n_samples = hp.shape[0]
	sample_rate = 2048
	
	seglen = n_samples/sample_rate
	
	time = np.linspace(-seglen, 0, n_samples)
	
	ref_samples = hp1.shape[0]
	sample_rate = 2048
	
	seglen1 = ref_samples/sample_rate
	
	time1 = np.linspace(-seglen1, 0, ref_samples)
	
	hp_norm = hp / np.linalg.norm(hp)
	hp1_norm = hp1 / np.linalg.norm(hp1)
	#conv = np.convolve(hp, hp1)
	match = np.round(np.max(abs(np.correlate(hp_norm, hp1_norm))), 2)
	
	def result_statement(match):
	    if 0.0 < match <= 0.25:
	        rs = "Different chirps, try again!"
	    elif 0.25 < match <= 0.5:
	        rs = "Slight overlap, try again!"
	    elif 0.5 < match <= 0.75:
	        rs = "Getting closer... try again!"
	    elif 0.75 < match < 1.0:
	        rs = "Almost there... try again!"
	    elif match == 1.0:
	        rs = "Perfect!"
	    return rs
	        
	
	f = plt.figure(figsize=(12,4))
	plt.plot(time1,hp1)
	plt.plot(time, hp, c='black', linestyle="--", label=f"{result_statement(match)}")
	plt.xlabel("time (seconds)")
	plt.xlim(-2.0,0.0)
	plt.ylabel("Gravitational Wave strain")
	plt.legend(fontsize=24)
	f
	


