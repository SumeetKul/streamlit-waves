import streamlit as st
import numpy as np
import streamlit_analytics
import altair as alt

#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%#
###################################### Page 1: Introduction to Oscillations and Waves ################################################################ 
#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%#


# GW150914 Hook:

"""
In September 2015, LIGO _observed_ two black holes spiraling into one another, and colliding to form one, larger black hole.

"""

#print(f'saving to {args.outfile}')
outfile = f"graphics/gw150914.gif"
st.image(outfile)


"""
But rather than directly observing this event, LIGO detected Gravitational Waves, ripples in the fabric of spacetime given out by the motion of these dense and massive black holes. This is what the two LIGO detectors, one in Livingston, Louisiana, and the other in Hanford, Washington recorded on September 14, 2015.
"""

st.image("graphics/GW150914.png")

"""
How does this signal translate into two black holes colliding? What makes a Gravitational _Wave_? To understand, let’s dive into the nature and properties of waves.

"""

