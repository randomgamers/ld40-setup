import psycopg2
from sqlalchemy import create_engine
import datetime
from . import config
import random
import numpy as np


connection = None


def get_db():
    global connection

    if connection is None:
        connection = create_engine(config.DATABASE_URL)
    return connection


def insert_score(score, level, name=None):
    try:
        engine = get_db()
        time = datetime.datetime.utcnow().isoformat()
        engine.execute("INSERT INTO %s (name, score, level, created_at) VALUES ('%s', %f, %i, '%s')" % (config.DATABASE_TABLE, name, score, level, time))
    except:
        print("Couldn't connect to the database")


def get_score_histogram(level):
    try:
        engine = get_db()
        min_result = engine.execute("SELECT MIN(score) FROM %s WHERE level = %i" % (config.DATABASE_TABLE, level))
        max_result = engine.execute("SELECT MAX(score) FROM %s WHERE level = %i" % (config.DATABASE_TABLE, level))
        min = (list(min_result)[0][0] or 0) - 1
        max = (list(max_result)[0][0] or 0) + 1
        query = "select width_bucket(score, %f, %f, 9) as buckets, count(*) from %s where level = %i group by buckets order by buckets" % (min, max, config.DATABASE_TABLE, level)
        hist_result = engine.execute(query)
        bucket_size = (max-min)/10
        counts = np.zeros((10))
        buckets = ([(min + i*bucket_size, min + (i + 1)*bucket_size) for i in range(10)])
        for bucket, count in hist_result:
            counts[bucket - 1] = count
        return list(zip(buckets, counts))
    except:
        print("Couldn't connect to the database")
        return None


try:
    get_db()
except:
    print("Couldn't connect to the database")

#for i in range(1000):
#    insert_score(random.gauss(500, 200), 1, 'test-' + str(i))

#print(get_score_histogram(2))
