# Clovers Tiles Hearts Pikes
Deck of cards utilities and common entities. Name originates from the original French suit names: trèfles (clovers), carreaux (tiles), cœurs (hearts), and piques (pikes).

## Video Poker
Single-draw video poker deals a 5-card hand which players choose to hold any number of cards. The unheld cards will be replaced with new cards. This final 5-card hand is scored as a normal poker hand, although some special rules may apply such as deuces being wild. The most important aspect when choosing a strategy is understanding the poker hand distributions and the payout structure.

### Poker Hand Distribution
Looking at the game variant "Jack or Better", which means to be paid the hand must be at least as strong as a pair of Jacks, we will understand how the payout changes the distribution and therefore strategy. Let's look at all possible poker hands (52 choose 5, aka 2,598,960 combinations).

|Hand|Total Hands| |Payout| |Won|
|----|----:|----|----:|----|----:|
|Royal Flush|4|x|250|=|1,000|
|Straight Flush|36|x|50|=|1,800|
|Four Aces with 2,3,4|12|x|400|=|4,800|
|Four 4,3,2 with A,2,3,4|36|x|160|=|5,760|
|Four Aces|36|x|160|=|5,760|
|Four 4,3,2|108|x|80|=|8,640|
|Four 5s through Kings|432|x|50|=|21,600|
|Full House|3,744|x|9|=|33,696|
|Flush|5,108|x|5|=|25,540|
|Straight|10,200|x|4|=|40,800|
|Three of a Kind|54,912|x|3|=|164,736|
|Two Pair|123,552|x|1|=|123,552|
|Jacks or Better|337,920|x|1|=|337,920|

Out of 2,598,960 hands there are 536,100 winners which will return 775,604! Which means if you always hold the 5 cards you are dealt, you could expect to get back **29.84%**

### Hold Strategy
When determining which cards to hold, we must make a weighted decision about the potential payouts and the likelihood of hitting them. For instance, *Four Aces with 2, 3, 4* has the single highest payout at 400 units. Does that mean you should hold **A, 2** instead of just an **A**? Does the payout justify giving up that extra slot which could contribute to acheiving another scoring hand?





## Card Representation

Within a standard 52-card deck of French playing cards there are 13 ranks in each of the 4 suits.
**Ranks**: 2, 3, 4, 5, 6, 7, 8, 9, 10 (T), (J)ack, (Q)ueen, (K)ing, (A)ce. **Suits**: (C)lubs ♣, (D)iamonds ♦, (H)earts ♥, (S)pades ♠. Sorted, this would start with 2♣ and progress through the ranks and suits until A♠.

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
