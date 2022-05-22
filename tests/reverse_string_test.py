"""This is the "reverse_string.py" test file
"""
import unittest
from reverse_sandbox import reverse_string


class Initialize(unittest.TestCase):
    """Test the ReverseStringState object initialization
    """

    def test_object_exists(self):
        """Tests that the ReverseStringState object can be created
        """
        rss = reverse_string.ReverseStringState("0000")
        self.assertIsNotNone(rss)
        self.assertEqual(rss.binary_string, "0000")

    def test_init_with_no_args(self):
        """Tests the initialisation with no arguments
        """
        with self.assertRaises(TypeError):
            reverse_string.ReverseStringState()


class Methods(unittest.TestCase):
    """Tests the ReverseStringState methods
    """
    def test_update_state(self):
        """Tests the "update_state" method, and by it all its submethods
        """
        rss = reverse_string.ReverseStringState("0000")
        # Tests the "update_state_end_byte_read" method and the state_stack updating
        rss.update_state(0x0a)
        self.assertEqual(rss.state, rss.STATE_END_BYTE_READ)
        self.assertEqual(rss.state_stack[-1], rss.STATE_UNKNOWN)
        # Tests the "update_state_concat_byte_read" method
        rss.update_state(0x0f)
        self.assertEqual(rss.state, rss.STATE_CONCAT_BYTE_READ)
        # Tests the "update_state_split_byte_read" method
        rss.update_state(0x80)
        self.assertEqual(rss.state, rss.STATE_SPLIT_BYTE_READ)
        # Tests the "update_state_unknown" method
        rss.update_state(0x00)
        self.assertEqual(rss.state, rss.STATE_UNKNOWN)
        rss.update_state(0x07)
        self.assertEqual(rss.state, rss.STATE_UNKNOWN)
        # Tests the "update_state_reset_string" method
        rss.update_state(0x05)
        self.assertEqual(rss.state, rss.STATE_RESET_STRING)
        # Tests the "update_state_concat_save_byte_read" method
        rss.update_state(0x08)
        self.assertEqual(rss.state, rss.STATE_CONCAT_SAVE_BYTE_READ)
        # Tests the "update_state_constant_read" method with extreme values
        rss.update_state(0x10)
        self.assertEqual(rss.state, rss.STATE_CONSTANT_READ)
        rss.update_state(0x3e)
        self.assertEqual(rss.state, rss.STATE_CONSTANT_READ)
        # Tests the "update_state_range_byte_read" method
        rss.update_state(0x0b)
        self.assertEqual(rss.state, rss.STATE_RANGE_BYTE_READ)
        # Tests the "update_state_plus_read" method
        rss.update_state(0x02)
        self.assertEqual(rss.state, rss.STATE_PLUS_READ)
        # Tests the "update_state_reset_string" method
        rss.update_state(0x06)
        self.assertEqual(rss.state, rss.STATE_RESET_STRING)
        # Tests the "update_state_token_byte_read" method with 3f byte
        rss.update_state(0x3f)
        self.assertEqual(rss.state, rss.STATE_TOKEN_BYTE_READ)

    def test_get_next_byte(self):
        """Tests the "get_next_byte" method
        """
        # Tests the is_end() case
        rss_ending = reverse_string.ReverseStringState("0000")
        rss_ending.pos = 4
        self.assertEqual(rss_ending.get_next_byte(), 0x00)
        # Tests the return value with byte 0 (ascii value: 48)
        rss = reverse_string.ReverseStringState("0000")
        self.assertEqual(rss.get_next_byte(), 48)

    def test_get_length_minus_1(self):
        """Tests the "get_length_minus_1" method
        """
        # Tests the case b == 0x04 - string is EOT
        rss = reverse_string.ReverseStringState(chr(4) + "0")
        rss.pos = 1
        self.assertEqual(rss.get_length_minus_1(), 0x71)
        # Tests the classic case
        rss = reverse_string.ReverseStringState("A")
        rss.pos = 1
        self.assertEqual(rss.get_length_minus_1(), 0x02)

    def test_read_token(self):
        """Tests the "read_token" method
        """
        rss = reverse_string.ReverseStringState("0000")
        rss.read_token(2)
        self.assertEqual(rss.token, "00")
        self.assertEqual(rss.pos, 2)

    def test_update_base(self):
        """Tests the "update_base" method
        """
        rss = reverse_string.ReverseStringState("0000")
        rss.token = "1234"
        rss.update_base()
        self.assertEqual(rss.token, "")
        self.assertEqual(rss.base[-4:], "1234")

    def test_update_base_stack(self):
        """Tests the "update_base_stack" method
        """
        rss = reverse_string.ReverseStringState("0000")
        rss.base = "1234"
        rss.update_base_stack()
        self.assertEqual(rss.base_stack[-1], "1234")

    def test_end_current_token(self):
        """Tests the "end_current_token" method
        """
        rss = reverse_string.ReverseStringState("0000")
        rss.base = "12"
        rss.token = "34"
        rss.end_current_token()
        self.assertEqual(rss.output_strings[-1], "1234")
        self.assertEqual(rss.token, "")

    def test_get_last_byte(self):
        """Tests the "get_last_byte" method
        """
        rss = reverse_string.ReverseStringState("0123")
        rss.pos = 1
        last_byte = rss.get_last_byte()
        self.assertEqual(last_byte, 0x30)

    def test_get_substring(self):
        """Tests the "get_substring" method
        """
        rss = reverse_string.ReverseStringState("0000")
        substr = rss.get_substring(2)
        self.assertEqual(substr, "00")
        self.assertEqual(rss.pos, 2)

    def test_end_with_subtokens(self):
        """Tests the "end_with_subtokens" method
        """
        rss = reverse_string.ReverseStringState("0000")
        rss.token = "1234"
        rss.end_with_subtokens(["AB", "CD"])
        self.assertEqual(rss.output_strings[-2:], ["1234AB", "1234CD"])
        self.assertEqual(rss.token, "")

    def test_is_end(self):
        """Tests the "is_end" method
        """
        # Tests not ended case
        rss = reverse_string.ReverseStringState("0000")
        self.assertFalse(rss.is_end())
        # Tests ended case
        rss.pos = 4
        self.assertTrue(rss.is_end())

    def test_reset_base(self):
        """Tests the "reset_base" method
        """
        rss = reverse_string.ReverseStringState("0000")
        rss.base_stack = ["12", "34"]
        rss.reset_base()
        self.assertEqual(rss.base_stack[-1], "12")
        self.assertEqual(rss.base, "34")

    def test_reset_base_full(self):
        """Tests the "reset_base_full" method
        """
        rss = reverse_string.ReverseStringState("0000")
        rss.base_stack = ["12", "34"]
        rss.reset_base_full()
        self.assertEqual(rss.base_stack, [])
        self.assertEqual(rss.base, "")


if __name__ == '__main__':
    unittest.main()
