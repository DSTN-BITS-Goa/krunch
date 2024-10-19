package app;

import org.apache.kafka.clients.producer.Producer;
import java.util.List;

/**
 * MultiThreadedCardProducer is a class designed to produce Card objects to a Kafka topic
 * using multiple threads to enhance throughput. It partitions the cards based on their IDs
 * and distributes the production tasks across a fixed number of threads.
 */
public class MultiThreadedCardProducer {

    private final int numPartitions; // DONT CHANGE

    private final SimpleCardProducer producer; // DONT CHANGE


    /**
     * Constructs a MultiThreadedCardProducer with a specified number of partitions.
     *
     * @param numPartitions number of partitions.
     */
    public MultiThreadedCardProducer(int numPartitions) {
        this.producer = new SimpleCardProducer();
        this.numPartitions = numPartitions;
    }

    /**
     * Constructs a MultiThreadedCardProducer with a specified number of partitions and a custom producer.
     *
     * @param numPartitions number of partitions.
     * @param producer Kafka Producer instance to be used for producing messages.
     */
    public MultiThreadedCardProducer(int numPartitions, Producer<String, String> producer) {
        this.producer = new SimpleCardProducer(producer);
        this.numPartitions = numPartitions;
    }

    /**
     * Produces a list of Cards to the specified Kafka topic using multiple threads.
     * ensures even distribution of Cards to partitions.
     * ensures all threads complete before returning.
     *
     * @param cards list of Card objects to be produced.
     * @param topic Kafka topic to which the cards will be sent.
     */
    public void produceCards(List<Card> cards, String topic) {
        // WRITE CODE HERE
    }

    /**
     * Flushes pending records to Kafka broker.
     */
    public void flush() {
        // WRITE CODE HERE
    }

    /**
     * close the producer and release any resources held by the class
     */
    public void close() {
        // WRITE CODE HERE
    }


    public static void main(String[] args) {
        MultiThreadedCardProducer multiThreadedProducer = new MultiThreadedCardProducer(8);

        int numCards = 100;
        List<Card> cards = Card.getRandomCards(numCards);
        long start = System.currentTimeMillis();
        multiThreadedProducer.produceCards(cards, "cards-topic");
        multiThreadedProducer.flush();
        long end = System.currentTimeMillis();

        System.out.println("Produced " + numCards + " cards in " + (end - start) + "ms");

        multiThreadedProducer.close();
    }
}
