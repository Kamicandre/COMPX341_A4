import time

import redis
from flask import Flask

app = Flask(__name__)
cache = redis.Redis(host='redis', port=6379)

cache.delete('PrimeList')
pl = "PrimeList"
x = 0
store = []

def get_hit_count():
    retries = 5
    while True:
        try:
            return cache.incr('hits')
        except redis.exceptions.ConnectionError as exc:
            if retries == 0:
                raise exc
            retries -= 1
            time.sleep(0.5)

# Decides if the input integer is prime and returns /<number> is prime/ or /<number> is not prime/
@app.route('/isPrime/<int:number>')
def isPrime(number):
    global store
    if number > 1:
        if number == 2:
            s = str(number)
            if number not in store:
                storeRedis(s)
                store.append(number)
            return '{} is prime'.format(number)
        else:
            for i in range(2,number):
                if number % i == 0:
                    return '{} is not prime'.format(number)
                    break
                elif number == 2147483647:
                    s = str(number)
                    if number not in store:
                        storeRedis(s)
                        store.append(number)
                    return '{} is prime'.format(number)
                    break
            s = str(number)
            if number not in store:
                storeRedis(s)
                store.append(number)
            return '{} is prime'.format(number)
            
    else:
        return 'Number must not be 0 or 1'

def storeRedis(string):
    s ='[{}] '.format(string)
    global x
    x = 1
    cache.append(pl,s)

@app.route('/primesStored')
def primesStored():
    if x > 0:
        save = cache.get(pl)
        return save
    else:
        return "No list found"

@app.route('/primesStored/delete')
def checkList():
    cache.delete(pl)
    global store
    store.clear()
    global x
    x = 0
    return 'List deleted'
    
@app.route('/')
def hello():
    count = get_hit_count()
    return 'Hello from Adrien, have a nice day! I have been seen {} times.\n'.format(count)
