from enum import Enum
import re

class BlockType(Enum):
	PARAGRAPH = "paragraph"
	HEADING = "heading"
	CODE = "code"
	QUOTE = "quote"
	UNORDERED_LIST = "unordered_list"
	ORDERED_LIST = "ordered_list"

def block_to_block_type(block):
	#Input a block of Markdown text and returns the type of block that it is.
	block_lines = block.splitlines()
	if re.match(r"#{1,6} ", block):
		return BlockType.HEADING
	elif re.match(r"```\n[\s\S]*```$", block):
		return BlockType.CODE
	elif all(re.match(r">",line) for line in block_lines):
		return BlockType.QUOTE
	elif all(re.match(r"- ",line) for line in block_lines):
		return BlockType.UNORDERED_LIST
	elif all(re.match(rf"{i}\. ",line) for i, line in enumerate(block_lines, start=1)):
		return BlockType.ORDERED_LIST
	else:
		return BlockType.PARAGRAPH

def markdown_to_blocks(markdown):
	#Take a string of markdown text and split it up, returning a list of the constituent blocks.
	block_list = markdown.split("\n\n")
	for i in range(len(block_list)):
		block_list[i] = block_list[i].strip()
	return block_list
### This section may need some adjustment once I'm home and can look at my html references.
def block_type_to_tag(type):
	match type:
		case BlockType.HEADING:
			header_num = 0
			for char in text:
				if char == "#":
					header_num +=1
				else:
					break
			return f"h{header_num}"
		case BlockType.PARAGRAPH:
			return "p"
		case BlockType.CODE:
			return "pre"
		case BlockType.QUOTE:
			return "blockquote"
		case BlockType.UNORDERED_LIST:
			return "ul"
		case BlockType.ORDERED_LIST:
			return "ol"
