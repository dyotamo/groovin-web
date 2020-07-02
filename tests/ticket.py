from unittest import TestCase, main
from tests.utils import create_db


class TestEventServices(TestCase):

    def setUp(self):
        # Setup in-memory database
        create_db()

    def test_create_event(self):
        pass


if __name__ == '__main__':
    main()
