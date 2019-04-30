import sqlite3
import time
import string
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
    adds a note for a given amount of time
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
    adds a rest to the wave file
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

            array = np.array(alist)
            scipy.io.wavfile.write('__HOME__/dynamic_musical_interfaces/wavs/test2.wav', 44100, array)
            return  "you just added a recording value 0 to the database"
        conn.close() # close connection to database

        return  "you just added a recording bool 1 to the database"
