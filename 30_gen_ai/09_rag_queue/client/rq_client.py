# Import Redis client to connect with Redis/Valkey server
from redis import Redis

# Import Queue class from RQ (Redis Queue)
from rq import Queue

# Create a Queue instance
queue = Queue(
    connection=Redis(
        host="localhost",   # Redis server host (running locally)
        port=6379           # Redis server port (default is 6379)
    )
)