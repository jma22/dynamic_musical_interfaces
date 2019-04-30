import sounddevice as sd
import numpy as np
# import soundfile as sf
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
    
    for j in range(channelnum):
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
                    addnote(samplingrate,lastnote,resolution,musicdict[j],counter)
                    counter = 1
            else:
                addrest(samplingrate,resolution,musicdict[j])
                counter = 1
            lastnote = currentnote
        currentnote = noteDict[templist[-1]]
        lastnote = noteDict[templist[-2]]
        if currentnote!=0:
            addnote(samplingrate,currentnote,resolution,musicdict[j],counter)
        else:
            addrest(samplingrate,resolution,musicdict[j])
        
        
    


    #sum songs
    truemusic = []
    lengthsong = len(musicdict[0])
    
    for num in range(lengthsong):
        truemusic.append(0)
        for index in range(channelnum):
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
# # addnote(196,0.25,alist)
# 0:[2,2,2,2,2,2,2,2,2,2,2,2,2]

c = makeSong({0:[1,1,0,0,1,1,0,0],1:[5,5,5,5,5,5,5,5]},2)
array = np.array(c)   

# data, fs = sf.read(array)
# print(data.shape)
scipy.io.wavfile.write('../test1.wav', 44100, array)

sd.play(array, fs,blocking =True)
pp.plot(array)
pp.show()


