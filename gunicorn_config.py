import multiprocessing

wsgi_app = 'dao_analyzer.web:create_app()'
bind = ':80'
timeout = 1200
proc_name = 'DAO-Analyzer'
loglevel = 'info'
errorlog = '-'
workers = multiprocessing.cpu_count() * 2 + 1
raw_env = [
  # A bug with gunicorn and dash makes it so its always hot-reloading
  "DASH_HOT_RELOAD=false",
]
