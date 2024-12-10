package app;

import com.fasterxml.jackson.databind.ObjectMapper;
import com.google.gson.Gson;
import org.apache.kafka.common.serialization.Serdes;
import org.apache.kafka.streams.*;
import org.junit.jupiter.api.*;

import java.io.File;
import java.io.IOException;
import java.time.Duration;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.Properties;

import static org.apache.kafka.streams.StreamsConfig.*;
import static org.junit.jupiter.api.Assertions.assertEquals;

@TestMethodOrder(MethodOrderer.OrderAnnotation.class)
public class CardStreamProcessorTest {

    private TopologyTestDriver testDriver;
    private TestInputTopic<String, String> inputTopic;
    private TestOutputTopic<String, String> outputTopic;
    private final Gson gson = new Gson();

    private static int testCaseCounter = 1;

    private static final int toAdd = 0;
    private static final int[] points = {10, 10, 20, 20, 30, 40};

    private static int[] actual = {0, 0, 0, 0, 0, 0};

    private static boolean withoutFailure = false;

    @BeforeEach
    public void printTestCaseNumber() {
        System.out.println("Running Test Case " + testCaseCounter++ + "...");
    }

    @AfterEach
    public void resetBool() {
        if(withoutFailure){
            actual[testCaseCounter-2] = points[testCaseCounter-2];
        }
        withoutFailure = false;
    }

    @AfterAll
    public static void printFinalPoints() {
        Map<String, Object> total = new HashMap<>();
        Map<String, Object> presentation = new HashMap<>();
        Map<String, Object> scores = new HashMap<>();
        Map<String, Integer> testCaseScores = new HashMap<>();
        int totalScore = 0;

        for (int i = 1; i <= actual.length; i++) {
            testCaseScores.put("test_case_" + (toAdd + i), actual[i - 1]);
            totalScore += actual[i - 1];
        }

        total.put("total", totalScore);
        presentation.put("_presentation", "semantic");
        scores.put("scores", testCaseScores);

        ObjectMapper mapper = new ObjectMapper();
        try {
            String targetDir = System.getProperty("user.dir") + "/target";
            File targetFile = new File(targetDir, "test_results_streams.txt");

            mapper.writeValue(targetFile, total);
            try (var writer = new java.io.FileWriter(targetFile, true)) {
                writer.write("\n");
                writer.write(mapper.writeValueAsString(presentation));
                writer.write("\n");
                writer.write(mapper.writeValueAsString(scores));
            }

            System.out.println("Test results written to: " + targetFile.getAbsolutePath());
        } catch (IOException e) {
            e.printStackTrace();
        }
    }

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
    @Order(1)
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

        withoutFailure = true;
    }

    @Test
    @Order(2)
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
        withoutFailure = true;
    }

    @Test
    @Order(3)
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
        withoutFailure = true;
    }

    @Test
    @Order(4)
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
        withoutFailure = true;

    }


    @Test
    @Order(5)
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
        withoutFailure = true;
    }

    @Test
    @Order(6)
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
        withoutFailure = true;
    }

}