from textnode import TextNode, TextType

def main():
    dummy_node = TextNode("Gibberish", TextType.BOLD, "http://www.boot.dev")
    print(dummy_node)
main()