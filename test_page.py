import streamlit as st
import numpy as np
from astropy.table import Table
import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection
from pycbc.waveform import get_td_waveform, get_fd_waveform
#from gwpy.timeseries import TimeSeries
import pandas as pd


# skyfield
from skyfield.data import hipparcos, mpc, stellarium
from skyfield.projections import build_stereographic_projection
from skyfield.api import load, wgs84, Star, load_constellation_names
from skyfield.positionlib import position_of_radec


#st.text("hello world, again!")

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
	


"""

### This is where LIGO is
"""
map_data = pd.DataFrame(
    np.array([[46.45527344020971, -119.40686250020742],[30.565511255619594, -90.76134906555212]]),
    columns=['lat', 'lon'])

st.map(map_data)


st.subheader("Take a closer look")

df = pd.DataFrame({
    'LIGO Hanford': [46.45527344020971, -119.40686250020742],
    'LIGO Livingston': [30.565511255619594, -90.76134906555212]
    })

option = st.selectbox(
    'Choose a LIGO site',
     df.keys())

map_data = pd.DataFrame(
    np.array([df[option]]),
    columns=['lat', 'lon'])

st.map(map_data, zoom=10)


st.subheader("Where was GW170817 in the sky?")

#### Needs Cache-ing

# The Hipparcos mission provides our star catalog.
@st.cache
def load_catalog():
    with load.open(hipparcos.URL) as f:
        stars = hipparcos.load_dataframe(f)
    return stars

stars = load_catalog()

# And the constellation outlines come from Stellarium.  We make a list
# of the stars at which each edge stars, and the star at which each edge
# ends.

url = ('https://raw.githubusercontent.com/Stellarium/stellarium/master'
       '/skycultures/western_SnT/constellationship.fab')

@st.cache
def load_constellations(url):
    with load.open(url) as f:
        constellations = stellarium.parse_constellations(f)
    return constellations

constellations = load_constellations(url)


edges = [edge for name, edges in constellations for edge in edges]
edges_star1 = [star1 for star1, star2 in edges]
edges_star2 = [star2 for star1, star2 in edges]


ra_hours = 13.09
dec_deg = -23.5


gw170817 = position_of_radec(ra_hours, dec_deg)

projection = build_stereographic_projection(gw170817)
field_of_view_degrees = 100.0
limiting_magnitude = 5.0

planet_file = 'de421.bsp'

#@st.cache
#def load_planets(filename):
#    planets = load(filename)
#    return planets

planets = load(planet_file)

earth = planets['earth']

ts = load.timescale()
t = ts.now()

star_positions = earth.at(t).observe(Star.from_dataframe(stars))
stars['x'], stars['y'] = projection(star_positions)


# Create a True/False mask marking the stars bright enough to be
# included in our plot.  And go ahead and compute how large their
# markers will be on the plot.

bright_stars = (stars.magnitude <= limiting_magnitude)
magnitude = stars['magnitude'][bright_stars]
marker_size = (0.5 + limiting_magnitude - magnitude) ** 2.0


# The constellation lines will each begin at the x,y of one star and end
# at the x,y of another.  We have to "rollaxis" the resulting coordinate
# array into the shape that matplotlib expects.

xy1 = stars[['x', 'y']].loc[edges_star1].values
xy2 = stars[['x', 'y']].loc[edges_star2].values
lines_xy = np.rollaxis(np.array([xy1, xy2]), 1)

const_name_conv = dict(load_constellation_names())
constellations_annotate = []
# Get constellation midpoints:
for i in range(len(constellations)):
    try:
        abbr = constellations[i][0]
        starlist = constellations[i][1]
        star1, star2 = starlist[int(len(starlist)/2)]
        xpos1, xpos2 = stars[['x', 'y']].loc[star1].values
        constellations_annotate.append([const_name_conv[abbr], (xpos1, xpos2)])
        #constellations_ann[const_name_conv[abbr]] = (xpos1, xpos2)
    except KeyError:
         pass


# Time to build the figure!
fig, ax = plt.subplots(figsize=[9, 9])
# Draw the constellation lines.
ax.add_collection(LineCollection(lines_xy, colors='#00f2'))
# constellation names.
for i in range(len(constellations_annotate)):
    ax.annotate(constellations_annotate[i][0], constellations_annotate[i][1], fontsize=8, alpha=0.5)
# Draw the stars.
ax.scatter(stars['x'][bright_stars], stars['y'][bright_stars],
           s=marker_size, color='k')

event_x, event_y = projection(gw170817)

ax.plot(event_x, event_y, '+', c='red', zorder=3)

angle = np.pi - field_of_view_degrees / 360.0 * np.pi
limit = np.sin(angle) / (1.0 - np.cos(angle))

ax.set_xlim(-limit, limit)
ax.set_ylim(-limit, limit)
ax.xaxis.set_visible(False)
ax.yaxis.set_visible(False)
ax.set_aspect(1.0)

fig
