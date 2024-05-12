import numpy as np
from pyspark.sql import SparkSession
from pyspark.ml.evaluation import RegressionEvaluator
from pyspark.ml.feature import StringIndexer
from pyspark.ml.recommendation import ALS
from pyspark.sql.functions import col, udf, array, lit
from pyspark.sql.types import FloatType

# making a spark session
sparkSession = SparkSession.builder \
    .appName("Music Recommendation System") \
    .config("spark.mongodb.input.uri", "mongodb://127.0.0.1/MuneebTest.SpotifyBDATest") \
    .config("spark.mongodb.output.uri", "mongodb://127.0.0.1/MuneebTest.SpotifyBDATest") \
    .config("spark.jars.packages", "org.mongodb.spark:mongo-spark-connector_2.12:3.0.1") \
    .getOrCreate()

# Loading data from Mongo Database and creating a dataframe
dataFrame = sparkSession.read.format("com.mongodb.spark.sql.DefaultSource").load()

# Indexing track_id and genre_all
indexers = [
    StringIndexer(inputCol="track_id", outputCol="user_id_indexed"),
    StringIndexer(inputCol="genre_all", outputCol="item_id_indexed")
]

for indexer in indexers:
    ALSmodel = indexer.fit(dataFrame)
    dataFrame = ALSmodel.transform(dataFrame)

# making a dummy ratings column to use later
AlteredDataFrame = dataFrame.withColumn("rating", col("item_id_indexed") % 5 + 1)  # Example to generate ratings

# Spliting the data into training and testing datasets
(training, test) = AlteredDataFrame.randomSplit([0.8, 0.2])

# using ALS to build the spotify reccomendation system
alsDetails = ALS(
    maxIter=5,
    regParam=0.01,
    userCol="user_id_indexed",
    itemCol="item_id_indexed",
    ratingCol="rating",
    coldStartStrategy="drop",
    implicitPrefs=True
)

ALSmodel = alsDetails.fit(training)

# getting itemfactors of the als model for processing
itemFactors = ALSmodel.itemFactors

# using udf to find cosine similarity and find the most similar songs according to that
@udf(FloatType())

def cosineSimilarityFinderFunction(x, y):
    temp = float(np.dot(x, y) / (np.linalg.norm(x) * np.linalg.norm(y)))
    return temp

# findingSimilarSongs function is defined to find the any number of similar songs that the user wants. It takes in 2 arguments id of the first song that is the baseline jiske similar niqalne hai
def findingSimilarSongsFunc(songIDnum, numberOfSongsToFind):
    targetFactor_ = itemFactors.filter(col("id") == songIDnum).select("features").first()
    if targetFactor_:
        targetFactor_ = targetFactor_['features']
        similarities = itemFactors.withColumn("similarity", cosineSimilarityFinderFunction(col("features"), array([lit(float(x)) for x in targetFactor_])))
        MostSimilarSongs = similarities.sort(col("similarity").desc()).limit(numberOfSongsToFind + 1)
        return MostSimilarSongs.filter(col("id") != songIDnum)
    else:
        return None

#testing the output
similar_songs = findingSimilarSongsFunc(105, 15)
if similar_songs:
    similar_songs.show()

sparkSession.stop()
