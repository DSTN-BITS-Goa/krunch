package app;

import com.google.gson.Gson;
import org.apache.kafka.clients.consumer.MockConsumer;
import org.apache.kafka.clients.consumer.ConsumerRecord;
import org.apache.kafka.clients.consumer.OffsetResetStrategy;
import org.apache.kafka.common.TopicPartition;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;

import java.util.Collections;
import java.util.HashMap;
import java.util.List;
import java.util.Set;

import static org.junit.jupiter.api.Assertions.*;

public class CardConsumerTest {

    private static int testCaseCounter = 1;

    @BeforeEach
    public void printTestCaseNumber() {
        System.out.println("Running Test Case " + testCaseCounter++ + "...");
    }

    @Test
    public void testConsumeCards4() {

        String topic = "cards-topic";

        List<Card> cards = List.of(
                new Card(1, "Hearts", 10),
                new Card(2, "Diamonds", 5),
                new Card(3, "Clubs", 7),
                new Card(4, "Spades", 9)
        );

        List<String> cardJsons = List.of(
                "{\"id\":1,\"suit\":\"Hearts\",\"number\":10}",
                "{\"id\":2,\"suit\":\"Diamonds\",\"number\":5}",
                "{\"id\":3,\"suit\":\"Clubs\",\"number\":7}",
                "{\"id\":4,\"suit\":\"Spades\",\"number\":9}"
        );

        testConsumeCards(topic, cardJsons, cards);
    }

    @Test
    public void testConsumeCards10() {

        String topic = "cards-topic";


        List<Card> cards = List.of(
                new Card(11, "Hearts", 10),
                new Card(25, "Diamonds", 5),
                new Card(37, "Clubs", 7),
                new Card(43, "Spades", 9),
                new Card(56, "Hearts", 6),
                new Card(68, "Diamonds", 8),
                new Card(79, "Clubs", 4),
                new Card(82, "Spades", 12),
                new Card(91, "Hearts", 11),
                new Card(105, "Diamonds", 3)
        );

        List<String> cardJsons = List.of(
                "{\"id\":11,\"suit\":\"Hearts\",\"number\":10}",
                "{\"id\":25,\"suit\":\"Diamonds\",\"number\":5}",
                "{\"id\":37,\"suit\":\"Clubs\",\"number\":7}",
                "{\"id\":43,\"suit\":\"Spades\",\"number\":9}",
                "{\"id\":56,\"suit\":\"Hearts\",\"number\":6}",
                "{\"id\":68,\"suit\":\"Diamonds\",\"number\":8}",
                "{\"id\":79,\"suit\":\"Clubs\",\"number\":4}",
                "{\"id\":82,\"suit\":\"Spades\",\"number\":12}",
                "{\"id\":91,\"suit\":\"Hearts\",\"number\":11}",
                "{\"id\":105,\"suit\":\"Diamonds\",\"number\":3}"
        );

        testConsumeCards(topic, cardJsons, cards);
    }

    @Test
    public void testConsumeCardsStress100000() {

        String topic = "cards-topic";
        int count = 100000;

        testConsumeCardsStress(topic, count);
    }

    @Test
    public void testConsumeCardsStress1000000() {

        String topic = "cards-topic";
        int count = 1000000;

        testConsumeCardsStress(topic, count);
    }

    private static void testConsumeCards(String topic, List<String> cardJsons, List<Card> cards) {
        MockConsumer<String, String> mockConsumer = new MockConsumer<>(OffsetResetStrategy.EARLIEST);
        SimpleCardConsumer cardConsumer = new SimpleCardConsumer(mockConsumer);

        TopicPartition tp = new TopicPartition(topic, 0);
        HashMap<TopicPartition, Long> startOffsets = new HashMap<>();
        startOffsets.put(tp, 0L);
        mockConsumer.updateBeginningOffsets(startOffsets);

        mockConsumer.schedulePollTask(() -> {
            mockConsumer.rebalance(Collections.singletonList(tp));
            for (int i = 0; i < cardJsons.size(); i++) {
                mockConsumer.addRecord(new ConsumerRecord<>(topic, 0, i, String.valueOf(cards.get(i).id), cardJsons.get(i)));
            }
        });

        mockConsumer.schedulePollTask(cardConsumer::stop);

        cardConsumer.consumeCards(topic);

        Set<String> subscribedTopics = mockConsumer.subscription();
        assertTrue(subscribedTopics.contains(topic), "Consumer subscribed to correct topic: " + topic);

        List<Card> consumedCards = cardConsumer.getConsumedCards();

        assertEquals(cards.size(), consumedCards.size(), "Number of consumed cards");

        for (int i = 0; i < cards.size(); i++) {
            Card expectedCard = cards.get(i);
            Card actualCard = consumedCards.get(i);
            assertEquals(expectedCard, actualCard, "Consumed card");
        }

        assertTrue(mockConsumer.closed(), "Mock consumer closed");
    }

    private static void testConsumeCardsStress(String topic, int count) {

        Gson gson = new Gson();
        MockConsumer<String, String> mockConsumer = new MockConsumer<>(OffsetResetStrategy.EARLIEST);
        SimpleCardConsumer cardConsumer = new SimpleCardConsumer(mockConsumer);

        TopicPartition tp = new TopicPartition(topic, 0);
        HashMap<TopicPartition, Long> startOffsets = new HashMap<>();
        startOffsets.put(tp, 0L);
        mockConsumer.updateBeginningOffsets(startOffsets);

        List<Card> cards = Card.getRandomCards(count);

        mockConsumer.schedulePollTask(() -> {
            mockConsumer.rebalance(Collections.singletonList(tp));
            for (int i = 0; i < count; i++) {
                mockConsumer.addRecord(new ConsumerRecord<>(topic, 0, i, String.valueOf(cards.get(i).id), gson.toJson(cards.get(i))));
            }
        });

        mockConsumer.schedulePollTask(cardConsumer::stop);


        cardConsumer.consumeCards(topic);

        Set<String> subscribedTopics = mockConsumer.subscription();
        assertTrue(subscribedTopics.contains(topic), "Consumer subscribed to correct topic: " + topic);

        List<Card> consumedCards = cardConsumer.getConsumedCards();

        assertEquals(cards.size(), consumedCards.size(), "Number of consumed cards");

        assertTrue(mockConsumer.closed(), "Mock consumer closed");
    }
}
