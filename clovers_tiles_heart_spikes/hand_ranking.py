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
    hand_ranks = []
    hand_count = 0
    for card_list in generate_hands_from_deck(52, 5):
        if hand_count and hand_count % 250000 == 0:
            LOGGER.info(f'..cached {hand_count} hands..')

        hand_count += 1
        cards, indexes = zip(*card_list)
        hand = reduce(__or__, cards)

        is_flush = all(indexes[0]//CARDS_IN_COLOR_COUNT == index//CARDS_IN_COLOR_COUNT for index in indexes)
        card_ranks = sorted([index % CARDS_IN_COLOR_COUNT for index in indexes])
        rank_counts = {i: 0 for i in range(CARDS_IN_COLOR_COUNT)}
        for rank in card_ranks:
            rank_counts[rank] += 1

        rank_by_count = {}
        for k, v in rank_counts.items():
            rank_by_count[v] = k
        
        rank_values = sorted(rank_counts.values(), reverse=True)
        is_four_of_a_kind = rank_values[0] == 4
        is_four_aces = is_four_of_a_kind and rank_by_count[4] == 12 # ACE
        is_four_aces_w_234 = is_four_aces and rank_by_count[1] < 3 # FIVE
        is_four_aces = is_four_aces and not is_four_aces_w_234

        is_four_432 = is_four_of_a_kind and rank_by_count[4] < 3 # FIVE
        is_four_432_w_a234 = is_four_432 and (
            rank_by_count[1] < 3 or # FIVE
            rank_by_count[1] == 12) # ACE
        is_four_432 = is_four_432 and not is_four_432_w_a234

        is_four_of_a_kind_fives_to_kings = is_four_of_a_kind and (
            rank_by_count[4] > 2 and # FOUR
            rank_by_count[4] < 12) # ACE

        is_full_house = rank_values[0] == 3 and rank_values[1] == 2
        is_three_of_a_kind = not is_full_house and rank_values[0] == 3
        is_two_pair = rank_values[0] == 2 and rank_values[1] == 2
        is_pair_jacks_or_better = not is_two_pair and rank_values[0] == 2 and rank_by_count[2] > 8 # TEN

        is_straight = len(set(card_ranks)) == 5 and (
            card_ranks[-1] - card_ranks[0] == 4 or
            card_ranks[-1] - card_ranks[-2] == 9)
        is_royal_flush = is_straight and is_flush and card_ranks[0] == 0 and card_ranks[-1] == 12
        is_straight_flush = not is_royal_flush and is_straight and is_flush
        is_straight = is_straight and not (is_royal_flush or is_straight_flush) 
        is_flush = is_flush and not (is_royal_flush or is_straight_flush) 

        hand_ranks.append({
            'hand': hand,
            'is_royal_flush': 1 if is_royal_flush else 0,
            'is_straight_flush': 1 if is_straight_flush else 0,
            'is_four_aces_w_234': 1 if is_four_aces_w_234 else 0,
            'is_four_432_w_a234': 1 if is_four_432_w_a234 else 0,
            'is_four_aces': 1 if is_four_aces else 0,
            'is_four_432': 1 if is_four_432 else 0,
            'is_four_of_a_kind_fives_to_kings': 1 if is_four_of_a_kind_fives_to_kings else 0,
            'is_full_house': 1 if is_full_house else 0,
            'is_flush': 1 if is_flush else 0,
            'is_straight': 1 if is_straight else 0,
            'is_three_of_a_kind': 1 if is_three_of_a_kind else 0,
            'is_two_pair': 1 if is_two_pair else 0,
            'is_pair_jacks_or_better': 1 if is_pair_jacks_or_better else 0,
            '2': rank_counts[0],
            '3': rank_counts[1],
            '4': rank_counts[2],
            '5': rank_counts[3],
            '6': rank_counts[4],
            '7': rank_counts[5],
            '8': rank_counts[6],
            '9': rank_counts[7],
            'T': rank_counts[8],
            'J': rank_counts[9],
            'Q': rank_counts[10],
            'K': rank_counts[11],
            'A': rank_counts[12],
        })

    return hand_ranks
