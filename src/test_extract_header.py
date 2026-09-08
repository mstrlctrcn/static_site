from extract_header import extract_title
import unittest

class TestExtractHeader(unittest.TestCase):
	def test_good_title_extraction(self):
		md = "# This is the title"
		self.assertEqual(extract_title(md), "This is the title")
	def test_bad_title_extraction(self):
		md = "## There is no title"
		with self.assertRaises(Exception):
			extract_title(md)
