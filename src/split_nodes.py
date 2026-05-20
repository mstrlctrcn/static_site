from textnode import TextType, TextNode
import re
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
	new_nodes = []
	for node in old_nodes:
		images = extract_markdown_images(node.text)
		for image in images:
			image_node = TextNode(image[0], TextType.IMAGE, image[1])
			new_nodes.append(image_node)
	return new_nodes
def split_nodes_link(old_nodes):
	#Takes a list of old_nodes and separates out all links into their own link nodes
	new_nodes = []
	for node in old_nodes:
		links = extract_markdown_links(node.text)
		for link in links:
			link_node = TextNode(link[0], TextType.LINK, link[1])




def extract_markdown_images(text):
	images = re.findall(r"!\[.*?\)", text)
	final_images = []
	for image in images:
		link = re.findall(r"\((.*?)\)", image)
		alt_text = re.findall(r"!\[(.*?)\]", image)
		final_images.append((alt_text[0], link[0]))
	return final_images

def extract_markdown_links(text):
	links = re.findall(r"\[.*?\].*?\(.*?\)", text)
	final_links = []
	for link in links:
		link_text = re.findall(r"\[(.*?)].*?\(.*?\)", link)
		link_address = re.findall(r"\[.*?\].*?\((.*?)\)", link)
		final_links.append((link_text[0], link_address[0]))
	return final_links
