import requests
from os import listdir
from os.path import isfile, join
import base64
def request_handler(request):

    onlyfiles = [f for f in listdir("__HOME__/dynamic_musical_interfaces/wavs") if isfile(join("__HOME__/dynamic_musical_interfaces/wavs", f))]
    basehtml = open('__HOME__/dynamic_musical_interfaces/website.html').read()
    # for f in onlyfiles:
    #     fi = open("__HOME__/dynamic_musical_interfaces/wavs/"+f, 'rb')
    #     base64string = base64.encodestring(fi.read()).decode("utf-8")
    #     fi.close()
    #     basehtml += """
    #         <br>
    #         {}
    #         <audio controls>
    #             <source src="data:audio/wav;base64, {}" type="audio/wav">
    #         </audio>
    #     """.format(f, base64string)
    for f in onlyfiles:
        basehtml += """
            <button onclick=changeUrl("/sandbox/sc/kvfrans/dynamic_musical_interfaces/play.py?wav={}")>{}</button>
        """.format(f,f)
    basehtml += "</body></html>"
    return basehtml
