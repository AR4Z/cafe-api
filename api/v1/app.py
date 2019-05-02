import falcon
from falcon_cors import CORS
from resources import ScheduleCollectionResource

class Cafe():
    def __init__(self):
        self.api = falcon.API(middleware=[
            CORS(
                allow_all_origins=True,
                allow_all_methods=True,
                allow_all_headers=True,
                expose_headers_list=[
                    'Content-Range',
                ],
            ).middleware
        ])
        self.api.add_route('/v1/schedule', ScheduleCollectionResource())
        self.api.add_route('/v1/schedule/{schedule_id}', ScheduleCollectionResource())

    def get_api(self):
        return self.api

cafe = Cafe()
api = cafe.get_api()