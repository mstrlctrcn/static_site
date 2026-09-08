from markdown_to_blocks import markdown_to_blocks, block_to_block_type, block_type_to_tag
from htmlnode import LeafNode, ParentNode
from split_nodes import text_to_text_nodes

def markdown_to_html_node(markdown):
	block_list = markdown_to_blocks(markdown)
	node_list = []
	for block in block_list:
		#When creating the parent node, a tag and children list are needed.
		tag = block_type_to_tag(block_to_block_type(block))
		#Use textnode functions to split the text block into all of its constituent leaf nodes. This list of leaf nodes
		# will be the list of children.
		children = text_to_children(block, block_to_block_type(block))
		#Parent node needs: tag, children (props are optional)
		node = ParentNode(tag, children)
		node_list.append(node)
	return ParentNode("div", node_list)

def text_to_children(text, type):
	#Take input text and convert it to it's constituent leaf nodes
		match type:
			case BlockType.UNORDERED_LIST | BlockType.ORDERED_LIST:
				list_items = text.splitlines()
				children = []
				for item in list_items:
					line_children = textnode_to_html_node(text_to_text_nodes(item))
					children.append(ParentNode("li", line_children))
				return children
			case _:
				#Default for all others (header, paragraph, quote)
				return textnode_to_html_node(text_to_text_nodes(text))
