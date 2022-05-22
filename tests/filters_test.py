"""This is the "filters.py" test file
"""
import unittest
from reverse_sandbox import filters


class Initialize(unittest.TestCase):
    """Test the Filters object initialization
    """

    def test_object_exists(self):
        """Tests that the Filters object can be created
        """
        filter_object = filters.Filters()
        self.assertIsNotNone(filter_object)

    def test_read(self):
        """Tests the "read_filters" function result
        """
        filter_object = filters.Filters()
        self.assertIsNotNone(filter_object.filters_ios4)
        self.assertIsNotNone(filter_object.filters_ios5)
        self.assertIsNotNone(filter_object.filters_ios6)
        self.assertIsNotNone(filter_object.filters_ios11)
        self.assertIsNotNone(filter_object.filters_ios12)
        self.assertIsNotNone(filter_object.filters_ios13)
        self.assertIsNotNone(filter_object.filters_ios14)


class Methods(unittest.TestCase):
    """Tests the Filters methods
    """
    def test_get_filters(self):
        """Tests the "get_filters" method
        """
        filter_object = filters.Filters()
        self.assertEqual(filter_object.get_filters(9), filter_object.filters_ios11)

    def test_exists(self):
        """Tests the "exists" method
        """
        filter_object = filters.Filters()
        self.assertTrue(filter_object.exists(5, 0x0d))
        self.assertFalse(filter_object.exists(11, 0xa8))

    def test_get(self):
        """Tests the "get" method
        """
        filter_object = filters.Filters()
        self.assertEqual(filter_object.get(14, 0x09), filter_object.filters_ios14.get(0x09))


if __name__ == '__main__':
    unittest.main()
