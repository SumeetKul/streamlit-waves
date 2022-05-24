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
import binary
import artists 
import wave
from scipy.io import wavfile
#import soundfile as sf

#from gwpy.timeseries import TimeSeries
import pandas as pd

def const_note(freq, l, amp=10000, rate=44100):
    t = np.linspace(0,l,l*rate)
    data = np.sin(2*np.pi*freq*t)*amp
    return t, data.astype('int16') # two byte integers

def var_note(freq, l, amp, rate=44100):
    t = np.linspace(0,l,l*rate)
    data = np.sin(2*np.pi*freq*t)*amp
    return t, data.astype('int16') # two byte integers



chirp_option = st.sidebar.selectbox("Select Option", ["Oscillations, Waves, and Chirps", "Chirp Game", "Detecting Gravitational Waves"])

#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%#
###################################### Page 1: Introduction to Oscillations and Waves ################################################################ 
#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%#

if chirp_option == "Oscillations, Waves, and Chirps":

# GW150914 Hook:

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


        The peaks and troughs represent the extreme points of whatever is oscillating: your hand, water in a pond, or a pendulum. 

        """
        time = np.arange(0,10, 0.01)

        A = 5
        f = 0.44
        omega = 2*np.pi*f
        phi = np.pi/2

        W = A * np.sin(omega*time + phi)

        fig = plt.figure(figsize=(10,6))

        plt.plot(time, W)
        plt.xlabel("time (seconds)")

        fig

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
        #srate = 32000
        #t_audio = np.linspace(0,4,4*srate)
        #f_audio = 440
        #W_audio = A*1000 * np.sin(2*np.pi*f_audio*t_audio + phi)

        """
        #### Sound #1
        """
        t, W_audio = const_note(440, 4)
        wavfile.write("const_waves_audio.wav",44100,W_audio)
        st.audio("const_waves_audio.wav")


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

        source = ColumnDataSource(data=dict(x=time, y=W))


        # Set up plot
        plot = figure(height=600, width=1000, title="Make your own wave",
              tools="crosshair,pan,reset,save,wheel_zoom",
              x_range=[0, 10], y_range=[-12, 12])

        plot.line('x', 'y', source=source, line_color='orange', line_width=3, line_alpha=0.6)

        plot
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

# Real-life waves: varying frequencies and amplitudes:

        """
        Waves are thus all around us - they make up the sound of music, and the cacophony of noise. But they do not typically look like the perfect, sinusoidal oscillations shown in the graphs above. 

        Think of an ambulance siren. Its loudness varies, as does its frequency or pitch. 

        """

        st.audio("temp/ambulance-siren.mp3")

        """
        The waveform of a siren looks like this. Can you see the variation in frequency and amplitude here?
        """

        t = np.arange(4096)/1024
        A_siren = np.sin(2*np.pi*0.5*t)
        f_siren = np.sin(2*np.pi*0.7*t)

        w_siren = A_siren*np.sin(2*np.pi*f_siren*t)

        source = ColumnDataSource(data=dict(x=t, y=w_siren))

        # Set up plot
        plot = figure(height=600, width=1000, title="Ambulance Siren",
              tools="crosshair,pan,reset,save,wheel_zoom",
              x_range=[0, 4], y_range=[-2, 2])

        plot.line('x', 'y', source=source, line_width=3, line_color='crimson', line_alpha=0.6)

        plot

        """
        What happens when you have a constant frequency but varying amplitude?
        """

        t = np.arange(0,10,0.01)
        A_amp = 2 + np.sin(2*np.pi*0.5*t)
        f_amp = 5

        w_amp = A_amp*np.sin(2*np.pi*f_amp*t)

        source = ColumnDataSource(data=dict(x=t, y=w_amp))

        # Set up plot
        plot = figure(height=600, width=1000, title="Varying Amplitude",
              tools="crosshair,pan,reset,save,wheel_zoom",
              x_range=[0, 8], y_range=[-4, 4])

        plot.line('x', 'y', source=source, line_color='green', line_width=3, line_alpha=0.6)

        plot

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

        source = ColumnDataSource(data=dict(x=t, y=w_red))

        # Set up plot
        plot = figure(height=600, width=1000, title="Redshift",
        tools="crosshair,pan,reset,save,wheel_zoom",
        x_range=[0, 10], y_range=[-4, 4])

        plot.line('x', 'y', line_color='red', source=source, line_width=3, line_alpha=0.6)

        plot

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

        source = ColumnDataSource(data=dict(x=t, y=w_blue))

        # Set up plot
        plot = figure(height=600, width=1000, title="Blueshift",
        tools="crosshair,pan,reset,save,wheel_zoom",
        x_range=[0, 10], y_range=[-4, 4])

        plot.line('x', 'y', line_color='blue', source=source, line_width=3, line_alpha=0.6)

        plot

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


        Now that we have seen waves that change in amplitude alone or frequency alone, let us see an example where _both_ these quantities **increase** with time:
        """

        t = np.arange(0,10,0.01)
        A_chirp = np.power(1.3, t)
        f_chirp = np.exp(t/12)

        w_chirp = A_chirp*np.sin(2*np.pi*f_chirp*t)

        source = ColumnDataSource(data=dict(x=t, y=w_chirp))

        # Set up plot
        plot = figure(height=600, width=1000, title="Chirp",
        tools="crosshair,pan,reset,save,wheel_zoom",
        x_range=[0, 10], y_range=[-20, 20])

        plot.line('x', 'y', line_color='black', source=source, line_width=3, line_alpha=0.6)

        plot

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

        st.image("cbc.png")

        """
        As the two black holes are revolving around each other, their motion radiates gravitational waves. This causes them to lost energy through these waves, pulling them closer towards each other. 

        As the separation between the black holes decreases, the conservation of angular momentum implies that they start revolving faster! Think of a ballet dancer spinning faster as she pulls in her arms and legs close together.

        The faster motion of black holes as they come together increases the _frequency_ of their emitted gravitational waves, since the black holes complete more and more orbits around each other in a given amount of time. 

        At the same time, the _amplitude_ of the emitted gravitational wave also increases, since the spacetime around them gets more and more curved as they are drawn together.


        """

        st.image("bbh.gif")

        """

        Each pair of black holes, called a **Binary Black Hole (BBH)** system, thus leaves a characteristic imprint of gravitational waveforms as they spiral in and collide into one.
        """


#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%#
################################################# Part 2: Chirp Game #######################################################################################
#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%#

if chirp_option == "Chirp Game":
        """
        ### You can make your own chirp!
        """


        m1 = st.slider("Mass 1", min_value=20, max_value=50)
        m2 = st.slider('Mass 2', min_value=10, max_value=40)

        hp1, hc1 = get_td_waveform(approximant="IMRPhenomD",
                 mass1=m1,
                 mass2=m2,
                 coa_phase=np.pi,
                 delta_t=1.0/2048,
                 f_lower=15.)

        hp, hc = get_td_waveform(approximant="IMRPhenomD",
                 mass1=30,
                 mass2=28,
                 coa_phase=np.pi,
                 delta_t=1.0/2048,
                 f_lower=15.)

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
        conv = np.convolve(hp, hp1)
        match = np.round(np.max(abs(np.correlate(hp_norm, hp1_norm))), 2)
         
        def result_statement(match):
            if 0.0 < match <= 0.25:
                rs = "Different chirps, try again!"
                rc = "red"
            elif 0.25 < match <= 0.5:
                rs = "Slight overlap, try again!"
                rc = "red"
            elif 0.5 < match <= 0.75:
                rs = "Getting closer... try again!"
                rc = "orange"
            elif 0.75 < match < 1.0:
                rs = "Almost there... try again!"
                rc = "orange"
            elif match == 1.0:
                st.balloons()
                #st.success("Match found!")
                rs = "Perfect!"
                rc = "green"
            return rs, rc
                
        source = ColumnDataSource(data=dict(x=time, y=hp))
        source1 = ColumnDataSource(data=dict(x1=time1, y1=hp1))

        col_anim, col_plot = st.columns([1,3])
        with col_plot:
                # Set up plot
                plot = figure(height=300, width=800, title="GW match chirp",
                      tools="crosshair,pan,reset,save,wheel_zoom", x_range=[-4, 0])

                plot.title.text = result_statement(match)[0]
                plot.title.align = "center"
                plot.title.text_color =  result_statement(match)[1]
                plot.title.text_font_size = "25px"


                plot.line('x', 'y', source=source, line_width=3, line_alpha=0.9)
                plot.line('x1', 'y1', source=source1, line_width=3, line_color='black', line_alpha=0.6, line_dash='dashed')
                #plot.xlabel("time (seconds)")
                #plot.ylabel("Gravitational Wave strength")
                plot

        with col_anim:
                # ANIMATION        
                fig,ax = plt.subplots(figsize=(3,3))
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
                # configure plot axes, title
                    ax.set_xlim([-1,1])
                    ax.set_ylim([-1,1])
                    #if args.name is not None:
                    #    print('putting names on events')
                    #    ax.set_title(args.name)
                    return artist_dict

                def animate(i):
                    artist_dict.update(bbh.get_artists(i))
                    return artist_dict

                #print(f'saving to {args.outfile}')
                outfile = f"temp/bbh.gif"
                anim = animation.FuncAnimation(fig,animate,init_func=init,frames=n_frames)
                anim.save(outfile,fps=fps,writer='imagemagick')
                #anim.save(outfile,fps=fps)
                st.image(outfile)

        #plot

        #user_input_m1 = st.text_input("Mass 1")
        #user_input_m2 = st.text_input("Mass 2")

        #if user_input_m1 == 30 and user_input_m2 == 28:
        #    """ *Congratulations!!* you have entered the correct masses for the Black Holes in the GW150914 event."""
        #else:
        #    print("""Incorrect Black Hole masses for the GW150914 event. Please try again!""")

        """ #### Finally, you can compare the sound made by the Black Holes in the first event, GW150914, with the sound made by the Black Holes you selected: """
        """ ##### Original Event Sound """


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

        """ ##### Your Chirp Sound """
        tdata = hp1
        #template_data = np.int16(tdata/max(abs(tdata)) * 327670)
        W_audio = freqshift(tdata, fshift=fshift, sample_rate = fs)
        #W_audio = template_data
        write_wavfile("temp/chirp_template_audio.wav",fs,W_audio)
        st.audio("temp/chirp_template_audio.wav")


#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%#
################################################ Part 3: Detecting Gravitational Waves #######################################################################
#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%#

if chirp_option == "Detecting Gravitational Waves":

        """ 
        Remember the exercise in **Oscillations, Waves, and Chirps** where you changed different parameters in a wave to see its effect on the waveform and its sound? What was the parameter that caused no change in the sound?


        Yes, it was the _phase_ of the wave. The value that is determined by the starting point of the wave's creation, whether it was at a peak, a valley, or somewhere in between.       

        But do not discount the phase as a boring, irrelevant parameter just yet!

        While the gravitational wave amplitude and frequency tell us about the black holes that caused it, phase plays an important role in the actual detection of gravitational waves!

        To understand why, let's dig into how LIGO works.

        LIGO is the Laser _Interferometer_ Gravitational-wave Observatory. It is an _Interferometer_, which studies the interference between two laser beams that are shot along the two 4-km long arms of the L-shaped detector.


        <more to add...>        
        """
        st.image("temp/ligo.gif")

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
        source = ColumnDataSource(data=dict(x=time, y=W1))


        # Set up plot
        plot1 = figure(height=200, width=800, title="Fixed Phase Wave; Phase = 0",
              tools="crosshair,pan,reset,save,wheel_zoom",
              x_range=[0, 4], y_range=[-20, 20])

        plot1.line('x', 'y', source=source, line_color='yellow', line_width=3, line_alpha=0.6)

        
        plot1

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
            ax.plot(theta0, r0, linewidth=4, color="yellow")
            ax.set_rmax(1)
            ax.set_rticks([])  # Less radial ticks
            #ax.set_rlabel_position(-22.5)  # Move radial labels away from plotted line
            ax.grid(True)

            ax.set_title("Phase", va='bottom', fontsize=20)
            plt.tight_layout()
            fig

        W2 = A * np.sin(omega*time + phi2)
        W2_audio = A * np.sin(omega_audio*t + phi2)

        source = ColumnDataSource(data=dict(x=time, y=W2))


        # Set up plot
        plot2 = figure(height=200, width=800, title="Variable Phase Wave",
              tools="crosshair,pan,reset,save,wheel_zoom",
              x_range=[0, 4], y_range=[-20, 20])

        plot2.line('x', 'y', source=source, line_color='blue', line_width=3, line_alpha=0.6)

        plot2


# Phase difference plot:
        W3 = W1 + W2
      
        source = ColumnDataSource(data=dict(x=time, y=W3))


        # Set up plot
        plot3 = figure(height=200, width=800, title="Resultant Wave after Interference",
              tools="crosshair,pan,reset,save,wheel_zoom",
              x_range=[0, 4], y_range=[-20, 20])
        #plot3.xaxis.ticker = [0, np.pi, 2*np.pi]
        #plot3.xaxis.major_label_overrides = {1: '0', 2: 'pi', 3: '2pi'}

        plot3.line('x', 'y', source=source, line_color='green', line_width=3, line_alpha=0.6)

        plot3

        # t = np.linspace(0,l,l*rate)
        # data = np.sin(2*np.pi*freq*t)*amp
        W3_audio = (W1_audio + W2_audio) * 10000
        W3_audio = W3_audio.astype('int16')
#        t, W_audio = const_note(freq*100, 4, amp = W3)
        wavfile.write("temp/phase_audio.wav",44100,W3_audio)
        st.audio("temp/phase_audio.wav")

 
