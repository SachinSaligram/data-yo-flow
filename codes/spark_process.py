#============================================================================================
#@author: Sachin Saligram, Akanksha Singh, Siddharth Sharma
#@description: This code is a sample processing task to check if we are receiving data from
#              Apache Kafka in a appropriate manner. Once evaluation is done, data processing
#              tasks will be updated to match the current use case.
#============================================================================================

from pyspark import SparkConf, SparkContext
from pyspark.streaming import StreamingContext
from pyspark.streaming.kafka import KafkaUtils
import operator
import numpy as np
import matplotlib.pyplot as plt


def main():
    conf = SparkConf().setMaster("local[2]").setAppName("Streamer")
    sc = SparkContext(conf=conf)
    ssc = StreamingContext(sc, 10)   # Create a streaming context with batch interval of 10 sec
    ssc.checkpoint("checkpoint")
    sc.setLogLevel("ERROR")

    pwords = load_wordlist("positive.txt")
    nwords = load_wordlist("negative.txt")
   
    counts = stream(ssc, pwords, nwords, 100)
    make_plot(counts)


def make_plot(counts):
    """
    Plot the counts for the positive and negative words for each timestep.
    Use plt.show() so that the plot will popup.
    """
    positive_count = []
    negative_count = []
    
    for count in counts:
        for word in count:
            if word[0] == "positive":
                positive_count.append(word[1])
            else:
                negative_count.append(word[1])

    plt.axis([-1, len(positive_count), 0, max(max(positive_count),max(negative_count))+110])
    pos, = plt.plot(positive_count, 'b-', marker = 'o', markersize = 10)
    neg, = plt.plot(negative_count, 'g-', marker = 'o', markersize = 10)
    plt.legend((pos,neg),('Positive','Negative'),loc=2)
    plt.xticks(np.arange(0, len(positive_count), 1))
    plt.xlabel("Time Step")
    plt.ylabel("Word Count")
    plt.show()



def load_wordlist(filename):
    """ 
    This function should return a list or set of words from the given filename.
    """
    wordList = []
    f = open(filename, 'rU')
    for line in f:
        wordList.append(line.strip())
    f.close()
    return wordList


def updateFunction(newValues, runningCount):
    if runningCount is None:
        runningCount = 0
    return sum(newValues, runningCount)


def stream(ssc, pwords, nwords, duration):
    kstream = KafkaUtils.createDirectStream(ssc, topics = ['twitterstream'], kafkaParams = {"metadata.broker.list": 'localhost:9092'})
    tweets = kstream.map(lambda x: x[1].encode("ascii","ignore"))

    # Each element of tweets will be the text of a tweet.
    # You need to find the count of all the positive and negative words in these tweets.
    # Keep track of a running total counts and print this at every time step (use the pprint function).

    # Obtain list of words from tweets
    tweet_words = tweets.flatMap(lambda line: line.split(" "))
    
    # Filter for words either in the postive list or negative list of words
    tweet_words = tweet_words.filter(lambda word: (word in pwords) or (word in nwords))

    # Label and map each word to either 'positive' or 'negative', and 1 respectively
    wordPairs = tweet_words.map(lambda word: ('positive', 1) if (word in pwords) else ('negative', 1))

    # Count and print the number of postive and negative words
    wordCounts = wordPairs.reduceByKey(lambda x, y: x + y)
    totalCount = wordPairs.updateStateByKey(updateFunction)
    totalCount.pprint()
    
    # Let the counts variable hold the word counts for all time steps
    # You will need to use the foreachRDD function.
    # For our implementation, counts looked like:
    #   [[("positive", 100), ("negative", 50)], [("positive", 80), ("negative", 60)], ...]
    counts = []
    wordCounts.foreachRDD(lambda t,rdd: counts.append(rdd.collect()))
    
    # Start the computation
    ssc.start()
    ssc.awaitTerminationOrTimeout(duration)
    ssc.stop(stopGraceFully=True)

    return counts


if __name__=="__main__":
    main()
