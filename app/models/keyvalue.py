import redis
class redisConnection():
	def __init__(self, host):
		self.r = None
	def setConnection(self, host):
		self.r = redis.Redis(host=host, port = 6379)
	def insert(self, userid, serial):
		self.r.set(str(userid), str(serial))
	def get(self, userid):
		self.r.get(str(userid))