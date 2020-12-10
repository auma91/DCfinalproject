
import redis

import redis
redisConnection = redis.Redis(
	host='localhost',
	port=6379)
redisConnection.connection.host = "10.11.157.211"
redisConnection.set('foo', 'bar')
value = redisConnection.get('foo')
print(value)
redisConnection.close()