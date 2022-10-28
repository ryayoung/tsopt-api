# Maintainer:     Ryan Young
# Last Modified:  Oct 08, 2022
from redis_om import get_redis_connection

redis = get_redis_connection(
        host="redis-11217.c279.us-central1-1.gce.cloud.redislabs.com",
        port=11217,
        password="fxToQoPDu2gsv9v9d8bhvL4kRsMaGW9a",
        decode_responses=True,
)
