""" Testing functionality within ./cards.py """

from unittest import TestCase

from clovers_tiles_heart_spikes.cards import Cards


class TestCards(TestCase):
    """ Test Cards functionality """

    def test_create(self):
        """ Test various deck sizes """
        for deck_size in [2, 5, 13, 52]:
            self.assertEqual(Cards.create(deck_size), int('1' * deck_size, 2))

    def test_add_basic(self):
        """ Adding a card to a container """
        hand_card_results = [
            (0b10010, 0, 0b10011),
            (0b10010, 3, 0b11010),
            (0b10, 4, 0b10010),
            (0b000010010, 3, 0b11010),
            (0b111110010, 3, 0b111111010),
        ]
        for hand, card_index, result in hand_card_results:
            self.assertEqual(Cards.add(hand, card_index), result)

    def test_add_existing(self):
        """ Existing card remains """
        hand_card_results = [
            (0b10010, 1, 0b10010),
            (0b10010, 4, 0b10010),
        ]
        for hand, card_index, result in hand_card_results:
            self.assertEqual(Cards.add(hand, card_index), result)

    def test_remove_basic(self):
        """ Remove card from a container """
        hand_card_results = [
            (0b10010, 1, 0b10000),
            (0b10010, 4, 0b10),
            (0b000110010, 5, 0b10010),
        ]
        for hand, card_index, result in hand_card_results:
            self.assertEqual(Cards.remove(hand, card_index), result)

    def test_remove_nonexistent(self):
        """ Removing nonexistent card has no effect """
        hand_card_results = [
            (0b10010, 0, 0b10010),
            (0b10010, 2, 0b10010),
        ]
        for hand, card_index, result in hand_card_results:
            self.assertEqual(Cards.remove(hand, card_index), result)
