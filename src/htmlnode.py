class HTMLNode():
	def __init__(self, tag = None, value = None, children = None, props = None):
		#String of HTML tag name
		self.tag = tag
		#String of the value inside the node, text etc.
		self.value = value
		#List of child nodes
		self.children = children
		#Dictionary of properties or attributes of element
		self.props = props

	def __repr__(self):
		return (f"Tag: {self.tag}, Value: {self.value}, Children: {self.children}, Properties: {self.props}")

	def to_html(self):
		raise NotImplementedError()

	def props_to_html(self):
		if self.props:
			return " ".join(self.props)
		else:
			return ""

class LeafNode(HTMLNode):
	def __init__(self, tag, value, props = None):
		super().__init__(tag, value, None, props)

	def to_html(self):
		if self.value == None:
			raise ValueError("No value found")
		elif self.tag == None:
				return self.value
		else:
			tag_string = [self.tag]
			if self.props:
				for item in self.props:
					item_tag = item +"="+ self.props[item]
					tag_string.append(item_tag)
			return f"<{" ".join(tag_string)}>{self.value}</{self.tag}>"
	def __repr__(self):
		return (f"Tag: {self.tag}, Value: {self.value}, Properties: {self.props}")

class ParentNode(HTMLNode):
	def __init__(self, tag, children, props = None):
		super().__init__(tag, None, children, props)

	def to_html(self):
		if self.tag == None:
			raise ValueError("No tag found")
		elif self.children == None:
			raise ValueError("No children")
		else:
			tag_string = [self.tag]
			child_string_list = []
			if self.children:
				for child in self.children:
					child_string_list.append(child.to_html())
				child_string = " ".join(child_string_list)
			if self.props:
				for item in self.props:
					item_tag = item +"="+ self.props[item]
					tag_string.append(item_tag)
			return f"<{" ".join(tag_string)}>{child_string}</{self.tag}>"
