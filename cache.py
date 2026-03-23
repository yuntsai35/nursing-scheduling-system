import redis

r = redis.Redis(
        host='redis-15587.crce285.us-east-1-4.ec2.cloud.redislabs.com', 
        port=15587, 
        password='IKXOo1JGf19XnGO8cAVPGHvqg4idNg8b', 
        decode_responses=True
    )

def get_redis():
    return r