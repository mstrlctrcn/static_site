import unittest
from split_nodes import (
	split_nodes_delimiter, extract_markdown_images, extract_markdown_links,
	split_nodes_image, split_nodes_link, text_to_text_nodes
)
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

	def test_image_split_text_before_and_after_2_images_single_node(self):
		text = "Test with ![link1](url.1.com) embedded, but also with bonus content: ![link2](url.2.com) So that's nice."
		text_node = TextNode(text, TextType.PLAIN)
		new_node_list = split_nodes_image([text_node])
		test_node0 = TextNode("Test with ", TextType.PLAIN)
		test_node1 = TextNode("link1", TextType.IMAGE, "url.1.com")
		test_node2 = TextNode(" embedded, but also with bonus content: ", TextType.PLAIN)
		test_node3 = TextNode("link2", TextType.IMAGE, "url.2.com")
		test_node4 = TextNode(" So that's nice.", TextType.PLAIN)
		self.assertEqual(new_node_list[0], test_node0)
		self.assertEqual(new_node_list[1], test_node1)
		self.assertEqual(new_node_list[2], test_node2)
		self.assertEqual(new_node_list[3], test_node3)
		self.assertEqual(new_node_list[4], test_node4)
	def test_image_split_no_text_before_or_after_2_images_single_node(self):
		text = "![link1](url.1.com) embedded, but also with bonus content: ![link2](url.2.com)"
		text_node = TextNode(text, TextType.PLAIN)
		new_node_list = split_nodes_image([text_node])
		test_node0 = TextNode("link1", TextType.IMAGE, "url.1.com")
		test_node1 = TextNode(" embedded, but also with bonus content: ", TextType.PLAIN)
		test_node2 = TextNode("link2", TextType.IMAGE, "url.2.com")
		self.assertEqual(new_node_list[0], test_node0)
		self.assertEqual(new_node_list[1], test_node1)
		self.assertEqual(new_node_list[2], test_node2)
	def test_image_split_with_multiple_nodes_some_needing_extraction_some_not(self):
		text = "![link1](url.1.com) embedded, but also with bonus content: ![link2](url.2.com)"
		text_2 = "Test with ![link1](url.1.com) embedded, but also with bonus content: ![link2](url.2.com)"
		image_node = TextNode("image_node", TextType.IMAGE)
		text_node = TextNode(text, TextType.PLAIN)
		bold_node = TextNode("bold text", TextType.BOLD)
		text_node_no_images = TextNode("plain text node", TextType.PLAIN)
		text_node_2 = TextNode(text_2, TextType.PLAIN)

		node_list = [image_node,  text_node, bold_node, text_node_no_images, text_node_2]

		test_node_list = []
		test_node_list.append(image_node)
		#These next ones is the split version of text_node
		test_node_list.append(TextNode("link1", TextType.IMAGE, "url.1.com"))
		test_node_list.append(TextNode(" embedded, but also with bonus content: ", TextType.PLAIN))
		test_node_list.append(TextNode("link2", TextType.IMAGE, "url.2.com"))
		#Now the bold_node and the text_node_no_images
		test_node_list.append(bold_node)
		test_node_list.append(text_node_no_images)
		#Now for text_node_2, broken up into its 4 nodes
		test_node_list.append(TextNode("Test with ", TextType.PLAIN))
		test_node_list.append(TextNode("link1", TextType.IMAGE, "url.1.com"))
		test_node_list.append(TextNode(" embedded, but also with bonus content: ", TextType.PLAIN))
		test_node_list.append(TextNode("link2", TextType.IMAGE, "url.2.com"))

		split_node_list = split_nodes_image(node_list)
		for i in range(9):
			self.assertEqual(test_node_list[i], split_node_list[i])

	#Link extraction
	def test_link_split_text_before_and_after_2_links_single_node(self):
		text = "Test with [link1](url.1.com) embedded, but also with bonus content: [link2](url.2.com) So that's nice."
		text_node = TextNode(text, TextType.PLAIN)
		new_node_list = split_nodes_link([text_node])
		test_node0 = TextNode("Test with ", TextType.PLAIN)
		test_node1 = TextNode("link1", TextType.LINK, "url.1.com")
		test_node2 = TextNode(" embedded, but also with bonus content: ", TextType.PLAIN)
		test_node3 = TextNode("link2", TextType.LINK, "url.2.com")
		test_node4 = TextNode(" So that's nice.", TextType.PLAIN)
		self.assertEqual(new_node_list[0], test_node0)
		self.assertEqual(new_node_list[1], test_node1)
		self.assertEqual(new_node_list[2], test_node2)
		self.assertEqual(new_node_list[3], test_node3)
		self.assertEqual(new_node_list[4], test_node4)
	def test_link_split_no_text_before_or_after_2_links_single_node(self):
		text = "[link1](url.1.com) embedded, but also with bonus content: [link2](url.2.com)"
		text_node = TextNode(text, TextType.PLAIN)
		new_node_list = split_nodes_link([text_node])
		test_node0 = TextNode("link1", TextType.LINK, "url.1.com")
		test_node1 = TextNode(" embedded, but also with bonus content: ", TextType.PLAIN)
		test_node2 = TextNode("link2", TextType.LINK, "url.2.com")
		self.assertEqual(new_node_list[0], test_node0)
		self.assertEqual(new_node_list[1], test_node1)
		self.assertEqual(new_node_list[2], test_node2)
	def test_link_split_with_multiple_nodes_some_needing_extraction_some_not(self):
		text = "[link1](url.1.com) embedded, but also with bonus content: [link2](url.2.com)"
		text_2 = "Test with [link1](url.1.com) embedded, but also with bonus content: [link2](url.2.com)"
		image_node = TextNode("image_node", TextType.IMAGE)
		text_node = TextNode(text, TextType.PLAIN)
		bold_node = TextNode("bold text", TextType.BOLD)
		text_node_no_images = TextNode("plain text node", TextType.PLAIN)
		text_node_2 = TextNode(text_2, TextType.PLAIN)

		node_list = [image_node,  text_node, bold_node, text_node_no_images, text_node_2]

		test_node_list = []
		test_node_list.append(image_node)
		#These next ones is the split version of text_node
		test_node_list.append(TextNode("link1", TextType.LINK, "url.1.com"))
		test_node_list.append(TextNode(" embedded, but also with bonus content: ", TextType.PLAIN))
		test_node_list.append(TextNode("link2", TextType.LINK, "url.2.com"))
		#Now the bold_node and the text_node_no_images
		test_node_list.append(bold_node)
		test_node_list.append(text_node_no_images)
		#Now for text_node_2, broken up into its 4 nodes
		test_node_list.append(TextNode("Test with ", TextType.PLAIN))
		test_node_list.append(TextNode("link1", TextType.LINK, "url.1.com"))
		test_node_list.append(TextNode(" embedded, but also with bonus content: ", TextType.PLAIN))
		test_node_list.append(TextNode("link2", TextType.LINK, "url.2.com"))

		split_node_list = split_nodes_link(node_list)
		for i in range(9):
			self.assertEqual(test_node_list[i], split_node_list[i])

	def test_text_to_text_nodes(self):
		text = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
		test_nodes =[]
		test_nodes.append(TextNode("This is ", TextType.PLAIN))
		test_nodes.append(TextNode("text", TextType.BOLD))
		test_nodes.append(TextNode(" with an ", TextType.PLAIN))
		test_nodes.append(TextNode("italic", TextType.ITALIC))
		test_nodes.append(TextNode(" word and a ", TextType.PLAIN))
		test_nodes.append(TextNode("code block", TextType.CODE))
		test_nodes.append(TextNode(" and an ", TextType.PLAIN))
		test_nodes.append(TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"))
		test_nodes.append(TextNode(" and a ", TextType.PLAIN))
		test_nodes.append(TextNode("link", TextType.LINK, "https://boot.dev"))
