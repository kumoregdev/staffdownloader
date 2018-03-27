import unittest
import get_staff

good_input = '{"namePreferred": "Some Guy"}'


class CleanText(unittest.TestCase):
    def test_clean_downloaded_text_happy_path(self):
        self.assertEqual(good_input, get_staff.clean_downloaded_text(good_input))

    def test_clean_downloadeD_text_removes_unencoded_zero_width_space(self):
        input = '{"namePreferred": "\u200bSome Guy"}'
        self.assertEqual(good_input, get_staff.clean_downloaded_text(input))

    def test_clean_downloadeD_text_removes_encoded_zero_width_space(self):
        input = '{"namePreferred": "\\u200bSome Guy"}'
        self.assertEqual(good_input, get_staff.clean_downloaded_text(input))

    def test_clean_downloaded_text_removes_encoded_non_blocking_space(self):
        input = '{"namePreferred": "Some\xa0Guy"}'
        self.assertEqual(good_input, get_staff.clean_downloaded_text(input))
