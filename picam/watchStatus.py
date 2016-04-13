
__author__ = 'siva'

import urllib2
import json
import time

camName = "TESTA"

while True :
    time.sleep(5)
    req = urllib2.Request('http://69.241.63.148/rspi/getrsstat.php?name={}'.format(camName))
    response = urllib2.urlopen(req)
    the_page = response.read()
    d = json.loads(the_page)
    if d["status"] :
        print "Video Analysis started"
    else :
        print "Camer module not started"

