
import redis

r = redis.Redis(
	host='10.11.157.211',
	port=6379)
r.set('foo', 'bar')
value = r.get('foo')
print(value)