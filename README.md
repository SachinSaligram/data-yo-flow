# Team4Project

- Siddharth Sharma
- Sachin Saligram
- Akanksha Singh

## Consume multiple real time data streams and provide analytics and a unified search interface.

The idea of this project is to build a robuts and efficient data pipeline that scales seamlessly with increase in input data sources and analytical processing tasks. The distributed processing framework includes Apache Kafka for buffering data, Apache Spark for processing data, MongoDB for storage, and Elasticseach + Kibana for custom queries and visualization.


### Updates

  __1. 1st October 2017__

  * We we able to succesfully obtain streaming data (JSON) from our first data source, Twitter API.
  * Conducted a reading session and evaluation of technologies we could use to build our data pipeline. Some technologies considered are Apache Spark, Apache Kafka, Cassandra, MongoDB, Impala, Elasticsearch to name a few.

  __2. 8th October 2017__

  * We have connected the Twitter API, Apache Kafka and Apache Spark.
  * Currently able to supply JSON streaming data to Kafka for buffering. This data is fed to Apache Spark in batch intervals for some basic sample processing to check for working stability. Processing tasks to be done in Spark will be subsequently added depending on requirements.

  __3. 15th October 2017__

  * Implemented a parallel process to store JSON streaming data from Twitter API in MongoDB for persistant, fault tolerant storage.
  * Currently exploring the possibility of supplying a subset of data in MongoDB to Elasticsearch to allow for custom queries.


### Pending Tasks

1. Connect MongoDB to Elasticsearch+Kibana to provide visualizations for custom queries.
2. Move the framework to a VCL cluster to check for performance issues and bugs.
3. Add/update data processing tasks in Apache Spark.
  
__Note__: Implementations are currently being done on local machine with the hope of moving it to a VCL cluster by the end of October.
