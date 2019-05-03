web: gunicorn --chdir api/v1/ app:api
worker: celery --workdir=api/v1 -A utils.scheduler worker --loglevel=infoS