"""
Hook to embed markdown content into pages for LLM copy functionality.
Captures the processed markdown (after Jinja rendering) and embeds it with
frontmatter, title, and URL for easy copying to clipboard.
"""

import json
import re


def on_page_content(html, page, config, files):
    """
    Called after markdown is converted to HTML but before template is applied.
    Capture the processed markdown and store it in page metadata.
    """
    # Get the rendered markdown (post-Jinja processing)
    markdown_content = page.markdown

    # Build the formatted content for LLM
    llm_content_parts = []

    # Add page title
    if page.title:
        llm_content_parts.append(f"# {page.title}\n")

    # Add page URL
    site_url = config.get('site_url', '').rstrip('/')
    page_url = f"{site_url}/{page.file.dest_uri}"
    llm_content_parts.append(f"**Source:** {page_url}\n")

    # Add frontmatter if it exists
    if page.meta:
        # Only include common frontmatter fields
        frontmatter_fields = {}
        common_fields = ['title', 'description', 'tags', 'date', 'author']
        for field in common_fields:
            if field in page.meta:
                frontmatter_fields[field] = page.meta[field]

        if frontmatter_fields:
            llm_content_parts.append("\n---")
            for key, value in frontmatter_fields.items():
                if isinstance(value, list):
                    llm_content_parts.append(f"{key}: {', '.join(str(v) for v in value)}")
                else:
                    llm_content_parts.append(f"{key}: {value}")
            llm_content_parts.append("---\n")

    # Add the actual markdown content
    llm_content_parts.append("\n" + markdown_content)

    # Combine all parts
    llm_content = "\n".join(llm_content_parts)

    # Store in page meta for later injection
    page.llm_content = llm_content

    return html


def on_post_page(output, page, config):
    """
    Called after the template is rendered. Inject the LLM content and button.
    """
    if not hasattr(page, 'llm_content'):
        return output

    # Escape the content for HTML embedding
    # Use a hidden div instead of script tag because script tags don't work with innerHTML
    import html
    safe_content = html.escape(page.llm_content)

    # Create hidden div with the data
    content_div = f"""<div id="llm-markdown-content" style="display: none;" data-content="{safe_content}"></div>"""

    # Create the button HTML
    button_html = """<button type="button" class="copy-to-llm-button" title="Copy documentation for LLM">
      <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
        <rect x="9" y="9" width="13" height="13" rx="2" ry="2"></rect>
        <path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1"></path>
      </svg>
      <span>Copy for LLM</span>
    </button>"""

    # Inject button at the top of the right sidebar (Table of Contents)
    # Look for the secondary sidebar and inject at the beginning of its content
    sidebar_pattern = r'(<div[^>]*class="[^"]*md-sidebar--secondary[^"]*"[^>]*>.*?<div[^>]*class="[^"]*md-sidebar__scrollwrap[^"]*"[^>]*>)'
    if re.search(sidebar_pattern, output, re.DOTALL):
        output = re.sub(sidebar_pattern, r'\1\n' + button_html + '\n', output, count=1, flags=re.DOTALL)
    else:
        # Fallback: inject after the first h1 tag if sidebar not found
        h1_pattern = r'(<h1[^>]*>.*?</h1>)'
        if re.search(h1_pattern, output, re.DOTALL):
            output = re.sub(h1_pattern, r'\1\n' + button_html, output, count=1, flags=re.DOTALL)

    # Inject div BEFORE closing </article> so it's part of the swapped content
    if '</article>' in output:
        output = output.replace('</article>', f'{content_div}\n</article>', 1)
    elif '</body>' in output:
        output = output.replace('</body>', f'{content_div}\n</body>', 1)

    return output
