import sqlite3
import datetime
import string
import numpy

soundcloud = '__HOME__/project/soundcloud.db'  #database

"""
database entry will contain timing, instrument name, string
containing numbers for each note value. Assuming a sampling
rate of 8 hz?

post request form: instrument=?&notes=?
"""

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
            return
        elif recording_times[1] == 0:
            #case when user input from website asked to stop recording
            #this will initialize creation of a wave file
            c = conn.cursor()
            c.execute('''DROP TABLE music_table;''')   #this deletes the music_table so that memory doesnt overflow
            conn.commit() # commit commands
            conn.close() # close connection to database
            return "time to create a wave file"

    if request['method'] == 'GET':
        """
        server will send get requests to determine if the database should record the incoming
        music or not. this will be stored in a table "recording_table" within the soundcloud.
        entries: timing timestamp, recording integer (boolean does not exist in sqlite)
        """
        recording = request['values']['recording']  #value sent by the server in a get request
        conn = sqlite3.connect(soundcloud)  # connect to that database (will create if it doesn't already exist)
        c = conn.cursor()  # make cursor into database (allows us to execute commands)
        c.execute('''CREATE TABLE IF NOT EXISTS recording_table (timing timestamp, recording integer);''') # run a CREATE TABLE command
        c.execute('''insert into recording_table VALUES (?,?);''',(datetime.datetime.now(),recording,))
        conn.commit() # commit commands
        conn.close() # close connection to database
        return  "you just added a recording bool to the database"
