from . import redisConnection

def insert(userid, serial):
	redisConnection.set(str(userid), str(serial))
def get(userid):
	redisConnection.get(str(userid))