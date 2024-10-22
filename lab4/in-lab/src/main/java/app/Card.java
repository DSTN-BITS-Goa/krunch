package app;


import java.util.ArrayList;
import java.util.List;
import java.util.Objects;
import java.util.Random;

class Card {
    int id;
    String suit;
    int number;


    private static final String[] SUITS = {"Hearts", "Spades", "Diamonds", "Clubs"};
    private static final Random random = new Random();

    public Card(int id, String suit, int number) {
        this.id = id;
        this.suit = suit;
        this.number = number;
    }

    public static Card getRandomCard() {
        int id = random.nextInt(10);
        String suit = SUITS[random.nextInt(SUITS.length)];
        int rank = random.nextInt(13) + 1;
        return new Card(id, suit, rank);
    }

    public static List<Card> getRandomCards(int count) {
        List<Card> cards = new ArrayList<>();
        for (int i = 0; i < count; i++) {
            cards.add(getRandomCard());
        }
        return cards;
    }

    @Override
    public boolean equals(Object o) {
        if (this == o) return true;
        if (o == null || getClass() != o.getClass()) return false;

        Card card = (Card) o;
        return id == card.id && number == card.number && Objects.equals(suit, card.suit);
    }

    @Override
    public int hashCode() {
        return Objects.hash(id, suit, number);
    }

    @Override
    public String toString() {
        return "Card{" +
                "id=" + id +
                ", suit='" + suit + '\'' +
                ", number=" + number +
                '}';
    }
}
