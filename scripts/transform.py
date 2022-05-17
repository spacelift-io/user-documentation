import glob
import re
from pathlib import Path

def list_markdown_files(path):
  return [f for f in glob.glob(str(path) + "/**/*.md", recursive=True)]

def read_src_file_content(path):
  return Path(path).read_text()

def save_content_to_dest_file(path, content):
  Path(path).write_text(content)

def transform_hints(content):
  matches = re.finditer('{% hint style="(.*?)" %}(.*?){% endhint %}', content, flags=re.DOTALL)
  for match in matches:
    hint_type = match.group(1)

    hint_lines   = match.group(2).strip().split("\n")
    hint_content = "\r".join([f"    {line}" for line in hint_lines])

    original_hint_block = match.group(0)
    new_hint_block      = f"!!! {hint_type}\n{hint_content}"

    content = content.replace(original_hint_block, new_hint_block)

  return content

def remove_unicode_spaces(content):
  return content.replace("&#x20;", "")

def remove_bold_formatting_from_headings(content):
  matches = re.finditer("^#{2,4}.*(?:\*\*|__).*(?:\*\*|__).*", content, flags=re.MULTILINE)
  for match in matches:
    src_heading = match.group(0)
    dest_heading = src_heading.replace("**", "").replace("__", "")
    content = content.replace(src_heading, dest_heading)

  return content

def remove_backslashes_in_paths(content):
  matches = re.finditer("\[(.*?)\]\((.*?)\)", content, flags=re.MULTILINE)
  for match in matches:
    src_link = match.group(0)
    description = match.group(1)
    url = match.group(2)
    url = url.replace("\_", "_")
    dest_link = f"[{description}]({url})"
    content = content.replace(src_link, dest_link)

  return content

def remove_anchors_from_headings(content):
  matches = re.finditer("^#{2,4}.*?(<a.*?><\/a>.*$)", content, flags=re.MULTILINE)
  for match in matches:
    src_heading = match.group(0)
    anchor = match.group(1)
    dest_heading = src_heading.replace(anchor, "").strip()
    content = content.replace(src_heading, dest_heading)

  return content

if __name__ == "__main__":
  ROOT_DIR = Path(__file__).parent.parent.absolute()
  DOCS_DIR = ROOT_DIR.joinpath("docs")

  files = list_markdown_files(DOCS_DIR)
  for src_file in files:
    content = read_src_file_content(src_file)

    content = transform_hints(content)
    content = remove_unicode_spaces(content)
    content = remove_bold_formatting_from_headings(content)
    content = remove_backslashes_in_paths(content)
    content = remove_anchors_from_headings(content)

    save_content_to_dest_file(src_file, content)
