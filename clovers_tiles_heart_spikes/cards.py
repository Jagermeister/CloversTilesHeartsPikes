""" A collection of cards and common utilities acting on them """

from enum import Enum
import random

CARDS_IN_DECK_COUNT = 52
CARDS_IN_COLOR_COUNT = 13

DECK_BIT_MASK = (1 << CARDS_IN_DECK_COUNT) - 1

def bit_mask(index):
    return DECK_BIT_MASK - (1 << index)


class Cards:
    """ Collection of cards which may represent a deck of cards,
        a player's hand, or a discard pile. Common functionality
        provided which acts on a container.
    """

    @staticmethod
    def create(card_count):
        """ Create a new collection consisting of `card_count`
            number of cards. This is generally useful for creating
            a deck of cards, as you are given back a container which
            has all those cards.
        Args:
            card_count: int - Number of cards in container.
        """
        return 2**card_count - 1

    @staticmethod
    def add(container, card_index):
        """ Add card at index `card_index` to `container`.
        Args:
            container: int - The representation of a deck of cards.
            card_index: int - Index location of card.
        Return:
            int: Container with card added.
        """
        return container | 1 << card_index

    @staticmethod
    def remove(container, card_index):
        """ Remove card at index `card_index` to `container`.
        Args:
            container: int - The representation of a deck of cards.
            card_index: int - Index location of card.
        Return:
            int: Container with card removed.
        """
        return container & bit_mask(card_index)

    @staticmethod
    def card_peek(container, card_count):
        """ Randomly select a card within the container to return.
            This cards stays inside the container. E.g. Show me the
            next card in the deck, but do not remove it from the deck.
            Cards Peek is randomly selecting a card instead of picking the
            top card on a shuffled deck. This allows for repeated simulations
            without need to shuffle all cards each time.
        Args:
            container: int - The representation of a deck of cards.
            card_count: int - Number of remaining cards in deck.
        Returns:
            int - Selected card's index
        """
        unset_index = random.randrange(card_count)
        while unset_index:
            container &= container - 1
            unset_index -= 1

        return len(bin(container)) - len(bin(container).rstrip('0'))

#    @staticmethod
#    def color(card_index):
#        return card_index // CARDS_IN_COLOR_COUNT
#
#    @staticmethod
#    def value(card_index):
#        return card_index % CARDS_IN_COLOR_COUNT

#    @staticmethod
#    def to_index(card):
#        color, value = card
#        return CARDS_IN_COLOR_COUNT * color + value



    #@staticmethod
    #def color2(container, card_index):
    #    return (container >> (card_index * CARDS_IN_COLOR_COUNT)) & ((1 << CARDS_IN_COLOR_COUNT) - 1)

#    @staticmethod
#    def card_choice(container, card_count):
#        """ Randomly return a card from `container`. Remove that card
#            from the container.
#        Args:
#            container: int - The representation of a deck of cards.
#            card_count: int - Number of remaining cards in deck.
#        Returns:
#            container: int - Container with selected card removed
#            card: (card_color, card_value) - Selected card
#        """
#        card = Cards.card_peek(container, card_count)
#        return Cards.remove(container, card), (Cards.color(card), Cards.value(card))



#class Suit(Enum):
#    CLUBS = 0
#    DIAMONDS = 1
#    HEARTS = 2
#    SPADES = 3
#
#class Value(Enum):
#    TWO = 0
#    THREE = 1
#    FOUR = 2
#    FIVE = 3
#    SIX = 4
#    SEVEN = 5
#    EIGHT = 6
#    NINE = 7
#    TEN = 8
#    JACK = 9
#    QUEEN = 10
#    KING = 11
#    ACE = 12
#