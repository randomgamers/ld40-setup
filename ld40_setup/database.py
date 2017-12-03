import psycopg2
from sqlalchemy import create_engine
import datetime
from . import config
import random

def get_db():
    return create_engine(config.DATABASE_URL)


def insert_score(score, level, name=None):
    engine = get_db()
    time = datetime.datetime.utcnow().isoformat()
    engine.execute("INSERT INTO %s (name, score, level, created_at) VALUES ('%s', %f, %i, '%s')" % (config.DATABASE_TABLE, name, score, level, time))


def get_score_histogram(level):
    engine = get_db()
    min_result = engine.execute("SELECT MIN(score) FROM %s WHERE level = %i" % (config.DATABASE_TABLE, level))
    max_result = engine.execute("SELECT MAX(score) FROM %s WHERE level = %i" % (config.DATABASE_TABLE, level))
    min = list(min_result)[0][0]
    max = list(max_result)[0][0]
    query = "select width_bucket(score, %f, %f, 9) as buckets, count(*) from %s where level = %i group by buckets order by buckets" % (min, max, config.DATABASE_TABLE, level)
    hist_result = engine.execute(query)
    return [(bucket, count) for bucket, count in hist_result]


#for i in range(1000):
#    insert_score(random.gauss(500, 200), 1, 'test-' + str(i))

#print(get_score_histogram(1))
