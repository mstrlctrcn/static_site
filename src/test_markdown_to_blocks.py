import unittest
from markdown_to_blocks import markdown_to_blocks, block_to_block_type, BlockType


class TestMarkdownToBlocks(unittest.TestCase):
	def test_markdown_to_blocks(self):
		md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
		blocks = markdown_to_blocks(md)
		self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

	def test_block_to_block_type(self):
		md = []
		#Headings
		md.append(("### This Should be a HEading!", BlockType.HEADING))
		md.append(("###NO SPACE Means no good", BlockType.PARAGRAPH))
		md.append(("####### One to many Hashes", BlockType.PARAGRAPH))
		md.append(("# This is good", BlockType.HEADING))
		md.append((" ### Space before the Hashes", BlockType.PARAGRAPH))
		md.append(("#### Multiple lines \n ### Second line, but it sshould be fine.", BlockType.HEADING))
		#Codes
		md.append(("```\n ```", BlockType.CODE))
		md.append(("``` Won't work ``` \n", BlockType.PARAGRAPH))
		#Quote
		md.append((">It's a quote.", BlockType.QUOTE))
		md.append((">>It's a \n> quote", BlockType.QUOTE))
		md.append((">It's not a \n quote", BlockType.PARAGRAPH))
		#Unordered list
		md.append(("- Line \n- This should work. \n- I think.", BlockType.UNORDERED_LIST))
		md.append(("- Line one \n But not this", BlockType.PARAGRAPH))
		md.append(("- Line one \n -Or this", BlockType.PARAGRAPH))
		#Ordered List
		md.append(("1.  \n2. \n3. ", BlockType.ORDERED_LIST))
		md.append(("1. \n2.", BlockType.PARAGRAPH))
		md.append(("1. 2. 3. ", BlockType.ORDERED_LIST))

		for block in md:
			self.assertEqual(block_to_block_type(block[0]), block[1])


	PARAGRAPH = "paragraph"
	HEADING = "heading"
	CODE = "code"
	QUOTE = "quote"
	UNORDERED_LIST = "unordered_list"
	ORDERED_LIST = "ordered_list"
