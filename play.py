import requests
from os import listdir
from os.path import isfile, join
import base64
def request_handler(request):
    file = request['values']['wav']
    fi = open("__HOME__/dynamic_musical_interfaces/wavs/"+file, 'rb')
    base64string = base64.encodestring(fi.read()).decode("utf-8")
    fi.close()
    basehtml = """
        <br>
        
        <audio controls style="width: 1000px;">
            <source src="data:audio/wav;base64, {}" type="audio/wav">
        </audio>
    """.format(base64string)
    return basehtml
