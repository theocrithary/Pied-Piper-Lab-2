import redis
#r = redis.Redis(host='', port='5379')
#r = redis.Redis(host='', port='15379', password='')


######################
#### WORKING WITH KEYS
#r.set('mykey','PiedPiper')
#### Single key
#print r.get('mykey')
#print r.exists('mykey')
#r.delete('mykey')
#### Multiple keys at once
#r.mset({'mykey1':'value1', 'mykey2':123})
#### Handy way to create and increment a counter
#print r.incr('mycounter') # Increment by one
#print r.incrby('mycounter',10) # Increment by any number

#######################
#### WORKING WITH LISTS
#r.lpush('mylist', 'item1')
#r.rpush('mylist', 'item2')
#r.rpush('my.list','item3','item4') #Insert multiple items
#### Display the length of the list
#print r.llen('mylist')
#### Extract a section of the list: list_name, start_position, last_position
#print r.lrange('mylist',0,-1)  # Positions start from 0. Last position is -1
#### Pops out an item and the list shrinks
#print r.lpop('mylist')
#print r.rpop('mylist')
#print r.llen('mylist')
#### Trim operation. Handy if you want to insert items but keep same list size
#print r.llen('mylist')
#r.lpush('mylist','item0')
#r.ltrim('mylist',0,1)
#print r.llen('mylist')
#r.delete('mylist')

########################
#### WORKING WITH HASHES
#r.hset('myhash','field1','some value') # Setting and existing field overwrites it
#r.hmset('myhash', {'field2':True, 'field3': 145})
#print r.hget('myhash','field1')
#print r.hmget('myhash','field1','field2','field3')
#print r.hincrby('myhash','field3',10)
#r.delete('myhash')

######################
#### WORKING WITH SETS
#r.sadd('myset', 1, 2, 3)
#print r.smembers('myset')
#print r.sismember('myset', 3)
#print r.scard('myset') # Use this to display the amount of elements
#r.delete('myset')
# Other tutorials for more SET operations like intersections

###########################
#### SORTED SET SECTION TBC
