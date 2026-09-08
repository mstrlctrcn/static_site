from textnode import TextNode, TextType
from file_management import static_to_public
from generate_page import generate_pages_recursive

def main():
    dummy_node = TextNode("Gibberish", TextType.BOLD, "http://www.boot.dev")
    print(dummy_node)
    static_to_public()
    generate_pages_recursive("content", "template.html", "public")
main()
