import re
def extract_title(markdown):
	matches = re.findall(r"^#\s+(.+)$", markdown, re.MULTILINE)
	if matches:
		heading = matches[0].strip()
	else:
		raise Exception("No Title Header")
	return heading
