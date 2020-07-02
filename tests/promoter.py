from unittest import TestCase, main

from peewee import IntegrityError
from werkzeug.security import generate_password_hash

from tests.utils import create_db
from services.promoter import create_promoter, check_promoter


class TestPromoterServices(TestCase):

    def setUp(self):
        # Setup in-memory database
        create_db()

    def test_create_promoter(self):
        # Promoter correcto
        promoter = create_promoter(name='Dássone J.',
                                   email='dyotamo@gmail.com',
                                   bio='fyi.',
                                   password=generate_password_hash('xyz'))

        self.assertEqual('Dássone J.', promoter.name)
        self.assertEqual('dyotamo@gmail.com', promoter.email)
        self.assertEqual('fyi.', promoter.bio)

    def test_create_incomplete_promoter(self):
        with self.assertRaises(IntegrityError):
            # Aqui faltam mais atributos para criar o promoter,
            # devendo lançar uma IntegrityError
            create_promoter(name='Dássone J.')

    def test_check_promoter(self):
        create_promoter(name='Dássone J.',
                        email='dyotamo@gmail.com',
                        bio='fyi.',
                        password=generate_password_hash('xyz'))

        # Login com senha correcta
        self.assertIsNotNone(check_promoter('dyotamo@gmail.com', 'xyz'))
        # Login cm senha errada
        self.assertIsNone(check_promoter('dyotamo@gmail.com', 'abc'))


if __name__ == '__main__':
    main()
