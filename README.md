# Clovers Tiles Hearts Pikes
Deck of cards utilities and common entities. Name originates from the original French suit names: trèfles (clovers), carreaux (tiles), cœurs (hearts), and piques (pikes).

## Card Representation

Within a standard 52-card deck of French playing cards there are 13 ranks in each of the 4 suits.
**Ranks**: 2, 3, 4, 5, 6, 7, 8, 9, 10 (T), (J)ack, (Q)ueen, (K)ing, (A)ce. **Suits**: (C)lubs ♣, (D)iamonds ♦, (H)earts ♥, (S)pades ♠.

Sorted, this would start with 2♣ and progress through the ranks and suits until A♠.

### Binary
Cards and collection of cards (deck, player's hands, discard pile, etc) are integers, where their binary representation shows which cards are present.
A binary representation would be a list of 1s and 0s where 1 signifies the card exists and a 0 where the card is no longer in the deck. To start this means a list of 52 1s, every card is present in the deck.

```python
# Here the first 13 characters (from the right)
# represent all the cards of the Club suit.
0b0000000000000
int(0b0000000000000) # 0 ## An empty pile of cards

# Here is an example of a five card hand with:
# A♣, Q♣, 8♣, 7♣, 3♣
0b1010001100010
int(0b1010001100010) # 5218

# 3♣----------
# 7♣------   |
# 8♣-----|   |
# Q♣-   ||   |
# A♣|   ||   |
# | |   ||   |
# V V   VV   V
0b1010001100010
```

#### Performance benefits
When performing large number of operations on cards, we want to reduce the footprint in terms of memory used, objects created, and computational time used to perform basic operations. When representing any combination of cards in a standard 52-card deck, the interger value will be between `0` and `4503599627370495`. A list of varied length might require constant appending, popping, sorting, and iterating.

Adding/removing cards can instead be simple binary operations:
```python
# Adding a card to a hand
two_of_clubs = 0b1
current_hand = 0b10101100

new_hand = current_hand | two_of_clubs
# 0b10101101
```

This keeps constant time operations.
