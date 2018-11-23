import os


class Cache:
    """Cache settings for prod

    Refactored out of settings.py because its getting really long.
    Memcache is used as the default cache backend. Everything being stored in memcache comes from django-cachalot
    Redis is used just for storing sessions.

    See-Also:
    https://github.com/noripyt/django-cachalot
    https://devcenter.heroku.com/articles/django-memcache currently
    https://niwinz.github.io/django-redis/latest/
    """

    @staticmethod
    def get_cache():
        try:
            servers = os.environ["MEMCACHIER_SERVERS"]
            username = os.environ.get("MEMCACHIER_USERNAME")
            password = os.environ.get("MEMCACHIER_PASSWORD")
            cache = {
                "default": {
                    "BACKEND": "django.core.cache.backends.memcached.PyLibMCCache",
                    # TIMEOUT is not the connection timeout! It's the default expiration
                    # timeout that should be applied to keys! Setting it to `None`
                    # disables expiration.
                    "TIMEOUT": None,
                    "LOCATION": servers,
                    "OPTIONS": {
                        "binary": True,
                        "behaviors": {
                            # Enable faster IO
                            "no_block": True,
                            "tcp_nodelay": True,
                            # Keep connection alive
                            "tcp_keepalive": True,
                            # Timeout settings
                            "connect_timeout": 2000,  # ms
                            "send_timeout": 750 * 1000,  # us
                            "receive_timeout": 750 * 1000,  # us
                            "_poll_timeout": 2000,  # ms
                            # Better failover
                            "ketama": True,
                            "remove_failed": 1,
                            "retry_timeout": 2,
                            "dead_timeout": 30,
                        },
                    },
                },
                "redis": {
                    "BACKEND": "django_redis.cache.RedisCache",
                    "LOCATION": os.environ["REDIS_URL"],
                    "OPTIONS": {"CLIENT_CLASS": "django_redis.client.DefaultClient"},
                },
            }
            if password and username:
                cache["default"]["OPTIONS"]["username"] = username
                cache["default"]["OPTIONS"]["password"] = password
            return cache
        except KeyError:
            return {
                "default": {"BACKEND": "django.core.cache.backends.locmem.LocMemCache"}
            }
