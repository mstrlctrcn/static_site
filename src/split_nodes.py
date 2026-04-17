from textnode import TextType, TextNode
def split_nodes_delimiter(old_nodes, delimiter, text_type):
	#Takes a list of old_nodes searches for the delimiter to find where text type changes.
	# Create new nodes separating out the sections to be turned into a separate node of a different text type
	new_nodes = []
	for node in old_nodes:
		if node.text_type == TextType.PLAIN:
			if node.text.count(delimiter) %2 != 0:
				raise Exception("Odd number of delimiters used")
				return
			node_text = node.text.split(delimiter)
			### The text has been split up at this point. But how do I determine which sections are within a delimiter
			# and which sections are not?
			# This solution seems like it will work except for instances where there is only one delimiter and no close.
			# For a situation like that maybe can search string to determine if there is an even number before processing?
			# Resolved Odd number delimiters. But now a new issue:
				# in a string with more than 2 delimiters, the current code will identify all text as within a delimiter zone
				# because it does not distinguish between what is a starting delimiter and what is an ending delimiter.

			#Instead of splitting everything at once, go through the code one segment at a time with an on/off switch to determine
			# whether you are within or outside of a delimited section.
			for i in range(len(node_text)):
				if node_text[i] == "":
					continue
				elif i%2 == 0:
					new_nodes.append(TextNode(node_text[i], TextType.PLAIN))
				else:
					new_nodes.append(TextNode(node_text[i], text_type))

		else:
			new_nodes.append(node)
	return new_nodes
