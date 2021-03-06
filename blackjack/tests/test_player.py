"""Unit-tests for blackjack/player.py module."""

import unittest
import unittest.mock

import blackjack.card
import blackjack.player


class TestPlayer(unittest.TestCase):

    def setUp(self):
        self.deck = blackjack.card.Deck()
        self.player = blackjack.player.Player('John', 5)
        self.player.hand = blackjack.card.Hand()

    def test_str(self):
        self.assertEqual(str(self.player), self.player.name)

    def test_bet(self):
        chip_count_before = self.player.chip_count
        self.player.bet(1)
        self.assertEqual(self.player.hand.wager, 1)
        self.assertEqual(self.player.chip_count, chip_count_before - 1)

    def test_bet_too_much(self):
        with self.assertRaises(blackjack.player.NoEnoughChip):
            self.player.bet(10)

    def test_earn(self):
        chip_count_before = self.player.chip_count
        self.player.earn(1)
        self.assertEqual(self.player.chip_count, chip_count_before + 1)

    def test_drop_hand(self):
        self.player.drop_hand()
        self.assertEqual(self.player.hand, None)

    def test_repr_with_no_card(self):
        self.player.hand = None
        txt = repr(self.player)
        self.assertIn(self.player.name, txt)
        self.assertIn('0', txt)
        self.assertIn(str(self.player.chip_count), txt)

    def test_repr_with_cards(self):
        self.player.hand.add_card(self.deck[0])
        txt = repr(self.player)
        self.assertIn(self.player.name, txt)
        self.assertIn('1', txt)
        self.assertIn(str(self.player.chip_count), txt)


class TestDealer(unittest.TestCase):

    def setUp(self):
        self.deck = blackjack.card.Deck()
        self.dealer = blackjack.player.Dealer('Artur')

    def test_str(self):
        self.assertIn(self.dealer.name, str(self.dealer))

    def test_str_without_name(self):
        dealer = blackjack.player.Dealer()
        self.assertEqual(str(dealer), '')

    def test_drop_hand(self):
        self.dealer.hand = blackjack.card.Hand()
        self.dealer.drop_hand()
        self.assertEqual(self.dealer.hand, None)

    def test_repr_with_no_card(self):
        self.assertIn('0', repr(self.dealer))

    def test_repr_with_cards(self):
        self.dealer.hand = blackjack.card.Hand()
        self.dealer.hand.add_card(self.deck[0])
        self.assertIn('1', repr(self.dealer))


class TestTable(unittest.TestCase):

    def setUp(self):
        deck = blackjack.card.Deck()
        shoe = blackjack.card.Shoe(deck)
        dealer = blackjack.player.Dealer()
        players = [blackjack.player.Player('John', 5)]
        self.table = blackjack.player.Table(shoe, dealer, players)

    def test_play(self):
        game = unittest.mock.Mock()
        self.table.play(game)
        game.run.assert_called_with(self.table)

