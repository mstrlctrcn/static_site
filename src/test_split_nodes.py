import unittest
from split_nodes import split_nodes_delimiter
from textnode import TextNode, TextType

class Test_Split_Nodes(unittest.TestCase):
	def test_single_bold_section(self):
		text_node = TextNode("Test with **bold section** embedded", TextType.PLAIN)
		new_node_list = split_nodes_delimiter([text_node], "**", TextType.BOLD)
		self.assertEqual(new_node_list[0].text, "Test with ")
		self.assertEqual(new_node_list[0].text_type, TextType.PLAIN)
		self.assertEqual(new_node_list[1].text, "bold section")
		self.assertEqual(new_node_list[1].text_type, TextType.BOLD)
		self.assertEqual(new_node_list[2].text_type, TextType.PLAIN)
		self.assertEqual(new_node_list[2].text, " embedded")
	def test_two_italic_sections(self):
		text_node = TextNode("Test with __italic section__ embedded __and another__", TextType.PLAIN)
		new_node_list = split_nodes_delimiter([text_node], "__", TextType.ITALIC)
		self.assertEqual(new_node_list[0].text, "Test with ")
		self.assertEqual(new_node_list[0].text_type, TextType.PLAIN)
		self.assertEqual(new_node_list[1].text, "italic section")
		self.assertEqual(new_node_list[1].text_type, TextType.ITALIC)
		self.assertEqual(new_node_list[2].text_type, TextType.PLAIN)
		self.assertEqual(new_node_list[2].text, " embedded ")
		self.assertEqual(new_node_list[3].text_type, TextType.ITALIC)
		self.assertEqual(new_node_list[3].text, "and another")
