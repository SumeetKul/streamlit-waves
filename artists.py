import numpy as np
import binary
from matplotlib import pyplot as plt
from matplotlib.patches import Ellipse,Circle

class BinaryBlackHole:

    """
    A class to define the matplotlib artists
    for a binary black hole.
    """

    def __init__(self,
        binary,
        ax,
        name,
        BH_scale = 1,
    ):
        """
        Parameters
        ----------
        binary: Binary
            An evolved Binary object
        ax: axis object
            The matplotlib axis to plot the artists on
        name: str
            unique name of the binary for identification
        BH_scale: float
            scale of BH on image WRT BH mass in solar masses

        Returns
        -------
        None
        """
        self.binary = binary
        self.ax = ax
        self.name = name
        self.BH_scale = BH_scale
        self.edgecolor='white',
        self.facecolor='black',
        self.artists = {}

    def setup_artists(self):
        z1,x1,y1 = self.binary.pos1_projected[0,:]
        z2,x2,y2 = self.binary.pos2_projected[0,:]
        self.artists['{}_m1'.format(self.name)] = self.ax.add_artist(
            Circle((x1,y1), radius=self.BH_scale*self.binary.m1,
                edgecolor='white',
                facecolor='black'
            )
        )
        self.artists['{}_m2'.format(self.name)] = self.ax.add_artist(
            Circle((x2,y2), radius=self.BH_scale*self.binary.m2,
                edgecolor='white',
                facecolor='black'
            )
        )
        # make sure star that is closer is shown on top of the other
        if z1 > z2:
            zorder_1, zorder_2 = 2, 1
        else:
            zorder_1, zorder_2 = 1, 2
        self.artists['{}_m1'.format(self.name)].set_zorder(zorder_1)
        self.artists['{}_m2'.format(self.name)].set_zorder(zorder_2)

        return self.artists

    def get_artists(self,i):
        z1,x1,y1 = self.binary.pos1_projected[i,:]
        z2,x2,y2 = self.binary.pos2_projected[i,:]
        self.artists['{}_m1'.format(self.name)].set_center((x1,y1))
        self.artists['{}_m2'.format(self.name)].set_center((x2,y2)) 

        # make sure star that is closer is shown on top of the other
        if z1 > z2:
            zorder_1, zorder_2 = 2, 1
        else:
            zorder_1, zorder_2 = 1, 2
        self.artists['{}_m1'.format(self.name)].set_zorder(zorder_1)
        self.artists['{}_m2'.format(self.name)].set_zorder(zorder_2)

        return self.artists

class BlackHoleRingdown:
    def __init__(self,
        M,
        amplitude0,
        omega,
        tau,
        ax,
        name,
        BH_scale = 1
    ):
        self.M = M
        self.tau = tau
        self._amplitude0 = amplitude0
        self.omega = omega
        self.ax = ax
        self.name = name
        self.artists = {}
        self.BH_scale = BH_scale

    def amplitude(self,i):
        return self._amplitude0 * np.exp(-i/self.tau) * np.cos(2.*2.*np.pi*i/self.tau)

    def get_height_width(self,i):
        return 1 + self.amplitude(i), 1 - self.amplitude(i) 

    def setup_artists(self):
        height,width = self.get_height_width(0)
        self.artists['{}_ringdown'.format(self.name)] = self.ax.add_artist(
            Ellipse((0,0),
                self.BH_scale*self.M*height,self.BH_scale*self.M*width,
                edgecolor='white',facecolor='black'
            )
        )
        return self.artists

    def get_artists(self,i):
        height,width = self.get_height_width(i)
        self.artists['{}_ringdown'.format(self.name)].height = self.BH_scale*self.M*height
        self.artists['{}_ringdown'.format(self.name)].width = self.BH_scale*self.M*width
        return self.artists       
         
