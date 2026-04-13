import unittest
from htmlnode import HTMLNode, LeafNode

class TestHTMLNode(unittest.TestCase):
	def test_default_to_none(self):
		node = HTMLNode()
		self.assertEqual(node.tag, None)
		self.assertEqual(node.value, None)
		self.assertEqual(node.children, None)
		self.assertEqual(node.props, None)
	def test_tag_input_value(self):
		node = HTMLNode("/p")
		self.assertEqual(node.tag, "/p")
	def test_value_input_value(self):
		node = HTMLNode(value="test value")
		self.assertEqual(node.value, "test value")
	def test_children_input_value(self):
		sub_node1 = HTMLNode()
		sub_node2 = HTMLNode()
		sub_node_list = [sub_node1, sub_node2]
		node = HTMLNode(children=sub_node_list)
		self.assertEqual(node.children, sub_node_list)
	def test_props_input_value(self):
		property_dict = {"Prop1":"Value1"}
		node = HTMLNode(props=property_dict)
		self.assertEqual(node.props, property_dict)
	def test_leaf_node_to_html_no_props(self):
		html_string = "<a>testing</a>"
		node = LeafNode("a","testing")
		self.assertEqual(node.to_html(), html_string)
	def test_leaf_node_to_html(self):
		html_string = "<a href=test.com>testing</a>"
		node = LeafNode("a","testing",{"href":"test.com"})
		self.assertEqual(node.to_html(), html_string)
	def test_leaf_node_to_html_no_tag(self):
		html_string = "testing"
		node = LeafNode(None, "testing")
		self.assertEqual(node.to_html(), html_string)
