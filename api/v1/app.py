import falcon
from falcon_cors improt CORS

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

    def get_api(self):
        return self.api

cafe = Cafe()
api = cafe.get_api()