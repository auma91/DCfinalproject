
import redis

import redis
redisConnection = redis.Redis(
	host='localhost',
	port=6379)
redisConnection.set('foo', 'bar')
value = redisConnection.get('foo')
print(value)
redisConnection.close()