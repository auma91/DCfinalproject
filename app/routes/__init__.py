import redis
redisConnection = redis.Redis(
	host='localhost',
	port=6379)
redisConnection.connection.host = "10.11.157.211"
def init_app(appf):
	global app
	app = appf