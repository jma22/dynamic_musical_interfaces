import requests
import scipy.io.wavfile
import numpy as np
# import soundfile as sf
import math


def addnote(samplingrate,freq,resolution,alist):
    """
    jeremy is retarded
    """
    noteduration = 1/samplingrate
    totalstuff = int(noteduration*resolution)
    period = resolution/freq

    for dot in range(totalstuff):
        alist.append(math.cos(2*3.14/period*dot))

def addrest(samplingrate,resolution,alist):
    """
    im cool
    """
    noteduration = 1/samplingrate
    totalstuff = int(noteduration*resolution)

    for dot in range(totalstuff):
        alist.append(0)



# filename = "actualsong.wav"
# fs = 5000
# frequency = 140
# counter = 0
# alist = []
# c = []
# addnote(261,2,c)




# sd.play(array, fs,blocking =True)
# pp.plot(array)
# pp.show()

def request_handler(request):
    resolution = 44100
    samplingrate = 8 #Hz
    #add timing to db
    # method': 'GET', 'args': ['foo', 'bar'], 'values': {'recording':'true'}}
    if request['form']['recording'] =='true':
        #start recording by saving timestamp/resetting databse idk alex
        return request['form']['recording']
    elif request['form']['recording'] =='false':
        #stop recording by doing whatever @alex
        alist = []
        addnote(samplingrate,freq,resolution,alist)
        addrest(samplingrate,resolution,alist)


        array = np.array(alist)
        scipy.io.wavfile.write('__home__/testfinal/music/test.wav', resolution, array)  #make unique string plz
        return request['form']['recording']
