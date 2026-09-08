from markdown_to_html_node import markdown_to_html_node
from extract_header import extract_title
import os

def generate_page(from_path, template_path, dest_path):
	print(f"Generating page from {from_path} to {dest_path} using {template_path} as template.")
	with open(from_path, "r", encoding = "utf-8") as file:
		from_md = file.read()
	with open(template_path, "r", encoding = "utf-8") as file:
		template_html = file.read()
	from_html = markdown_to_html_node(from_md).to_html()
	from_title = extract_title(from_md)
	new_html = template_html.replace("{{ Title }}", from_title)
	new_html = new_html.replace("{{ Content }}", from_html)
	dest_dir = os.path.dirname(dest_path)

	if not os.path.exists(dest_dir):
		os.makedirs(dest_dir)

	with open(dest_path, "w", encoding="utf-8") as file:
		file.write(new_html)

def generate_pages_recursive(from_path, template_path, dest_path):
	print(f"Running iteration of recursive generation")
	content_list = os.listdir(from_path)
	for item in content_list:
		file_path = os.path.join(from_path, item)
		new_dest_path = os.path.join(dest_path, item)
		if os.path.isdir(file_path):
			generate_pages_recursive(file_path, template_path, new_dest_path)
		else:
			print(f"Generating page from {file_path} to {new_dest_path} using {template_path} as template.")
			with open(file_path, "r", encoding= "utf-8") as file:
				from_md = file.read()
			with open(template_path,"r", encoding="utf-8") as file:
				template_html = file.read()
			from_html = markdown_to_html_node(from_md).to_html()
			from_title = extract_title(from_md)
			new_html = template_html.replace("{{ Title }}", from_title)
			new_html = new_html.replace("{{ Content }}", from_html)
			dest_dir = os.path.dirname(new_dest_path)
			if not os.path.exists(dest_dir):
				os.makedirs(dest_dir)
			new_dest_path = new_dest_path.replace(".md", ".html")
			with open(new_dest_path, "w", encoding="utf-8") as file:
				file.write(new_html)
