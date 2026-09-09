from markdown_to_blocks import markdown_to_blocks, block_to_block_type, block_type_to_tag, BlockType
from htmlnode import LeafNode, ParentNode
from split_nodes import text_to_text_nodes
from textnode import text_node_to_html_node

def markdown_to_html_node(markdown):
	block_list = markdown_to_blocks(markdown)
	node_list = []
	for block in block_list:
		block_type = block_to_block_type(block)
		#When creating the parent node, a tag and children list are needed.
		tag = block_type_to_tag(block_type,block)
		#Use textnode functions to split the text block into all of its constituent leaf nodes. This list of leaf nodes
		# will be the list of children.
		children = text_to_children(block, block_type)
		#Parent node needs: tag, children (props are optional)
		if block_type == BlockType.CODE:
			node = ParentNode(tag, children)
			pre_node = ParentNode("pre", [node])
			node_list.append(pre_node)
		node = ParentNode(tag, children)
		node_list.append(node)
	return ParentNode("div", node_list)

def text_to_children(text, type):
	#Take input text and convert it to it's constituent leaf nodes
		match type:
			case BlockType.ORDERED_LIST:
				list_items = text.splitlines()
				children = []
				for item in list_items:
					line_nodes = text_to_text_nodes(item.split(". ", 1)[1])
					line_children = []
					for node in line_nodes:
						line_children.append(text_node_to_html_node(node))
					children.append(ParentNode("li", line_children))
				return children
			case BlockType.UNORDERED_LIST:
				list_items = text.splitlines()
				children = []
				for item in list_items:
					line_nodes = text_to_text_nodes(item.split("- ", 1)[1])
					line_children = []
					for node in line_nodes:
						line_children.append(text_node_to_html_node(node))
					children.append(ParentNode("li", line_children))
				return children
			case BlockType.HEADING:
				text = text.strip("# ")
				text_nodes = text_to_text_nodes(text)
				children = []
				for text_node in text_nodes:
					children.append(text_node_to_html_node(text_node))
				return children
			case BlockType.QUOTE:
				text = text.strip("> ")
				text_nodes = text_to_text_nodes(text)
				children = []
				for text_node in text_nodes:
					children.append(text_node_to_html_node(text_node))
				return children
			case _:
				#Default for all others (code, paragraph, quote)
				text_nodes = text_to_text_nodes(text)
				children = []
				for text_node in text_nodes:
					children.append(text_node_to_html_node(text_node))
				return children
