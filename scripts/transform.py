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

if __name__ == "__main__":
  ROOT_DIR = Path(__file__).parent.parent.absolute()
  DOCS_DIR = ROOT_DIR.joinpath("docs")

  files = list_markdown_files(DOCS_DIR)
  for src_file in files:
    content = read_src_file_content(src_file)

    content = transform_hints(content)
    content = remove_unicode_spaces(content)

    save_content_to_dest_file(src_file, content)
