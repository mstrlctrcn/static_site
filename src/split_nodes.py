from textnode import TextType, TextNode
def split_nodes_delimiter(old_nodes, delimiter, text_type):
	#Takes a list of old_nodes searches for the delimiter to find where text type changes.
	# Create new nodes separating out the sections to be turned into a separate node of a different text type
	new_nodes = []
	for node in old_nodes:
		if node.text_type == TextType.PLAIN:
			node_text = node.text.split(delimiter)
			### The text has been split up at this point. But how do I determine which sections are within a delimiter
			# and which sections are not?
			# This solution seems like it will work except for instances where there is only one delimiter and no close.
			# For a situation like that maybe can search string to determine if there is an even number before processing?
			for segment in node_text:
				if f"{delimiter}{segment}{delimiter}" in node.text:
					new_nodes.append(TextNode(segment, text_type))
				else:
					new_nodes.append(TextNode(segment, TextType.PLAIN))

		else:
			new_nodes.append(node)
