import sounddevice as sd
import numpy as np
import soundfile as sf
import matplotlib.pyplot as pp
import math
import scipy.io.wavfile



def addrest(samplingrate,resolution,alist):
    """
    adds a rest to the wave file
    """
    noteduration = 1/samplingrate
    totalstuff = int(noteduration*resolution)

    for dot in range(totalstuff):
        alist.append(0)


def addnote(samplingrate,freq,resolution,alist,duration):
    """
    input: samplingrate, freqtuple, resolution, alist, duration in sampling rates
    output: adds a note,
    """
    noteduration = 1/samplingrate
    totalstuff = int(noteduration*resolution)
    dot = 0
    period = resolution/freq
    for dot in range(totalstuff*duration):
        alist.append(math.sin(2*3.14/period*dot))



    # if freq[1] ==0:
    #     period1 = resolution/freq[0]
    #     for dot in range(totalstuff*duration):
    #         alist.append(math.cos(2*3.14/period1*dot))
    # elif freq[2] ==0:
    #     period1 = resolution/freq[0]
    #     period2 = resolution/freq[1]
    #     for dot in range(totalstuff*duration):
    #         alist.append(math.cos(2*3.14/period1*dot)+(math.cos(2*3.14/period2*dot)))
    # else:
    #     period1 = resolution/freq[0]
    #     period2 = resolution/freq[1]
    #     period3 = resolution/freq[2]
    #     for dot in range(totalstuff*duration):
    #         alist.append((math.cos(2*3.14/period1*dot))+(math.cos(2*3.14/period2*dot))+(math.cos(2*3.14/period3*dot)))

def makeSong(songDict,channelnum):
    noteDict = {0:0,1:261,2:294,3:330,4:349,5:392,6:440,7:494,8:523}
    samplingrate = 8
    resolution = 44100
    musicdict = {}
    #init empty dict

    for j in songDict.keys():
        musicdict[j] = []
        templist = songDict[j]
        print(templist)
        counter = 1
        lastnote = templist[0]
        for note in templist:
            currentnote = noteDict[note]
            if lastnote != 0:
                if lastnote == currentnote:
                    counter+=1
                else:
                    addnote_oboe(samplingrate,lastnote,resolution,musicdict[j],counter)
                    counter = 1
            else:
                addrest(samplingrate,resolution,musicdict[j])
                counter = 1
            lastnote = currentnote
        currentnote = noteDict[templist[-1]]
        lastnote = noteDict[templist[-2]]
        if currentnote!=0:
            addnote_oboe(samplingrate,currentnote,resolution,musicdict[j],counter)
        else:
            addrest(samplingrate,resolution,musicdict[j])
    #sum songs
    truemusic = []
    lengthsong = len(musicdict[list(songDict.keys())[0]])

    for num in range(lengthsong):
        truemusic.append(0)
        for index in songDict.keys():
            truemusic[num]+= musicdict[index][num]/channelnum

    print(lengthsong)
    print(len(truemusic))
    return truemusic








filename = "actualsong.wav"
fs = 44100
frequency = 140



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



import matplotlib.pyplot as plt
import numpy as np
from numpy.fft import fft, fftfreq, ifft


testnote = []
addnote(8,440,44100,testnote,8)
testlen = np.linspace(0,1,len(testnote))

def addnote_oboe(samplingrate,freq,resolution,alist,duration):
    """
    input: samplingrate, freqtuple, resolution, alist, duration in sampling rates
    output: adds a note,
    """
    testfft_vals = []
    noteduration = 1/samplingrate
    totalstuff = int(noteduration*resolution)*duration
    freqscale = noteduration*duration

    print(duration)
    #init fft
    for i in range(totalstuff):
        testfft_vals.append(0)
    #put the goodstuff
    print(totalstuff)
    print(int(freq*freqscale))
    testfft_vals[int(freq*freqscale)]=totalstuff
    testfft_vals[int(freq*freqscale)*2]=totalstuff*9/10
    testfft_vals[int(freq*freqscale)*3]=totalstuff*22/10
    testfft_vals[int(freq*freqscale)*4]=totalstuff*2/10
    testfft_vals[int(freq*freqscale)*5]=totalstuff*22/100
    testfft_vals[int(freq*freqscale)*6]=totalstuff*23/100
    testifft_vals = ifft(testfft_vals)
    alist.extend(list(testifft_vals.real[0:totalstuff]))
    
# n = 1000

# T = 100

# omg = 2*np.pi/T

# x = np.linspace(0,T,n)

# y1 = np.cos(1.0*omg*x)
# y2 = np.cos(100.0*omg*x)
# y3 = np.sin(20.0*omg*x)

# y=y2
# freqs = fftfreq(n)

# mask = freqs > 0

# fft_vals = fft(y) 

# ifft_vals = ifft(fft_vals)

# print(ifft_vals)

# fft_theo = 2*np.abs(fft_vals/n)


# testnotefreqs = fftfreq(len(testnote))
# mask = testnotefreqs > 0
# testnotefftvals = fft(testnote)
# testnotefft_theo = 2*np.abs(testnotefftvals/len(testnote))
# testfft_vals = []
# # testnoteifftvals = ifft(testnotefftvals)
# for i in range(88200):
#     testfft_vals.append(0)

# # #violin
# testfft_vals[880]=44100
# testfft_vals[880*2]=44100/4
# testfft_vals[880*3]=44100/8
# testfft_vals[880*4]=44100*3/16
# testfft_vals[880*5]=44100/2
# testfft_vals[440*6]=44100/4
# testfft_vals[440*7]=44100*11/16
# testfft_vals[440*8]=44100/2
# testfft_vals[440*9]=44100*3/16
#piano
# testfft_vals[220]=44100*16/100
# testfft_vals[330]=44100*8/100
# testfft_vals[440]=44100
# testfft_vals[440*2]=44100*1/10
# testfft_vals[440*3]=44100*36/100
# testfft_vals[440*4]=44100*7/100
# testfft_vals[440*5]=44100*6/100
# testfft_vals[440*6]=44100*5/100
# testfft_vals[440*2-1]=44100*7/10/4
# testfft_vals[440*3-1]=44100*15/100/4
# testfft_vals[440*4-1]=44100*2/100/4
# testfft_vals[440*5-1]=44100*4/100/4

# #oboe
# testfft_vals[220]=44100
# testfft_vals[220*2]=44100*9/10
# testfft_vals[220*3]=44100*22/10
# testfft_vals[220*4]=44100*2/10
# testfft_vals[220*5]=44100*22/100
# testfft_vals[220*6]=44100*23/100


# testifft_vals = ifft(testfft_vals)
# lasti=0
# j = 0
# positivevals = testnotefft_theo[mask]
# for i in positivevals:
#     if lasti < i:
#         print(i)
#         print(j)
#     lasti = i
#     j+=1

# print(len(testnoteifftvals))

# plt.figure(1)
# plt.title('original signal')
# plt.plot(testnotefreqs[mask],testnotefft_theo[mask],color = 'xkcd:salmon')

# plt.figure(2)
# plt.plot(testlen,testnoteifftvals, label = "raw")
# plt.title("raw fft")
# plt.plot(freqs[mask],fft_theo[mask], label ="true")
# plt.title("true fft")

# plt.show()



c = makeSong({'lmao':[2,2,0,0,2,2,0,0]},1)
array = np.array(c, dtype=np.float32)
# print(c)

# data, fs = sf.read(array)
# print(np.mean(array))
# print(array.dtype)
# scipy.io.wavfile.write('./test3.wav', 44100, array)

sd.play(array, 44100,blocking =True)

plt.plot(c)
plt.show()
