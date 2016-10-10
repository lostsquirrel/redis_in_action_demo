import redis

QUIT = False
LIMIT = 10000000
REDIS_HOST = '192.168.1.139'
conn = redis.Redis(REDIS_HOST)
