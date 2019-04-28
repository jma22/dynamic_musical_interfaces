import sqlite3
import datetime
import string
import numpy
# from recording import *
import scipy.io.wavfile
import numpy as np
import math


soundcloud = '__HOME__/dynamic_musical_interfaces/soundcloud.db'  #database

"""
database entry will contain timing, instrument name, string
containing numbers for each note value. Assuming a sampling
rate of 8 hz?

post request form: instrument=?&notes=?
"""


def addnote(samplingrate,freq,resolution,alist):
    """
    jeremy is retarded
    """
    noteduration = 1/samplingrate
    totalstuff = int(noteduration*resolution)
    period = resolution/freq
    counter = 0

    for dot in range(totalstuff):
        alist.append(np.int16(32767*math.cos(2*3.14/period*dot)))
        
        # if(counter==period):
        #     alist.append(0.99)
        #     counter = 0
        # else:
        #     alist.append(0)
        #     counter +=1

def addrest(samplingrate,resolution,alist):
    """
    im cool
    """
    noteduration = 1/samplingrate
    totalstuff = int(noteduration*resolution)

    for dot in range(totalstuff):
        alist.append(0)

def request_handler(request):
    if request['method'] == 'POST':
        '''
        esp32 module sends a post request containing a n instrument name and a string of numbers
        corresponding to what note is being played based on an 8Hz sampling rate
        '''
        conn = sqlite3.connect(soundcloud)  # connect to that database (will create if it doesn't already exist)
        c = conn.cursor()  # make cursor into database (allows us to execute commands)
        #determine if the server has stopped the recording.
        c.execute('''CREATE TABLE IF NOT EXISTS music_table (timing timestamp, instrument text, note text);''') # run a CREATE TABLE command
        c.execute('''CREATE TABLE IF NOT EXISTS recording_table (timing timestamp, recording integer);''') # run a CREATE TABLE command
        conn.commit()

        c = conn.cursor()  # make cursor into database (allows us to execute commands)
        recording_times = c.execute('''SELECT * FROM recording_table ORDER BY timing DESC;''').fetchone()   #takes in the last two items in recoridng_table
        conn.commit() # commit commands

        if len(recording_times) == 0:
            #case when nothing in recording times exists
            return "we aint recording"
        if recording_times[1] == 1:
            #user input asks to record current post request
            instrumentID = request['form']['instrument']
            notes_str = request['form']['notes']    #string can be put directly into the database
            c.execute('''INSERT into music_table VALUES (?,?,?);''', (datetime.datetime.now(),instrumentID,notes_str,))
            conn.commit() # commit commands
            conn.close() # close connection to database
            return "added music"
        elif recording_times[1] == 0:
            #case when user input from website asked to stop recording
            #this will initialize creation of a wave file
            # c = conn.cursor()
            # c.execute('''DROP TABLE music_table;''')   #this deletes the music_table so that memory doesnt overflow
            # conn.commit() # commit commands
            # conn.close() # close connection to database
            return "time to create a wave file"

    if request['method'] == 'GET':
        """
        server will send get requests to determine if the database should record the incoming
        music or not. this will be stored in a table "recording_table" within the soundcloud.
        entries: timing timestamp, recording integer (boolean does not exist in sqlite)
        """
        
        recording = int(request['values']['recording'])  #value sent by the server in a get request
        conn = sqlite3.connect(soundcloud)  # connect to that database (will create if it doesn't already exist)
        c = conn.cursor()  # make cursor into database (allows us to execute commands)
        c.execute('''CREATE TABLE IF NOT EXISTS recording_table (timing timestamp, recording integer);''') # run a CREATE TABLE command
        c.execute('''insert into recording_table VALUES (?,?);''',(datetime.datetime.now(),recording,))
        conn.commit() # commit commands
        
        # check if 1 first
        if recording == 0:
            c = conn.cursor()  # make cursor into database (allows us to execute commands)
            music = c.execute('''SELECT * FROM music_table ORDER BY timing DESC;''').fetchall()   #takes in the last two items in recoridng_table
            alist = []
            # return music
            for timing, instrument, notes in music:
                for n in notes.split(" "):
                    if n != "":
                        ni = int(n)
                        convert = {0: 440, 1: 493.8, 2: 523.25, 3: 587.33}
                        if ni == 9:
                            addrest(8, 44100, alist)
                        else:
                            addnote(8, convert[ni], 44100, alist)
            array = np.array(alist)
            scipy.io.wavfile.write('__HOME__/dynamic_musical_interfaces/wavs/test2.wav', 44100, array)
            conn.commit() # commit commands
            conn.close()
            return "lmaokai"
        conn.close() # close connection to database

        return  "you just added a recording bool 1 to the database"
