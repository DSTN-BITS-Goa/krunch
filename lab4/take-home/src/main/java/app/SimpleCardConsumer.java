package app;

import com.google.gson.Gson;
import org.apache.kafka.clients.consumer.Consumer;
import org.apache.kafka.clients.consumer.KafkaConsumer;
import org.apache.kafka.common.errors.WakeupException;

import java.io.File;
import java.io.IOException;
import java.util.*;

/**
 * SimpleCardConsumer is a class responsible for consuming card data from a Kafka topic.
 * It utilizes the Kafka Consumer API to read serialized GSON representations of Card objects
 * from a specified Kafka topic and store them in a list.
 */
public class SimpleCardConsumer {

    private final boolean inDocker = new File("/.dockerenv").exists(); // DONT CHANGE

    private final List<Card> consumedCards = new ArrayList<>(); // DONT CHANGE

    private final Consumer<String, String> consumer; // DONT CHANGE


    /**
     * Default constructor that initializes the Kafka consumer using default properties.
     */
    public SimpleCardConsumer() {
        this.consumer = createKafkaConsumer();
    }

    /**
     * Constructor that allows passing a custom Kafka consumer instance.
     *
     * @param consumer A Kafka consumer instance to be used for consuming messages.
     */
    public SimpleCardConsumer(Consumer<String, String> consumer) {
        this.consumer = consumer;
    }

    /**
     * Creates and configures a Kafka consumer instance using properties loaded from a file.
     * This method checks if the application is running in a Docker environment and adjusts
     * the Kafka bootstrap servers accordingly.
     *
     * @return A configured KafkaConsumer instance.
     */
    public Consumer<String, String> createKafkaConsumer() { // DONT CHANGE
        try (var stream = Consumer.class.getClassLoader().getResourceAsStream("consumer.properties")) {
            Properties props = new Properties();
            props.load(stream);
            props.setProperty("client.id", "consumer-" + UUID.randomUUID());
            props.setProperty("group.instance.id", props.getProperty("client.id"));

            if (inDocker) {
                // Use Docker-specific Kafka bootstrap servers if in Docker
                props.setProperty("bootstrap.servers", props.getProperty("bootstrap.servers.docker"));
            }

            return new KafkaConsumer<>(props);
        } catch (IOException e) {
            throw new RuntimeException(e);
        }
    }

    /**
     * Consumes Card objects from the specified Kafka topic in an infinite loop.
     * Each consumed Card is deserialized and added to the consumedCards list.
     *
     * @param topic The Kafka topic from which to consume cards.
     */
    public void consumeCards(String topic) {

        try {
            while (true) {


            }
        } catch (WakeupException e) { // DONT CHANGE
            System.out.println("Shutting down...");
        } finally { // DONT CHANGE
            close();
        }
    }

    /**
     * close the consumer and release any resources held by the class
     */
    public void close() {
        // WRITE CODE HERE
    }

    /**
     * Returns the list of consumed Card objects.
     *
     * @return A List containing the consumed Card objects.
     */
    public List<Card> getConsumedCards() {
        return consumedCards;
    }

    /**
     * This method can be used to stop the consumer gracefully.
     */
    public void stop() {
        consumer.wakeup(); // Wake up the consumer to exit the polling loop
    }

    public static void main(String[] args) {
        SimpleCardConsumer simpleCardConsumer = new SimpleCardConsumer();
        simpleCardConsumer.consumeCards("cards-topic");
    }
}
