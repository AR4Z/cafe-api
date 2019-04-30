import falcon
from utils import req_to_dict
import json

class ScheduleCollectionResource(object):
    def on_post(self, req, resp):
        schedule  = req_to_dict(req)

    

