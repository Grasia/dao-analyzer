import multiprocessing

bind = ':80'
timeout = 1200
proc_name = 'DAO-Analyzer'
loglevel = 'debug'
errorlog = '-'
workers = multiprocessing.cpu_count() * 2 + 1
