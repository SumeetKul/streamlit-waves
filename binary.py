import numpy as np

class Binary:
    
    def __init__(self,
        m1=10.,m2=10.,
        alpha=50.,beta=30.,gamma=0.,
        frame_rate = 30.,omega = 1.
    ):
        """
        A class for representing binaries.

        Parameters
        ----------
        m1,m2: floats
            masses of 1st and 2nd star, repsectively
        inclination: float
            inclination angle of binary wrt viewer
            in degrees, between [0,90] deg.
        azimuth: float
            azimuthal angle of viewer in coordinates
            of the binary, between [0,360] deg.
        phase: float
            phase of the binary, between [0,360] deg.
        frame_rate: float
            frames per second
        omega: float
            rotations per second
        """
        self.m1 = m1
        self.m2 = m2
        self.alpha = alpha
        self.beta = beta
        self.gamma = gamma
        self._omega = omega
        self.frame_rate = frame_rate
        self.precession='off'
        self._phase1 = self.gamma_rad
        self._D = np.identity(3)
        self._C = np.identity(3)
        self._B = np.identity(3)

        self._pos1_projected = []
        self._pos2_projected = []
        self._r = 1.
        

    @property
    def r(self):
        return self._r
    
    @property
    def omega(self):
        return self._omega

    @property
    def alpha_rad(self):
        return self.alpha*np.pi/180.

    @property
    def beta_rad(self):
        return self.beta*np.pi/180.

    @property
    def gamma_rad(self):
        return self.gamma*np.pi/180.

    @property
    def phase1(self):
        return self._phase1
    
    @phase1.setter
    def phase1(self,phase_rad):
        self._phase1 = phase_rad % 2*np.pi 
    
    @property
    def phase2(self):
        return self.phase1+np.pi
        
    def orbit(self):
        self._phase1 = self.phase1 + 2.*np.pi*self.omega/self.frame_rate

    @property
    def Dmatrix(self):
        self._D[0,0] = self._D[1,1] = np.cos(self.alpha_rad)
        self._D[1,0] = -np.sin(self.alpha_rad)
        self._D[0,1] = np.sin(self.alpha_rad)
        return self._D

    @property
    def Cmatrix(self):
        self._C[1,1] = self._C[2,2] = np.cos(self.beta_rad)
        self._C[2,1] = -np.sin(self.beta_rad)
        self._C[1,2] = np.sin(self.beta_rad)
        return self._C

    @property
    def Bmatrix(self):
        self._B[0,0] = self._B[1,1] = np.cos(self.gamma_rad)
        self._B[1,0] = -np.sin(self.gamma_rad)
        self._B[0,1] = np.sin(self.gamma_rad)
        return self._B
    
    @property
    def Amatrix(self):
       return np.matmul(np.matmul(self.Bmatrix,self.Cmatrix),self.Dmatrix)

    @property
    def pos1(self):
        """
        position of primary in XYZ coordinates of binary plane 
        """
        return (self.r*(self.m2/(self.m1+self.m2))
                * np.array([np.cos(self.phase1),np.sin(self.phase1),0])
        )

    @property
    def pos2(self):
        return (self.r*(self.m1/(self.m1+self.m2))
                * np.array([np.cos(self.phase2),np.sin(self.phase2),0])
        )
    
    def project(self):
        return np.matmul(self.Amatrix,self.pos1),np.matmul(self.Amatrix,self.pos2)

    def evolve(self,n_steps=1):
        for i in range(n_steps):
            self.orbit()
            pos1_proj,pos2_proj = self.project()
            self._pos1_projected.append(pos1_proj) 
            self._pos2_projected.append(pos2_proj)

    @property
    def pos1_projected(self):
        return np.array(self._pos1_projected)

    @property
    def pos2_projected(self):
        return np.array(self._pos2_projected) 

class InspiralingBinary(Binary):

    def __init__(self,
        m1=10.,m2=10.,
        alpha=50.,beta=30.,gamma=0.,
        frame_rate = 30.,omega0 = 1.
    ):

        super().__init__(
            m1,m2,
            alpha,beta,gamma,
            frame_rate,omega0
        )
        
        self.Mc = ((self.m1*self.m2)**(3./5))/((self.m1+self.m2)**(1./5))
        self.G = 4.3e-3 * 3.1e13  # km Msol^-1 (km/s)^2
        self.c = 3e5 # km/s

        self.tc = (((2.*omega0)**(-8./3))
                    * (5./((8.*np.pi)**(8./3)))
                    * (((self.c**3.)/(self.G*self.Mc))**(5./3))
        )
        print('tc',self.tc)        

        self.rmax = 2.*(self.G/(self.c**2))*(self.m1+self.m2)
        self.omegamax = np.sqrt(self.G*(self.m1+self.m2)/self.rmax**3)
        self.frame_rate = self.omegamax        
 
        self.t = [0.]
        pos1_proj,pos2_proj = self.project()
        self._pos1_projected = [pos1_proj]
        self._pos2_projected = [pos2_proj]         

    @property
    def nframes(self):
        return len(self.t)

    @property
    def omega(self):
        return (0.5)*((((8.*np.pi)**(8./3))/5.)
                        * (self.G*self.Mc/(self.c**3.))**(5./3)
                        * (self.tc - self.t[-1])
                  )**(-3./8)

    @property
    def r(self):
        return (self.G*(self.m1+self.m2)/(self.omega**2))**(1./3)

    def inspiral(self):
        while self.r > self.rmax:
            print('r,rmax:',self.r,self.rmax)
            self.t.append(self.t[-1]+(1./self.frame_rate))
            self.orbit()
            if isinstance(self.r,complex):
                print('r going complex, breaking out of loop')
                break
            pos1_proj,pos2_proj = self.project()
            self._pos1_projected.append(pos1_proj)
            self._pos2_projected.append(pos2_proj)     

