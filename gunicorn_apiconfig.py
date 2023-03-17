bind = '0.0.0.0:5001'
worker_class = 'sync'
workers = '1'
loglevel = 'debug'
accesslog = 'log/gunicorn/access_log_wtapi'
acceslogformat ="%(h)s %(l)s %(u)s %(t)s %(r)s %(s)s %(b)s %(f)s %(a)s"
errorlog =  'log/gunicorn/error_log_wtapi'

#keyfile = '/etc/letsencrypt/live/workteams.ifechukwu001.tech/privkey.pem'
#certfile = '/etc/letsencrypt/live/workteams.ifechukwu001.tech/cert.pem'
#ca_certs = '/etc/letsencrypt/live/workteams.ifechukwu001.tech/chain.pem'