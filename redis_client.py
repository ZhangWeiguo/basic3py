from redis import Redis,ConnectionPool


class RedisClient(Redis):
    def __init__(self, *args, **kwargs):
        super(Redis, self).__init__(*args, **kwargs)

    def close(self):
        pass
