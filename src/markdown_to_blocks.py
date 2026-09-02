def markdown_to_blocks(markdown):
	block_list = markdown.split("\n\n")
	for i in range(len(block_list)):
		block_list[i] = block_list[i].strip()
	return block_list
