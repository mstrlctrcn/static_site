from textnode import TextType, TextNode
import re

def text_to_text_nodes(text):
	#Break up a wall of Markdown text into individual nodes for each type.
	nodes_list = [TextNode(text, TextType.PLAIN)]
	#Separate out images, then links
	node_list = split_nodes_link(split_nodes_image(nodes_list))
	#Separate out Bold, then Italic, then Code
	node_list = split_nodes_delimiter(split_nodes_delimiter(node_list,"**", TextType.BOLD), "_", TextType.ITALIC)
	node_list = split_nodes_delimiter(node_list, "```", TextType.CODE)
	return node_list

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

def split_nodes_image(old_nodes):
	#Takes a list of old_nodes and separates out all images into their own image nodes
	# leaving non-image text as PLAIN TextNodes in an ordered list with the images nodes
	new_nodes = []
	#Cycle throught the nodes and extract the images. For each extracted image, split() the remaining text and append the
	# resultant text node before appending the image node. Then append the final remaining text node after the last image node
	for node in old_nodes:
		if node.text_type == TextType.PLAIN:
			text = node.text
			images = extract_markdown_images(node.text)
			for image in images:
				image_node = TextNode(image[0], TextType.IMAGE, image[1])
				split_text = text.split(f"![{image[0]}]({image[1]})",1)
				text = split_text[1]
				if split_text[0]:
					text_node = TextNode(split_text[0], TextType.PLAIN)
					new_nodes.append(text_node)
				new_nodes.append(image_node)
			if text:
				new_nodes.append(TextNode(text, TextType.PLAIN))
		else:
			new_nodes.append(node)

	return new_nodes
def split_nodes_link(old_nodes):
	#Takes a list of old_nodes and separates out all links into their own link nodes
	# leaving non-link text as PLAIN TextNodes in an ordered list with the link nodes
	new_nodes = []
	#Cycle throught the nodes and extract the links. For each extracted link, split() the remaining text and append the
	# resultant text node before appending the link node. Then append the final remaining text node after the last link node
	for node in old_nodes:
		if node.text_type == TextType.PLAIN:
			text = node.text
			links = extract_markdown_links(node.text)
			for link in links:
				link_node = TextNode(link[0], TextType.LINK, link[1])
				split_text = text.split(f"[{link[0]}]({link[1]})",1)
				text = split_text[1]
				if split_text[0]:
					text_node = TextNode(split_text[0], TextType.PLAIN)
					new_nodes.append(text_node)
				new_nodes.append(link_node)
			if text:
				new_nodes.append(TextNode(text, TextType.PLAIN))
		else:
			new_nodes.append(node)

	return new_nodes




def extract_markdown_images(text):
	#returns a list of tuples. Each tuple contains the image text in [0] and the image link in[1]
	images = re.findall(r"!\[.*?\)", text)
	final_images = []
	for image in images:
		link = re.findall(r"\((.*?)\)", image)
		alt_text = re.findall(r"!\[(.*?)\]", image)
		final_images.append((alt_text[0], link[0]))
	return final_images

def extract_markdown_links(text):
	# in a section of text, finds all links and then returns a list of tuples. Each tuple contains the link text in [0]
	# and the link address in [1]
	links = re.findall(r"\[.*?\].*?\(.*?\)", text)
	final_links = []
	for link in links:
		link_text = re.findall(r"\[(.*?)].*?\(.*?\)", link)
		link_address = re.findall(r"\[.*?\].*?\((.*?)\)", link)
		final_links.append((link_text[0], link_address[0]))
	return final_links
