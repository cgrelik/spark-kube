from pyspark.sql import SparkSession
from pyspark.sql.functions import col, when, avg, count
import sys

def spark_run(params, spark):
    # csv containing chess data from Lichess
    df = spark.read.csv('games.csv',header=True)

    # Get all polish opening games
    openings = df.filter(col('moves').startswith(params))

    stats = openings.select(avg(when(col('winner')=='white', 1).otherwise(0)).alias('white_win_rate'), \
                            avg(when(col('winner')=='black', 1).otherwise(0)).alias('black_win_rate'), \
                            avg(when(col('winner')=='draw', 1).otherwise(0)).alias('draw_rate'), \
                            count(col('winner')))
    logger.debug(stats.show())

if __name__ == '__main__':
    params = " ".join(sys.argv[1:])
    spark = SparkSession.builder.appName('ChessOpenings').getOrCreate()
    log4jLogger = spark._jvm.org.apache.log4j
    logger = log4jLogger.LogManager.getLogger(__name__)
    logger.debug('Starting spark...')

    spark_run(params, spark)
