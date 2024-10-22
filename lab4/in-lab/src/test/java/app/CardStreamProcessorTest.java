package app;

import com.google.gson.Gson;
import org.apache.kafka.common.serialization.Serdes;
import org.apache.kafka.streams.*;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.AfterEach;

import java.time.Duration;
import java.util.List;
import java.util.Properties;

import static org.apache.kafka.streams.StreamsConfig.*;
import static org.junit.jupiter.api.Assertions.assertEquals;

public class CardStreamProcessorTest {

    private TopologyTestDriver testDriver;
    private TestInputTopic<String, String> inputTopic;
    private TestOutputTopic<String, String> outputTopic;
    private final Gson gson = new Gson();

    @BeforeEach
    public void setup() {
        Properties props = new Properties();
        props.put(APPLICATION_ID_CONFIG, "in-lab-test");
        props.put(BOOTSTRAP_SERVERS_CONFIG, "dummy:1234");
        props.put(DEFAULT_KEY_SERDE_CLASS_CONFIG, Serdes.String().getClass().getName());
        props.put(DEFAULT_VALUE_SERDE_CLASS_CONFIG, Serdes.String().getClass().getName());

        CardStreamProcessor processor = new CardStreamProcessor();
        Topology topology = processor.buildTopology("card-input", "card-output");

        testDriver = new TopologyTestDriver(topology, props);

        inputTopic = testDriver.createInputTopic("card-input", Serdes.String().serializer(), Serdes.String().serializer());
        outputTopic = testDriver.createOutputTopic("card-output", Serdes.String().deserializer(), Serdes.String().deserializer());
    }

    @AfterEach
    public void tearDown() {
        testDriver.close();
    }

    @Test
    public void testcase1() {
        List<Card> cards = List.of(
                new Card(1, "Hearts", 10),
                new Card(2, "Diamonds", 5)
        );

        List<String> cardJsons = List.of(
                "{\"id\":1,\"suit\":\"Hearts\",\"number\":10}",
                "{\"id\":1,\"suit\":\"Hearts\",\"number\":10}"
        );

        inputTopic.pipeInput(cardJsons.get(0));
        inputTopic.advanceTime(Duration.ofMillis(30));
        inputTopic.pipeInput(cardJsons.get(1));

        assertEquals(1, outputTopic.getQueueSize(), "Number of flagged cards");
        assertEquals(cardJsons.get(0), outputTopic.readValue(), "flagged card");
    }

    @Test
    public void testcase2() {
        List<Card> cards = List.of(
                new Card(1, "Hearts", 10),
                new Card(2, "Hearts", 10),
                new Card(3, "Diamonds", 5),
                new Card(1, "Hearts", 10)
        );

        List<String> cardJsons = List.of(
                "{\"id\":1,\"suit\":\"Hearts\",\"number\":10}",
                "{\"id\":2,\"suit\":\"Hearts\",\"number\":10}",
                "{\"id\":3,\"suit\":\"Diamonds\",\"number\":5}",
                "{\"id\":1,\"suit\":\"Hearts\",\"number\":10}"
        );

        inputTopic.pipeInput(cardJsons.get(0));
        inputTopic.advanceTime(Duration.ofMillis(20));
        inputTopic.pipeInput(cardJsons.get(1));
        inputTopic.advanceTime(Duration.ofMillis(30));
        inputTopic.pipeInput(cardJsons.get(2));
        inputTopic.advanceTime(Duration.ofMillis(10));
        inputTopic.pipeInput(cardJsons.get(3));

        assertEquals(0, outputTopic.getQueueSize(), "Number of flagged cards");
    }

    @Test
    public void testcase3() {
        List<Card> cards = List.of(
                new Card(1, "Hearts", 10),
                new Card(2, "Diamonds", 5),
                new Card(1, "Hearts", 10),
                new Card(2, "Diamonds", 5),
                new Card(1, "Hearts", 10)
        );

        List<String> cardJsons = List.of(
                "{\"id\":1,\"suit\":\"Hearts\",\"number\":10}",
                "{\"id\":2,\"suit\":\"Diamonds\",\"number\":5}",
                "{\"id\":1,\"suit\":\"Hearts\",\"number\":10}",
                "{\"id\":2,\"suit\":\"Diamonds\",\"number\":5}",
                "{\"id\":1,\"suit\":\"Hearts\",\"number\":10}"
        );

        inputTopic.pipeInput(cardJsons.get(0));
        inputTopic.pipeInput(cardJsons.get(1));
        inputTopic.advanceTime(Duration.ofMillis(15));
        inputTopic.pipeInput(cardJsons.get(2));
        inputTopic.pipeInput(cardJsons.get(3));
        inputTopic.advanceTime(Duration.ofMillis(25));
        inputTopic.pipeInput(cardJsons.get(4));

        assertEquals(3, outputTopic.getQueueSize(), "Number of flagged cards");
        assertEquals(cardJsons.get(0), outputTopic.readValue(), "flagged card");
        assertEquals(cardJsons.get(1), outputTopic.readValue(), "flagged card");
        assertEquals(cardJsons.get(0), outputTopic.readValue(), "flagged card");
    }

    @Test
    public void testcase4() {
        List<Card> cards = List.of(
                new Card(1, "Hearts", 10),
                new Card(2, "Diamonds", 5),
                new Card(3, "Spades", 2),
                new Card(1, "Hearts", 10),
                new Card(2, "Diamonds", 5)
        );

        List<String> cardJsons = List.of(
                "{\"id\":1,\"suit\":\"Hearts\",\"number\":10}",
                "{\"id\":2,\"suit\":\"Diamonds\",\"number\":5}",
                "{\"id\":3,\"suit\":\"Spades\",\"number\":2}",
                "{\"id\":1,\"suit\":\"Hearts\",\"number\":10}",
                "{\"id\":2,\"suit\":\"Diamonds\",\"number\":5}"
        );

        inputTopic.pipeInput(cardJsons.get(0));
        inputTopic.advanceTime(Duration.ofMillis(5));
        inputTopic.pipeInput(cardJsons.get(1));
        inputTopic.advanceTime(Duration.ofMillis(4));
        inputTopic.pipeInput(cardJsons.get(2));
        inputTopic.advanceTime(Duration.ofMillis(20));
        inputTopic.pipeInput(cardJsons.get(3));
        inputTopic.advanceTime(Duration.ofMillis(6));
        inputTopic.pipeInput(cardJsons.get(4));

        assertEquals(2, outputTopic.getQueueSize(), "Number of flagged cards");
        assertEquals(cardJsons.get(0), outputTopic.readValue(), "flagged card");
        assertEquals(cardJsons.get(1), outputTopic.readValue(), "flagged card");

    }


    @Test
    public void testcase5() {
        List<Card> cards = List.of(
                new Card(1, "Hearts", 10),
                new Card(2, "Diamonds", 5),
                new Card(3, "Clubs", 8),
                new Card(1, "Hearts", 10),
                new Card(2, "Diamonds", 5),
                new Card(3, "Clubs", 8)
        );

        List<String> cardJsons = List.of(
                "{\"id\":1,\"suit\":\"Hearts\",\"number\":10}",
                "{\"id\":2,\"suit\":\"Diamonds\",\"number\":5}",
                "{\"id\":3,\"suit\":\"Clubs\",\"number\":8}",
                "{\"id\":1,\"suit\":\"Hearts\",\"number\":10}",
                "{\"id\":2,\"suit\":\"Diamonds\",\"number\":5}",
                "{\"id\":3,\"suit\":\"Clubs\",\"number\":8}"
        );

        inputTopic.pipeInput(cardJsons.get(0));
        inputTopic.advanceTime(Duration.ofMillis(20));
        inputTopic.pipeInput(cardJsons.get(1));
        inputTopic.advanceTime(Duration.ofMillis(15));
        inputTopic.pipeInput(cardJsons.get(2));
        inputTopic.advanceTime(Duration.ofMillis(5));
        inputTopic.pipeInput(cardJsons.get(3));
        inputTopic.advanceTime(Duration.ofMillis(5));
        inputTopic.pipeInput(cardJsons.get(4));
        inputTopic.advanceTime(Duration.ofMillis(25));
        inputTopic.pipeInput(cardJsons.get(5));

        assertEquals(1, outputTopic.getQueueSize(), "Number of flagged cards");
        assertEquals(cardJsons.get(1), outputTopic.readValue(), "flagged card");
    }

    @Test
    public void testcase6() {
        List<Card> cards = List.of(
                new Card(1, "Hearts", 10),
                new Card(2, "Hearts", 10),
                new Card(2, "Diamonds", 5),
                new Card(3, "Spades", 7),
                new Card(1, "Hearts", 10),
                new Card(2, "Diamonds", 5),
                new Card(3, "Spades", 7),
                new Card(4, "Clubs", 8),
                new Card(4, "Clubs", 8),
                new Card(1, "Hearts", 10)
        );

        List<String> cardJsons = List.of(
                "{\"id\":1,\"suit\":\"Hearts\",\"number\":10}",
                "{\"id\":2,\"suit\":\"Hearts\",\"number\":10}",
                "{\"id\":2,\"suit\":\"Diamonds\",\"number\":5}",
                "{\"id\":3,\"suit\":\"Spades\",\"number\":7}",
                "{\"id\":1,\"suit\":\"Hearts\",\"number\":10}",
                "{\"id\":2,\"suit\":\"Diamonds\",\"number\":5}",
                "{\"id\":3,\"suit\":\"Spades\",\"number\":7}",
                "{\"id\":4,\"suit\":\"Clubs\",\"number\":8}",
                "{\"id\":4,\"suit\":\"Clubs\",\"number\":8}",
                "{\"id\":1,\"suit\":\"Hearts\",\"number\":10}"
        );

        inputTopic.pipeInput(cardJsons.get(0));
        inputTopic.pipeInput(cardJsons.get(1));
        inputTopic.advanceTime(Duration.ofMillis(15));
        inputTopic.pipeInput(cardJsons.get(2));
        inputTopic.pipeInput(cardJsons.get(3));
        inputTopic.advanceTime(Duration.ofMillis(30));
        inputTopic.pipeInput(cardJsons.get(4));
        inputTopic.advanceTime(Duration.ofMillis(20));
        inputTopic.pipeInput(cardJsons.get(5));
        inputTopic.pipeInput(cardJsons.get(6));
        inputTopic.advanceTime(Duration.ofMillis(5));
        inputTopic.pipeInput(cardJsons.get(7));
        inputTopic.pipeInput(cardJsons.get(8));
        inputTopic.advanceTime(Duration.ofMillis(4));
        inputTopic.pipeInput(cardJsons.get(9));

        assertEquals(2, outputTopic.getQueueSize(), "Number of flagged cards");
        assertEquals(cardJsons.get(8), outputTopic.readValue(), "flagged card");
        assertEquals(cardJsons.get(9), outputTopic.readValue(), "flagged card");
    }

}
