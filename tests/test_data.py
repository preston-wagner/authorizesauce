from datetime import date, datetime, timedelta

from unittest2 import TestCase

from authorizesauce.data import Address, CreditCard
from authorizesauce.exceptions import AuthorizeInvalidError


TEST_CARD_NUMBERS = [
    ('amex', '370000000000002'),
    ('mc', '5555555555554444'),
    ('mc', '5105105105105100'),
    ('discover', '6011000000000012'),
    ('visa', '4007000000027'),
    ('visa', '4012888818888'),
    ('diners', '38000000000006'),
]


class CreditCardTests(TestCase):
    def setUp(self):
        self.YEAR = date.today().year + 10

    def test_basic_credit_card(self):
        credit_card = CreditCard('4111-1111-1111-1111', self.YEAR, 1, '911')
        repr(credit_card)

    def test_credit_card_validation(self):
        # Expiration in the past fails
        expired = date.today() - timedelta(days=31)
        self.assertRaises(AuthorizeInvalidError, CreditCard,
            '4111111111111111', expired.year, expired.month, '911')

        # CVV in wrong format fails
        self.assertRaises(AuthorizeInvalidError, CreditCard,
            '4111111111111111', self.YEAR, 1, 'incorrect')

        # Invalid credit card number fails
        self.assertRaises(AuthorizeInvalidError, CreditCard,
            '4111111111111112', self.YEAR, 1, '911')

        # Test standard test credit card numbers that should validate
        for card_type, card_number in TEST_CARD_NUMBERS:
            CreditCard(card_number, self.YEAR, 1, '911')

    def test_credit_card_type_detection(self):
        for card_type, card_number in TEST_CARD_NUMBERS:
            credit_card = CreditCard(card_number, self.YEAR, 1, '911')
            self.assertEqual(credit_card.card_type, card_type)

    def test_credit_card_expiration(self):
        credit_card = CreditCard('4111111111111111', self.YEAR, 1, '911')
        self.assertEqual(credit_card.expiration,
            datetime(self.YEAR, 1, 31, 23, 59, 59))

    def test_credit_card_safe_number(self):
        credit_card = CreditCard('4111111111111111', self.YEAR, 1, '911')
        self.assertEqual(credit_card.safe_number, '************1111')


class AddressTests(TestCase):
    def test_basic_address(self):
        address = Address('45 Rose Ave', 'Venice', 'CA', '90291')
        repr(address)
