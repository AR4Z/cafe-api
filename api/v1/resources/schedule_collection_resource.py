import falcon
from utils import req_to_dict, schedule
from celery.result import AsyncResult
import json

class ScheduleCollectionResource(object):
    def on_post(self, req, resp):
        schedule_data  = req_to_dict(req)
        task_schedule = schedule.delay(schedule_data)
        resp.status = falcon.HTTP_202
        resp.body = json.dumps({
            'id_scheduler': task_schedule.id
        })

    def on_get(self, req, resp, schedule_id):
        scheduler_result = AsyncResult(schedule_id)
        if isinstance(scheduler_result.result, str):
            result = {
                'status': scheduler_result.status,
                'message': scheduler_result.result
            }

            resp.status = falcon.HTTP_200
            resp.body = json.dumps(result)
        else:
            result = {
                'status': scheduler_result.status,
                'schedule': scheduler_result.result
            }

            resp.status = falcon.HTTP_200
            resp.body = json.dumps(result) 
