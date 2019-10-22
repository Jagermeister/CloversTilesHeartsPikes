"""  """

from functools import reduce
from itertools import combinations
import logging
from operator import __or__

from clovers_tiles_heart_spikes.cards import CARDS_IN_COLOR_COUNT

logging.basicConfig(level=logging.INFO)
LOGGER = logging.getLogger(__name__)

def generate_hands_from_deck(deck_card_count, hand_card_count):
    """ Choose `hand_card_count` from `deck_card_count`
    Args:
        deck_card_count: int - Total number of cards in deck
        hand_card_count: int - Cards in the hand to construct
    Returns:
        Generator of all combinations of (card value, card index)
        within choose `hand_card_count` from `deck_card_count`
    """
    deck = [(0b1 << i, i) for i in range(deck_card_count)]
    return combinations(deck, hand_card_count)

def generate_cards_from_hands():
    """ Foreach hand, generate metrics for ranking
    Returns:
        Dictionary<int, (int)>:
            Key - integer representing hand
            Value - tuple (
                [list of card indexes]
            )
    """
    cards_by_hand = {}
    hand_count = 0
    for card_list in generate_hands_from_deck(52, 5):
        if hand_count and hand_count % 250000 == 0:
            LOGGER.info(f'..cached {hand_count} hands..')

        hand_count += 1
        cards, indexes = zip(*card_list)
        hand = reduce(__or__, cards)

        is_flush = all(indexes[0]//CARDS_IN_COLOR_COUNT == index//CARDS_IN_COLOR_COUNT for index in indexes)
        card_ranks = sorted([index % CARDS_IN_COLOR_COUNT for index in indexes])
        rank_counts = {}
        for rank in card_ranks:
            if rank not in rank_counts:
                rank_counts[rank] = 0

            rank_counts[rank] += 1
        
        rank_counts = sorted(rank_counts.values(), reverse=True)
        is_four_of_a_kind = rank_counts[0] == 4
        is_full_house = rank_counts[0] == 3 and rank_counts[1] == 2
        is_three_of_a_kind = not is_full_house and rank_counts[0] == 3
        is_two_pair = rank_counts[0] == 2 and rank_counts[1] == 2
        is_one_pair = not is_two_pair and rank_counts[0] == 2

        is_straight = len(set(card_ranks)) == 5 and (
            card_ranks[-1] - card_ranks[0] == 4 or
            card_ranks[-1] - card_ranks[-2] == 9)
        is_royal_flush = is_straight and is_flush and card_ranks[-1] == 12
        is_straight_flush = not is_royal_flush and is_straight and is_flush
        is_straight = is_straight and not (is_royal_flush or is_straight_flush) 
        is_flush = is_flush and not (is_royal_flush or is_straight_flush) 

        hand_rank = reduce(__or__, [(0b1 & r) << i for i, r in enumerate([is_royal_flush,
            is_straight_flush,
            is_four_of_a_kind,
            is_full_house,
            is_flush,
            is_straight,
            is_three_of_a_kind,
            is_two_pair,
            is_one_pair])])

        cards_by_hand[hand] = (
            indexes,
            hand_rank)

    return cards_by_hand
