# Lab 4: Take Home


## Requirements

- Maven
- Java 22

## Usage

To test your solution:

```bash
    cd PATH/TO/lab4/take-home
    mvn test    
    # to run a specific test class
    mvn -Dtest=CardProducerTest test
```
## Background

- In this lab you will implement a simple Kafka [producer](src/main/java/app/SimpleCardProducer.java) and [consumer](src/main/java/app/SimpleCardConsumer.java) class to produce and consume [Cards](src/main/java/app/Card.java)
- You will additionally implement a multi threaded version of the [producer](src/main/java/app/MultiThreadedCardProducer.java)
- This lab uses [Maven](https://maven.apache.org/) as the build tool
  - Great [tutorial](https://www.youtube.com/watch?v=Xatr8AZLOsE) to get familiar with Maven
- This [article](https://medium.com/@vinciabhinav7/concurrency-in-java-executorservice-future-and-callable-f22a7fbeefe2) explains key java features for multi threaded applications

## Starter code

- You are given a [Card](src/main/java/app/Card.java) class
- You are given 3 classes
  - [SimpleCardProducer](src/main/java/app/SimpleCardProducer.java)
  - [SimpleCardConsumer](src/main/java/app/SimpleCardConsumer.java)
  - [MultiThreadedCardProducer](src/main/java/app/MultiThreadedCardProducer.java)
    - Kafka usually load balances messages across partitions based on the key, but for the purposes of testing you will need to distribute the messages among the partitions yourself
    - In the `produceCards` method, its up to you to decide how to distribute the cards list among the partitions
    - Ensure that the scheme evenly distributes the cards, the stress tests will check that all partitions have atleast one record
    - Also ensure that the `produceCards` method waits for all threads to complete before returning
    
- The default constructor of the classes can be used to run them on the local Kafka cluster
- The main functions of the classes can be used to test your implementation on the local Kafka cluster
- Ensure the Kafka cluster is running before running the main functions of the classes
```bash
  # in the root directory of the project
  # spins up a single node kafka cluster on docker
  docker-compose up
```
- Additionally before running the main function of MultiThreadedCardProducer, ensure the topic is created with the appropriate number of partitions
```bash
  docker-compose exec kafka kafka-topics.sh --bootstrap-server localhost:9092 --delete --topic cards-topic
  docker-compose exec kafka kafka-topics.sh --bootstrap-server :9092 --create --replication-factor 1 --partitions 8 --topic cards-topic
```
- To view the contents of your topic on the local kafka cluster
```bash
    docker-compose exec kafka kafka-console-consumer.sh --bootstrap-server kafka:9092 --topic cards-topic --from-beginning```
```

## Question

- Implement the classes described above
- You are free to add code wherever you want, just dont modify any already existing code
- Perf tasks
  - Observe the time difference between the SimpleCardProducer and MultiThreadedCardProducer
  - Try running them for 10,000,000 cards and see the difference
  - What possible reasons are there for performance differences observed?
  - Are the performance differences consistent across runs and across machines?
  - For the producer side, look into tweaking the following properties
    - `buffer.memory`
    - `batch.size`
    - `linger.ms`
    - What effects did you observe?
  - For the consumer side, look into tweaking the following properties
    - `fetch.min.bytes`
    - `max.poll.records`
    - `max.poll.interval.ms`
    - `receive.buffer.bytes`
    - `max.partition.fetch.bytes`
    - What effects did you observe?