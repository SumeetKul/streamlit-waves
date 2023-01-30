# streamlit-waves

A python and streamlit-based learning tool to use gravitational wave research to teach concepts in oscillations and waves in middle- and high-school physics classrooms. You may access it at this [link](https://sumeetkul-streamlit-waves-gravitational-waves-demo-kxxtwz.streamlitapp.com/).

Here is an outline of this project presented at the 4th International Astronomical Union (IAU)-Shaw workshop on 'Astronomy for Education', held in November 2022: [Youtube link](https://www.youtube.com/watch?v=j7WcEimtJtI&list=PLeQtlKnFCOppopOt_SMXh_IFFsMOLQu5_&index=59)


## Bringing Gravitational Waves into the classroom using Streamlit

The LIGO Science Education Center (SEC) in Livingston, Louisiana, USA was established to increase science engagement and provide access to quality physics  education at one of the two Laser Interferometer Gravitational-wave Observatory (LIGO) sites in the country. Through on-site school field trips and detector tours, the focus of LIGO SEC has always been to connect the fundamental physics involved in the detection of gravitational waves to the concepts being taught in schools. A lot of this involves hands-on demonstrations that build upon certain instrumental challenges encountered by LIGO. For instance, the mirrors used inside the interferometer are controlled using electrostatic actuators - this is not too different from how the build up of static charge enables us to displace light objects. Another example involves using pressure and vacuum demos, given that the 4-km long LIGO arms contain one of the largest vacuums in the whole world, to avoid scattering of the laser light that they carry. 

With the onset of the COVID-19 pandemic, SEC field trips had to be conducted virtually. This change was accompanied by a creative redesign of the hands-on activities using materials that could be shipped or easily procured at home. At the same time, the value of developing web-based lessons was evident. However, the challenges of developing in-house web applications are many: how to transfer software to the students? How to make sure it is compatible with a wide array of computers and operating systems? How to strike a balance between creating a well-developed lesson plan and writing the actual code?

I spent the Spring semester of 2022 at LIGO Livingston SEC as an outreach fellow. I was well-versed in the Python programming language for my research, and I soon encountered Streamlit, an open-source framework for easy web-deployment of python code. Streamlit had been used previously within the LIGO education and public outreach (EPO) group to create a webpage [1] where users could easily visualize public data displaying the Gravitational-wave events detected by LIGO-Virgo so far. 

With the goal of using the fundamentals of gravitational waves to teach high-school physics concepts of oscillations and waves, I experimented with the streamlit interface and found it to be very easy to work with. I wanted to explain how a gravitational waveform recorded by our detectors is linked with the picture of two black holes spiraling into one another and colliding. The way these black holes move leads to interesting dynamics seen as changes in the frequency and amplitude of waves, which in turn can be used to teach these concepts. Streamlit enables making interactive plots where wave parameters can be modified by the user, and can even be played out as sound. At the end of the lesson, having learned different features of a gravitational wave, students can “make their own gravitational wave” by selecting masses of black holes. There is even a game at the end where students try to figure out which two black holes emit a particular waveform corresponding to one of the actual events detected by LIGO-VIrgo.

Our new app [2] is cloud-based and hosted on the streamlit server, which makes it possible for anyone to access it. There is no setup time and requirement involved for teachers. The lessons themselves can be either self-guided or conducted in classroom groups. 

All in all, streamlit makes it possible for creating a free, easy to deploy, interactive online classroom lesson to teach the simple physics of oscillations and waves by connecting it to the frontiers of gravitational wave research.


References: 
[1] Jonah Kanner (2020). Gravitational-wave apps help students learn about black holes: [Streamlit blog](https://blog.streamlit.io/gravitational-wave-apps-help-students-learn-about-black-holes/)
[2] [Link to streamlit app](https://sumeetkul-streamlit-waves-gravitational-waves-demo-kxxtwz.streamlitapp.com/)
