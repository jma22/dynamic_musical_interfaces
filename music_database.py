import sqlite3
import time
import string
# from recording import *
import scipy.io.wavfile
import numpy as np
import math
import soundfile as sf
import os


soundcloud = '__HOME__/dynamic_musical_interfaces/soundcloud.db'  #database

"""
database entry will contain timing, instrument name, string
containing numbers for each note value. Assuming a sampling
rate of 8 hz?

post request form: instrument=?&notes=?
"""


def addrest(samplingrate,resolution,alist):
    """
    adds a rest to the wave file
    """
    noteduration = 1/samplingrate
    totalstuff = int(noteduration*resolution)

    for dot in range(totalstuff):
        alist.append(0)

def addnote_theremin(samplingrate,freq,resolution,alist,duration):
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
    testfft_vals[int(freq*freqscale)]=totalstuff
    testfft_vals[int(freq*freqscale)*2]=totalstuff*9/10
    testfft_vals[int(freq*freqscale)*3]=totalstuff*22/10
    testfft_vals[int(freq*freqscale)*4]=totalstuff*2/10
    testfft_vals[int(freq*freqscale)*5]=totalstuff*22/100
    testfft_vals[int(freq*freqscale)*6]=totalstuff*23/100
    testifft_vals = ifft(testfft_vals)
    alist.extend(list(testifft_vals.real[0:totalstuff]))

def addnote_piano(samplingrate,freq,resolution,alist,duration):
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
    testfft_vals[int(freq*freqscale)]=totalstuff
    testfft_vals[int(freq*freqscale)*2]=totalstuff*1/10
    testfft_vals[int(freq*freqscale)*3]=totalstuff*36/100
    testfft_vals[int(freq*freqscale)*4]=totalstuff*7/100
    testfft_vals[int(freq*freqscale)*5]=totalstuff*6/100
    testfft_vals[int(freq*freqscale)*6]=totalstuff*5/100

    testifft_vals = ifft(testfft_vals)
    alist.extend(list(testifft_vals.real[0:totalstuff]))

def addnote_violin(samplingrate,freq,resolution,alist,duration):
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
    testfft_vals[int(freq*freqscale)]=totalstuff
    testfft_vals[int(freq*freqscale)*2]=totalstuff/4
    testfft_vals[int(freq*freqscale)*3]=totalstuff/8
    testfft_vals[int(freq*freqscale)*4]=totalstuff*3/16
    testfft_vals[int(freq*freqscale)*5]=totalstuff/2

    testifft_vals = ifft(testfft_vals)
    alist.extend(list(testifft_vals.real[0:totalstuff]))

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
                    if j == "piano":
                        addnote_piano(samplingrate,lastnote,resolution,musicdict[j],counter)
                    if j == "theremin":
                        addnote_theremin(samplingrate,lastnote,resolution,musicdict[j],counter)
                    if j == "violin":
                        addnote_violin(samplingrate,lastnote,resolution,musicdict[j],counter)
                    if j == "oboe":
                        addnote_oboe(samplingrate,lastnote,resolution,musicdict[j],counter)
                    counter = 1
            else:
                addrest(samplingrate,resolution,musicdict[j])
                counter = 1
            lastnote = currentnote
        currentnote = noteDict[templist[-1]]
        lastnote = noteDict[templist[-2]]
        if currentnote!=0:
            if j == "piano":
                addnote_piano(samplingrate,lastnote,resolution,musicdict[j],counter)
            if j == "theremin":
                addnote_theremin(samplingrate,lastnote,resolution,musicdict[j],counter)
            if j == "violin":
                addnote_violin(samplingrate,lastnote,resolution,musicdict[j],counter)
            if j == "oboe":
                addnote_oboe(samplingrate,lastnote,resolution,musicdict[j],counter)
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

def request_handler(request):
    if request['method'] == 'POST':
        '''
        esp32 module sends a post request containing a n instrument name and a string of numbers
        corresponding to what note is being played based on an 8Hz sampling rate
        '''
        conn = sqlite3.connect(soundcloud)  # connect to that database (will create if it doesn't already exist)
        c = conn.cursor()  # make cursor into database (allows us to execute commands)
        #determine if the server has stopped the recording.
        c.execute('''CREATE TABLE IF NOT EXISTS recording_table (timing real, recording integer);''') # run a CREATE TABLE command
        conn.commit()
        recording_times = c.execute('''SELECT * FROM recording_table ORDER BY timing DESC;''').fetchone()   #takes in the last two items in recoridng_table
        conn.commit() # commit commands

        if len(recording_times) == 0:
            #case when nothing in recording times exists
            output = "we aint recording"
        if recording_times[1] == 1:
            #user input asks to record current post request
            instrumentID = request['form']['instrument']
            notes_str = request['form']['notes']    #string can be put directly into the database
            c.execute('''INSERT into music_table VALUES (?,?,?);''', (time.time(),instrumentID,notes_str,))
            conn.commit() # commit commands
            output =  "added music"
        elif recording_times[1] == 0:
            output =  "time to create a wave file"
        conn.close()
        return output

    if request['method'] == 'GET':
        """
        server will send get requests to determine if the database should record the incoming
        music or not. this will be stored in a table "recording_table" within the soundcloud.
        entries: timing timestamp, recording integer (boolean does not exist in sqlite)

        if recording is set to 0, creates a wav file. Music is taken from the database
        and inputedi n the 'music_dict', storing instrument:noteList, where noteList is a
        list of integers. after note are taken from the music table, the table is deleted
        """

        recording = int(request['values']['recording'])  #value sent by the server in a get request
        conn = sqlite3.connect(soundcloud)  # connect to that database (will create if it doesn't already exist)
        c = conn.cursor()  # make cursor into database (allows us to execute commands)
        c.execute('''CREATE TABLE IF NOT EXISTS music_table (timing real, instrument text, note text);''') # timing is now stored as a floating point in seconds
        c.execute('''CREATE TABLE IF NOT EXISTS recording_table (timing real, recording integer);''') # timing is now stored as floating point in seconds
        c.execute('''insert into recording_table VALUES (?,?);''',(time.time(),recording,))
        conn.commit() # commit commands
        if recording == 0:
            c = conn.cursor()  # make cursor into database (allows us to execute commands)
            music = c.execute('''SELECT * FROM music_table ORDER BY timing ASC;''').fetchall()   #first notes inputed are at the top of the list
            record_stop, record_start = c.execute('''SELECT * FROM recording_table ORDER BY timing DESC LIMIT 2;''') #gets last two timestamps in the recording table
            conn.commit()
            record_stop = record_stop[0]
            record_start = record_start[0]  #floating point values corresponding to number of seconds
            alist = []
            music_dict = {}    #used to store strings of notes based on instrument name, hardcoded to make things easier
            for postings in music:
                #construct a dictionary of instruments mapped to notes, taking into account the sync issues
                try:
                    notes = postings[2].split(' ')
                    for note in notes:
                        if note != '':
                            music_dict[postings[1]].append(int(note))
                except:
                    #the first notes to be put in the wave file, need to be synced properly to the start time
                    notes = postings[2].split(' ')      #list of strings of numbers that correspond to a note
                    time_delta = math.floor((postings[0] - record_start)*8) - len(notes) #assumes the post request happens right after the last note was recorded at 8hz
                    if time_delta > 0:
                        added_rests = time_delta        #at 8Hz recording, for each second add 8 rests
                        music_dict[postings[1]] = [0 for rest in range(added_rests)]  # adds a bunch of rests to the beginning of the instrument dictionary
                    else:
                        notes = notes[-time_delta:]   #truncates the notes list
                        music_dict[postings[1]] = []    #the next line of code will add the notes in

                    for note in notes:
                        if note != '':
                            music_dict[postings[1]].append(int(note))

            ### addds zeros to the lists in the music dictionary for the empty time until the record stop
            for key in music_dict.keys():
                time_delta = record_stop - record_start
                zeros_to_add = time_delta*8 - len(music_dict[key])         #assuming an 8Hz recording rate, so add 8 rests per second
                for i in range(math.floor(zeros_to_add)):
                    music_dict[key].append(0)   #adds a rest note to the dictionary


            c.execute('''DROP TABLE music_table;''')    #delets the music table after the wave file is made. a new one is created each recording
            conn.commit()
            conn.close()


            alist = makeSong(music_dict, len(music_dict.keys()))
            array = np.array(alist, dtype=np.float32)
            name = '__HOME__/dynamic_musical_interfaces/wavs/'+str(time.time())
            scipy.io.wavfile.write(name+'.wav', 44100, array)
            data, samplerate = sf.read(name+'.wav')
            sf.write(name+'.ogg', data, samplerate)
            os.remove(name+'.wav')



            return  "Status: Stop"
        conn.close() # close connection to database

        return  "Status: Recording"
