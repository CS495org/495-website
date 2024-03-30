# URLS/backend need to be env vars

broker_url = 'redis://redis:6379/0'
result_backend = 'redis://redis:6379/0'
task_serializer = 'json'
result_serializer = 'json'
accept_content = ['json']
timezone = 'UTC'