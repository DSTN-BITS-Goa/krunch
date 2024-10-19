package app;

import org.apache.kafka.clients.producer.MockProducer;
import org.apache.kafka.common.serialization.StringSerializer;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;

import java.util.List;
import java.util.Objects;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertTrue;

class CardProducerTest {


    private static int testCaseCounter = 1;

    @BeforeEach
    public void printTestCaseNumber() {
        System.out.println("Running Test Case " + testCaseCounter++ + "...");
    }

    @Test
    public void testSendCardsSimple4() {

        String topic = "cards-topic";

        List<Card> cards = List.of(
                new Card(1, "Hearts", 10),
                new Card(2, "Spades", 7),
                new Card(3, "Diamonds", 5),
                new Card(4, "Clubs", 9)
        );
        List<String> cardJsons = List.of(
                "{\"id\":1,\"suit\":\"Hearts\",\"number\":10}",
                "{\"id\":2,\"suit\":\"Spades\",\"number\":7}",
                "{\"id\":3,\"suit\":\"Diamonds\",\"number\":5}",
                "{\"id\":4,\"suit\":\"Clubs\",\"number\":9}"
        );

        testSendCardsSimple(cards, topic, cardJsons);
    }

    @Test
    public void testSendCardsSimple10() {

        String topic = "cards-topic";

        List<Card> cards = List.of(
                new Card(11, "Hearts", 10),
                new Card(32, "Spades", 7),
                new Card(15, "Diamonds", 5),
                new Card(49, "Clubs", 9),
                new Card(27, "Hearts", 3),
                new Card(44, "Spades", 2),
                new Card(18, "Diamonds", 8),
                new Card(53, "Clubs", 6),
                new Card(64, "Hearts", 12),
                new Card(71, "Spades", 4)
        );

        List<String> cardJsons = List.of(
                "{\"id\":11,\"suit\":\"Hearts\",\"number\":10}",
                "{\"id\":32,\"suit\":\"Spades\",\"number\":7}",
                "{\"id\":15,\"suit\":\"Diamonds\",\"number\":5}",
                "{\"id\":49,\"suit\":\"Clubs\",\"number\":9}",
                "{\"id\":27,\"suit\":\"Hearts\",\"number\":3}",
                "{\"id\":44,\"suit\":\"Spades\",\"number\":2}",
                "{\"id\":18,\"suit\":\"Diamonds\",\"number\":8}",
                "{\"id\":53,\"suit\":\"Clubs\",\"number\":6}",
                "{\"id\":64,\"suit\":\"Hearts\",\"number\":12}",
                "{\"id\":71,\"suit\":\"Spades\",\"number\":4}"
        );

        testSendCardsSimple(cards, topic, cardJsons);
    }


    @Test
    public void testSendCardsSimpleStress100000() {

        int numCards = 100000;
        String topic = "cards-topic";

        testSendCardsSimpleStress(numCards, topic);
    }

    @Test
    public void testSendCardsSimpleStress1000000() {

        int numCards = 1000000;
        String topic = "cards-topic";

        testSendCardsSimpleStress(numCards, topic);
    }

    @Test
    public void testSendCardsMultiThreaded4() {

        String topic = "cards-topic";
        int numPartitions = 4;

        List<Card> cards = List.of(
                new Card(1, "Hearts", 10),
                new Card(2, "Spades", 7),
                new Card(3, "Diamonds", 5),
                new Card(numPartitions, "Clubs", 9)
        );

        List<String> cardJsons = List.of(
                "{\"id\":1,\"suit\":\"Hearts\",\"number\":10}",
                "{\"id\":2,\"suit\":\"Spades\",\"number\":7}",
                "{\"id\":3,\"suit\":\"Diamonds\",\"number\":5}",
                "{\"id\":4,\"suit\":\"Clubs\",\"number\":9}"
        );

        testSendCardsMultiThreaded(numPartitions, cards, topic, cardJsons);
    }

    @Test
    public void testSendCardsMultiThreaded10() {

        String topic = "cards-topic";
        int numPartitions = 4;

        List<Card> cards = List.of(
                new Card(11, "Hearts", 10),
                new Card(32, "Spades", 7),
                new Card(15, "Diamonds", 5),
                new Card(49, "Clubs", 9),
                new Card(27, "Hearts", 3),
                new Card(44, "Spades", 2),
                new Card(18, "Diamonds", 8),
                new Card(53, "Clubs", 6),
                new Card(64, "Hearts", 12),
                new Card(71, "Spades", 4)
        );

        List<String> cardJsons = List.of(
                "{\"id\":11,\"suit\":\"Hearts\",\"number\":10}",
                "{\"id\":32,\"suit\":\"Spades\",\"number\":7}",
                "{\"id\":15,\"suit\":\"Diamonds\",\"number\":5}",
                "{\"id\":49,\"suit\":\"Clubs\",\"number\":9}",
                "{\"id\":27,\"suit\":\"Hearts\",\"number\":3}",
                "{\"id\":44,\"suit\":\"Spades\",\"number\":2}",
                "{\"id\":18,\"suit\":\"Diamonds\",\"number\":8}",
                "{\"id\":53,\"suit\":\"Clubs\",\"number\":6}",
                "{\"id\":64,\"suit\":\"Hearts\",\"number\":12}",
                "{\"id\":71,\"suit\":\"Spades\",\"number\":4}"
        );

        testSendCardsMultiThreaded(numPartitions, cards, topic, cardJsons);
    }

    @Test
    public void testSendCardsMultiThreadedStress100000() {

        int numCards = 100000;
        int numPartitions = 8;
        String topic = "cards-topic";

        testSendCardsMultiThreadedStress(numPartitions, numCards, topic);
    }

    @Test
    public void testSendCardsMultiThreadedStress1000000() {

        int numCards = 1000000;
        int numPartitions = 12;
        String topic = "cards-topic";

        testSendCardsMultiThreadedStress(numPartitions, numCards, topic);
    }

    private static void testSendCardsSimple(List<Card> cards, String topic, List<String> cardJsons) {
        MockProducer<String, String> mockProducer = new MockProducer<>(true, new StringSerializer(), new StringSerializer());
        SimpleCardProducer cardProducer = new SimpleCardProducer(mockProducer);

        cardProducer.produceCards(cards, topic);
        cardProducer.flush();

        assertEquals(cards.size(), mockProducer.history().size(), "Cards produced");

        for (int i = 0; i < cardJsons.size(); i++) {
            assertEquals(cardJsons.get(i), mockProducer.history().get(i).value(), "Card " + (i + 1));
        }

        cardProducer.close();
    }

    private static void testSendCardsSimpleStress(int numCards, String topic) {
        MockProducer<String, String> mockProducer = new MockProducer<>(true, new StringSerializer(), new StringSerializer());
        SimpleCardProducer cardProducer = new SimpleCardProducer(mockProducer);

        List<Card> cards = Card.getRandomCards(numCards);

        long start = System.currentTimeMillis();
        cardProducer.produceCards(cards, topic);
        cardProducer.flush();
        long end = System.currentTimeMillis();

        assertEquals(numCards, mockProducer.history().size(), "Cards produced");

        System.out.println("Produced " + numCards + " cards in " + (end - start) + "ms");

        cardProducer.close();
    }

    private static void testSendCardsMultiThreaded(int numPartitions, List<Card> cards, String topic, List<String> cardJsons) {
        MockProducer<String, String> mockProducer = new MockProducer<>(true, new StringSerializer(), new StringSerializer());
        MultiThreadedCardProducer cardProducer = new MultiThreadedCardProducer(numPartitions, mockProducer);

        cardProducer.produceCards(cards, topic);
        cardProducer.flush();

        assertEquals(cards.size(), mockProducer.history().size(), "Cards produced");

        for (String expectedJson : cardJsons) {
            assertTrue(mockProducer.history().stream().anyMatch(record -> Objects.equals(record.value(), expectedJson)),
                    "card " + expectedJson + " found");
        }

        cardProducer.close();
    }


    private static void testSendCardsMultiThreadedStress(int numPartitions, int numCards, String topic) {
        MockProducer<String, String> mockProducer = new MockProducer<>(true, new StringSerializer(), new StringSerializer());
        MultiThreadedCardProducer cardProducer = new MultiThreadedCardProducer(numPartitions, mockProducer);
        List<Card> cards = Card.getRandomCards(numCards);

        long start = System.currentTimeMillis();
        cardProducer.produceCards(cards, topic);
        cardProducer.flush();
        long end = System.currentTimeMillis();

        assertEquals(numCards, mockProducer.history().size(), "Cards produced");

        System.out.println("Produced " + numCards + " cards in " + (end - start) + "ms");

        for (int partition = 0; partition < numPartitions; partition++) {
            int finalPartition = partition;
            assertTrue(mockProducer.history().stream().anyMatch(record -> record.partition() == finalPartition),
                    "Partition " + partition + " has a record");
        }

        cardProducer.close();
    }
}
