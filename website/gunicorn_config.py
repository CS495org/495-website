import multiprocessing
import os

bind = "0.0.0.0:8000"
workers = multiprocessing.cpu_count() * 2 + 1
threads = 2
worker_class = "gthread"
timeout = 30
graceful_timeout = 30
keepalive = 2

# Logging
accesslog = '-'  # Log to stdout
errorlog = '-'   # Log to stderr
loglevel = 'info'
# options (increasing verbosity): critical, error, warning, info, debug

# Security
limit_request_line = 4094
limit_request_fields = 100
limit_request_field_size = 8190

# Worker settings
worker_connections = 1000
max_requests = 1000
max_requests_jitter = 50

# Preload the application
preload_app = True

# Django-specific settings
# pythonpath = "/"  # Set the path to your Django project
# chdir = "/"       # Change to your Django project directory

# Enable or disable Gunicorn daemon mode
daemon = False