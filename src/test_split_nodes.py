import unittest
from split_nodes import split_nodes_delimiter, extract_markdown_images, extract_markdown_links
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
	def test_two_code_sections(self):
		text_node = TextNode("Test with ```code section``` embedded ```and another```", TextType.PLAIN)
		new_node_list = split_nodes_delimiter([text_node], "```", TextType.CODE)
		self.assertEqual(new_node_list[0].text, "Test with ")
		self.assertEqual(new_node_list[0].text_type, TextType.PLAIN)
		self.assertEqual(new_node_list[1].text, "code section")
		self.assertEqual(new_node_list[1].text_type, TextType.CODE)
		self.assertEqual(new_node_list[2].text_type, TextType.PLAIN)
		self.assertEqual(new_node_list[2].text, " embedded ")
		self.assertEqual(new_node_list[3].text_type, TextType.CODE)
		self.assertEqual(new_node_list[3].text, "and another")
	def test_image_extraction(self):
		text_node = TextNode("Test with image ![alt text for image](www.test.com) embedded", TextType.PLAIN)
		image_list = extract_markdown_images(text_node.text)
		self.assertEqual(image_list[0][0], "alt text for image")
		self.assertEqual(image_list[0][1], "www.test.com")
	def test_link_extraction(self):
		text_node = TextNode("Test with [link](www.test.com) embedded", TextType.PLAIN)
		link_list = extract_markdown_links(text_node.text)
		self.assertEqual(link_list[0][0], "link")
		self.assertEqual(link_list[0][1], "www.test.com")
