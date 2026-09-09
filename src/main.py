from textnode import TextNode, TextType
from file_management import static_to_public
from generate_page import generate_pages_recursive
import sys

def main():
	if len(sys.argv) > 1:
		basepath = sys.argv[1]
	else:
		basepath = "/"
	static_to_public()
	generate_pages_recursive(basepath, "content", "template.html", "docs")
main()
