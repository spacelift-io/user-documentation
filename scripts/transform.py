import glob
import os
import re
import shutil
import urllib
from pathlib import Path

def prepare_tmp_dir(path):
  if os.path.isdir(path):
    shutil.rmtree(path)
  os.makedirs(path)

def list_markdown_files(path):
  return [f for f in glob.glob(str(path) + "/**/*.md", recursive=True)]

def read_src_file_content(path):
  return Path(path).read_text()

def save_content_to_dest_file(path, content):
  path.parent.mkdir(parents=True, exist_ok=True)
  path.write_text(content)

def remove_yaml_front_matter(content):
  content = re.sub("---.*?---", "", content, count=1, flags=re.DOTALL)
  content = content.strip()

  return content

def remove_title(content):
  content = re.sub("#.*\n", "", content, count=1, flags=re.MULTILINE)
  content = content.strip()

  return content

def transform_hints(content):
  hint_types = {
    "danger": "Danger",
    "info": "Info",
    "success": "Success",
    "warning": "Warning",
  }
  for src_hint_type, dest_hint_type in hint_types.items():
    content = re.sub(f'{{% hint style="{src_hint_type}" %}}', f"!!! {dest_hint_type}", content, flags=re.MULTILINE)

  content = re.sub("{% endhint %}", "", content, flags=re.MULTILINE)

  return content

def transform_images(content):
  matches = re.finditer("!\[(.*?)\]\(.*?.gitbook\/assets\/(.*?\.(?:\w{3,4}))>?\)", content, flags=re.MULTILINE)
  for match in matches:
    src_image = match.group(0)
    description = match.group(1)
    filename = match.group(2)
    filename = filename.replace("\\", "")
    filename = urllib.parse.quote(filename)
    dest_image = f"![{description}](/assets/images/{filename})"
    content = content.replace(src_image, dest_image)

  return content

def remove_code_filenames(content):
  content = re.sub('{% code.* %}', "", content, flags=re.MULTILINE)
  content = re.sub('{% endcode %}', "", content, flags=re.MULTILINE)

  return content

def fix_links(content):
  matches = re.finditer("(?<!!)\[(.*?)\]\((.*?)\)", content, flags=re.MULTILINE)
  for match in matches:
    src_link = match.group(0)
    description = match.group(1)
    url = match.group(2)
    url = url.replace("\_", "_")
    dest_link = f"[{description}]({url})"
    content = content.replace(src_link, dest_link)

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

def remove_anchors_from_headings(content):
  matches = re.finditer("^#{2,4}.*?(<a.*?><\/a>.*$)", content, flags=re.MULTILINE)
  for match in matches:
    src_heading = match.group(0)
    anchor = match.group(1)
    dest_heading = src_heading.replace(anchor, "").strip()
    content = content.replace(src_heading, dest_heading)

  return content

def remove_code_formatting_from_headings(content):
  matches = re.finditer("^#{2,4}.*?(`.*?`).*$", content, flags=re.MULTILINE)
  for match in matches:
    src_heading = match.group(0)
    dest_heading = src_heading.replace("`", "")
    content = content.replace(src_heading, dest_heading)

  return content

if __name__ == "__main__":
  ROOT_DIR = Path(__file__).parent.parent.absolute()
  SRC_DIR = ROOT_DIR.joinpath("_src_")
  DEST_DIR = ROOT_DIR.joinpath("docs")

  files = list_markdown_files(SRC_DIR)

  for src_file in files:
    rel_src_file_path = Path(src_file).relative_to(SRC_DIR)
    dest_file = DEST_DIR.joinpath(rel_src_file_path)

    content = read_src_file_content(src_file)

    # content = remove_yaml_front_matter(content)
    # content = remove_title(content)
    content = transform_hints(content)
    content = transform_images(content)
    # content = remove_code_filenames(content)
    # content = fix_links(content)
    content = remove_unicode_spaces(content)
    content = remove_bold_formatting_from_headings(content)
    content = remove_anchors_from_headings(content)
    content = remove_code_formatting_from_headings(content)

    save_content_to_dest_file(dest_file, content)
