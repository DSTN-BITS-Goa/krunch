# Lab 4: In Lab


## Requirements

- Maven
- Java 22

## Usage

To test your solution:

```bash
    cd PATH/TO/lab4/in-lab
    mvn test
```
## Background

- In this lab you will implement a simple Kafka [streams](src/main/java/app/CardStreamProcessor.java) application

## Starter code

- You are given a [Card](src/main/java/app/Card.java) class
- You are given [CardStreamProcessor](src/main/java/app/CardStreamProcessor.java) class
  - `CardStreamProcessor` is an api for a streams application that reads an input stream of cards (string representations) and flags duplicate cards within a 30 millisecond time window to an output topic
  - A card in the input stream is flag if it occurs twice in a 30 millisecond time window
  - You can assume that a 30 millisecond time window will have atmost 2 occurences of the same card
  - Note that the same card may be flagged multiple times during different windows
  - When flagging a card to the output topic, both the key and value are the card
    
- The default constructor of the class can be used to run them on the local Kafka cluster
- The main functions of the class can be used to test your implementation on the local Kafka cluster
- Ensure the Kafka cluster is running before running the main functions of the class
```bash
  # in the root directory of the project
  # spins up a single node kafka cluster on docker
  docker-compose up
```

- To view the contents of your topic on the local kafka cluster
```bash
    docker-compose exec kafka kafka-console-consumer.sh --bootstrap-server kafka:9092 --topic cards-flag-topic --from-beginning
```

## Question

- Implement the classes described above
- You are free to add code wherever you want, just dont modify any already existing code