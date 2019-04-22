import sounddevice as sd
import numpy as np
# import soundfile as sf
import matplotlib.pyplot as pp
import math
import scipy.io.wavfile

def addnote(samplingrate,freq,resolution,alist):
    """
    im cool
    """
    noteduration = 1/samplingrate
    totalstuff = int(noteduration*resolution) 
    period = resolution/freq
    
    for dot in range(totalstuff):
        alist.append(np.int16(32767*math.cos(2*3.14/period*dot)))



filename = "actualsong.wav"
fs = 44100
frequency = 140
counter = 0
alist = []
c = []
addnote(1,261,44100,c)
# e = []
# addnote(311,2,e)
# g=[]
# addnote(392,2,g)
# lists_of_lists = [c,e,g]

# chord = [sum(x) for x in zip(*lists_of_lists)]

# for second in range(4*fs):
    # alist.append(0)
# for item in alist:
#square wave
    # if(counter==frequency):
    #     alist.append(0.99)
    #     counter = 0
    # else:
    #     alist.append(0)
    #     counter +=1


#sin wave
    # alist.append(math.cos(2*3.14/frequency*second))

#onephrase megalovanie
# addnote(147,0.25,alist)
# addnote(147,0.25,alist)
# addnote(294,0.25,alist)
# addnote(1,0.25,alist)
# addnote(220,0.75,alist)
# addnote(207,0.25,alist)
# addnote(1,0.25,alist)
# addnote(196,0.5,alist)
# addnote(174,0.5,alist)
# addnote(147,0.25,alist)
# addnote(174,0.25,alist)
# addnote(196,0.25,alist)
# #two
# addnote(130,0.25,alist)
# addnote(130,0.25,alist)
# addnote(294,0.25,alist)
# addnote(1,0.25,alist)
# addnote(220,0.75,alist)
# addnote(207,0.25,alist)
# addnote(1,0.25,alist)
# addnote(196,0.5,alist)
# addnote(174,0.5,alist)
# addnote(147,0.25,alist)
# addnote(174,0.25,alist)
# addnote(196,0.25,alist)
# #three
# addnote(123,0.25,alist)
# addnote(123,0.25,alist)
# addnote(294,0.25,alist)
# addnote(1,0.25,alist)
# addnote(220,0.75,alist)
# addnote(207,0.25,alist)
# addnote(1,0.25,alist)
# addnote(196,0.5,alist)
# addnote(174,0.5,alist)
# addnote(147,0.25,alist)
# addnote(174,0.25,alist)
# addnote(196,0.25,alist)
# #four
# addnote(116,0.25,alist)
# addnote(116,0.25,alist)
# addnote(294,0.25,alist)
# addnote(1,0.25,alist)
# addnote(220,0.75,alist)
# addnote(207,0.25,alist)
# addnote(1,0.25,alist)
# addnote(196,0.5,alist)
# addnote(174,0.5,alist)
# addnote(147,0.25,alist)
# addnote(174,0.25,alist)
# addnote(196,0.25,alist)
array = np.array(c)   

# data, fs = sf.read(array)
# print(data.shape)
scipy.io.wavfile.write('../final/test1.wav', 44100, array)

sd.play(array, fs,blocking =True)
pp.plot(array)
pp.show()


