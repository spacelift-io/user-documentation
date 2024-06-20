from mkdocs.structure.files import Files
from mkdocs.config.defaults import MkDocsConfig


def on_files(files: Files, config: MkDocsConfig):
    for file in files:
        if file.dest_uri.endswith("index.html") and file.dest_uri != "index.html":
            file.dest_uri = file.dest_uri.replace("/index.html", ".html")
    return files
