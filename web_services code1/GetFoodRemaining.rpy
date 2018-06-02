# Import necessary files
from twisted.internet import reactor, endpoints
from twisted.web.server import Site
from twisted.web.resource import Resource

import os
import subprocess

class GetFood(Resource):
    isLeaf = True
    def render_GET(self, request):
        p = subprocess.Popen("python /home/pi/Food_Water_Files/GetFoodRemaining.py", stdout=subprocess.PIPE, shell=True)
	return p.stdout.read()

resource = GetFood()
