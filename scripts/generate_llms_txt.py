#!/usr/bin/env python3
"""
Generate llms.txt file for Spacelift Documentation according to llmstxt.org standard
"""

import os
import glob
from pathlib import Path
from typing import List, Dict, Tuple

def get_file_title(file_path: str) -> str:
    """Extract title from markdown file, falling back to filename"""
    full_path = f"docs/{file_path}"
    
    if not os.path.exists(full_path):
        return Path(file_path).stem.replace('-', ' ').title()
    
    try:
        with open(full_path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line.startswith('# '):
                    return line[2:].strip()
                elif line and not line.startswith('#'):
                    break
    except Exception:
        pass
    
    return Path(file_path).stem.replace('-', ' ').title()

def find_markdown_files() -> List[str]:
    """Find all markdown files in docs directory"""
    files = []
    for root, dirs, filenames in os.walk('docs'):
        for filename in filenames:
            if filename.endswith('.md'):
                rel_path = os.path.relpath(os.path.join(root, filename), 'docs')
                files.append(rel_path)
    return sorted(files)

def organize_files_by_section(files: List[str]) -> Dict[str, List[Tuple[str, str]]]:
    """Organize files into logical sections"""
    sections = {
        "Getting Started": [],
        "Concepts": [],
        "Vendors": [],
        "Integrations": [],
        "Product": [],
        "Installation": [],
        "Optional": []
    }
    
    for file_path in files:
        # Skip certain files
        if file_path in ['README.md'] or file_path.startswith('legal/'):
            continue
            
        title = get_file_title(file_path)
        url = f"https://docs.spacelift.io/{file_path.replace('.md', '').replace('/README', '')}"
        
        if file_path.startswith('getting-started'):
            sections["Getting Started"].append((title, url))
        elif file_path.startswith('concepts/'):
            sections["Concepts"].append((title, url))
        elif file_path.startswith('vendors/'):
            sections["Vendors"].append((title, url))
        elif file_path.startswith('integrations/'):
            sections["Integrations"].append((title, url))
        elif file_path.startswith('product/'):
            sections["Product"].append((title, url))
        elif file_path.startswith('installing-spacelift/'):
            sections["Installation"].append((title, url))
        else:
            sections["Optional"].append((title, url))
    
    # Remove empty sections
    return {k: v for k, v in sections.items() if v}

def generate_llms_txt() -> str:
    """Generate llms.txt content"""
    
    # Find all markdown files
    markdown_files = find_markdown_files()
    
    # Organize files by section
    sections = organize_files_by_section(markdown_files)
    
    # Generate llms.txt content
    content = []
    content.append("# Spacelift Documentation")
    content.append("")
    content.append("> Collaborative Infrastructure For Modern Software Teams - Complete documentation for Spacelift's infrastructure orchestration platform")
    content.append("")
    content.append("This documentation covers Spacelift, a sophisticated GitOps platform for Infrastructure as Code (IaC) that supports Terraform, OpenTofu, Terragrunt, Pulumi, CloudFormation, Ansible, and Kubernetes. Spacelift provides policy-driven automation, stack dependencies, private worker pools, and comprehensive integrations with cloud providers and development tools.")
    content.append("")
    
    # Add sections
    for section_name, files in sections.items():
        if files:
            content.append(f"## {section_name}")
            content.append("")
            for title, url in files:
                content.append(f"- [{title}]({url})")
            content.append("")
    
    return "\n".join(content)

def main():
    """Main function"""
    # Generate llms.txt content
    llms_content = generate_llms_txt()
    
    # Write to file
    with open('llms.txt', 'w', encoding='utf-8') as f:
        f.write(llms_content)
    
    print("Generated llms.txt successfully")

if __name__ == "__main__":
    main()