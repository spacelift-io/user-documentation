import glob
import gzip
import re
import shutil

from pathlib import Path
from urllib.parse import urlparse

def list_src_files(path):
  files = [f for f in glob.glob(path.as_posix() + "/**/*.html", recursive=True)]
  files.append(path.joinpath("sitemap.xml").as_posix())

  return files

def read_src_file_content(path):
  return Path(path).read_text()

def save_content_to_dest_file(path, content):
  Path(path).write_text(content)

def transform_internal_urls(filename, content):
  if filename.endswith("/sitemap.xml"):
    matches = re.finditer('<loc>([^<]*)<\/loc>', content, flags=re.MULTILINE)
  else:
    matches = re.finditer('href="([^"]*)"', content, flags=re.MULTILINE)

  for match in matches:
    old_url = match.group(1)
    url_components = urlparse(old_url)

    if url_components.netloc in ["", "docs.spacelift.io"] and url_components.path.endswith(".html"):
      if url_components.path.endswith("index.html"):
        new_path = url_components.path.removesuffix("index.html")
      else:
        new_path = url_components.path.removesuffix(".html")

      new_url = url_components._replace(path=new_path).geturl()

      if filename.endswith("/sitemap.xml"):
        content = content.replace(f'<loc>{old_url}</loc>', f'<loc>{new_url}</loc>')
      else:
        content = content.replace(f'href="{old_url}"', f'href="{new_url}"')

  return content

def rebuild_sitemap_gz_file(docs_path):
  sitemap = Path(docs_path).joinpath("sitemap.xml")
  sitemap_gz = Path(docs_path).joinpath("sitemap.xml.gz")
  sitemap_gz.unlink()

  with open(sitemap, "rb") as f_in:
    with gzip.open(sitemap_gz, "wb") as f_out:
        shutil.copyfileobj(f_in, f_out)

if __name__ == "__main__":
  ROOT_DIR = Path(__file__).parent.parent.absolute()
  DOCS_DIR = ROOT_DIR.joinpath("site")

  files = list_src_files(DOCS_DIR)
  for src_file in files:
    content = read_src_file_content(src_file)
    content = transform_internal_urls(src_file, content)
    save_content_to_dest_file(src_file, content)

  rebuild_sitemap_gz_file(DOCS_DIR)
