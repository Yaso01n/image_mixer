import cv2
import numpy as np
from Functions import*


class Imagefourier:
    def __init__(self, image,mag_x,phase_x,y):
        self.image=cv2.imread(image,0)
        self.image=cv2.resize(self.image,(400,400))
        self.fftofimage=np.fft.fftshift(np.fft.fft2(self.image))
        self.magnitude=np.sqrt(np.real(self.fftofimage) ** 2 + np.imag(self.fftofimage) ** 2)
        self.magnitude_spectrum = 20*np.log(np.abs(self.fftofimage))
        self.phase=np.arctan2(np.imag(self.fftofimage), np.real(self.fftofimage))
        self.phase_spectrum = np.angle(self.fftofimage)
        self.mag_x=mag_x
        self.phase_x=phase_x
        self.mag_y=self.phase_y=y

class Processing(Imagefourier):

    def __init__(self,image,mag_x=0,phase_x=0,y=0):
        Imagefourier.__init__(self,image,mag_x,phase_x,y)
      
    def combine(self, magnitude, phase):
        self.outputcombine = np.multiply(magnitude, np.exp(1j *phase))
        self.img_output = np.real(np.fft.ifft2(self.outputcombine))
    
    def mask(self,x,y,width,height,inv,option_y,option_x,option):
        y_indx1= (y-option_y)
        y_indx2= (y+height-option_y)
        x_indx1= (x-option_x)
        x_indx2= (x+width-option_x)
        masked_option= option.copy()
        if inv==0:
            masked_option[int(y_indx1):int(y_indx2),int(x_indx1):int(x_indx2)]=option[int(y_indx1):int(y_indx2),int(x_indx1):int(x_indx2)]
        else:
            masked_option[0:int(y_indx1),0:-1]=1
            masked_option[int(y_indx2):-1,0:-1]=1
            masked_option[int(y_indx1):int(y_indx2),0:int(x_indx1)]=1
            masked_option[int(y_indx1):int(y_indx2),int(x_indx2):-1]=1
        return masked_option
  
    def index(self,image2,x,y,width,height,option_y,option_x,option_y1,option_x1,option,option1,inv,uniform_option):
        array=np.array([])
        if ( all( option_x+300>m> option_x for m in (x,x+width)) and all( option_y+300>m > option_y for m in (y,y+height))):
            array=self.mask(x,y,width,height,inv,option_y,option_x,option)
            
        elif ( all(option_x1+300>m >option_x1 for m in (x,x+width)) and all(option_y1+300>m >option_y1 for m in (y,y+height))):
            array=image2.mask(x,y,width,height,inv,option_y1,option_x1,option1)
        else:
            array=uniform_option

        return array

    def reconstruct(self,image2,x,y,width,height,x2,y2,width2,height2,inv):

        uniform_mag=np.ones(len(self.magnitude))
        uniform_phase=1j *np.ones(len(self.phase))
        
        new_mag=self.index(image2,x,y,width,height,self.mag_y,self.mag_x,image2.mag_y,image2.mag_x,self.magnitude,image2.magnitude,inv,uniform_mag)
        new_phase=self.index(image2,x2,y2,width2,height2,self.phase_y,self.phase_x,image2.phase_y,image2.phase_x,self.phase,image2.phase,inv,uniform_phase)

        if (len(new_mag)!=0 and len(new_phase)!=0):
            self.combine(new_mag,new_phase)
            