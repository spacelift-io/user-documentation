#!/usr/bin/env python3
"""
Unused Assets Linter for Spacelift Documentation

This script identifies assets in the docs/assets directory that are not referenced
in any markdown files throughout the documentation.

Exit codes:
- 0: No unused assets found
- 1: Unused assets found or other errors
"""

import os
import re
import glob
from pathlib import Path
from typing import Set, List, Tuple

def find_all_assets(docs_root: str) -> Set[str]:
    """Find all asset files in the docs/assets directory."""
    assets_dir = os.path.join(docs_root, "assets")
    asset_extensions = {".png", ".jpg", ".jpeg", ".gif", ".svg", ".webp", ".mov", ".mp4"}
    
    assets = set()
    for root, dirs, files in os.walk(assets_dir):
        for file in files:
            if any(file.lower().endswith(ext) for ext in asset_extensions):
                # Store relative path from docs root
                full_path = os.path.join(root, file)
                rel_path = os.path.relpath(full_path, docs_root)
                assets.add(rel_path)
    
    return assets

def find_all_markdown_files(docs_root: str) -> List[str]:
    """Find all markdown files in the docs directory."""
    md_files = []
    for root, dirs, files in os.walk(docs_root):
        for file in files:
            if file.endswith(".md"):
                md_files.append(os.path.join(root, file))
    return md_files

def extract_asset_references(md_file: str, docs_root: str) -> Set[str]:
    """Extract all asset references from a markdown file."""
    references = set()
    
    try:
        with open(md_file, 'r', encoding='utf-8') as f:
            content = f.read()
    except UnicodeDecodeError:
        try:
            with open(md_file, 'r', encoding='latin-1') as f:
                content = f.read()
        except Exception as e:
            print(f"Warning: Could not read {md_file}: {e}")
            return references
    
    # Find markdown image references: ![alt](path) and ![alt](<path>)
    # Handle angle brackets and parentheses in filenames properly
    img_pattern = r'!\[[^\]]*\]\(<([^>]+)>\)|!\[[^\]]*\]\(([^)]*(?:\([^)]*\)[^)]*)*)\)'
    img_matches = []
    for match in re.finditer(img_pattern, content):
        # match.group(1) is for <path> syntax, match.group(2) is for regular path
        path = match.group(1) if match.group(1) else match.group(2)
        if path:
            img_matches.append(path)
    
    # Find HTML img tags: <img src="path">
    html_img_pattern = r'<img[^>]+src=["\']([^"\']+)["\']'
    html_matches = re.findall(html_img_pattern, content, re.IGNORECASE)
    
    # Find HTML video/source tags
    video_pattern = r'<(?:video|source)[^>]+src=["\']([^"\']+)["\']'
    video_matches = re.findall(video_pattern, content, re.IGNORECASE)
    
    all_matches = img_matches + html_matches + video_matches
    
    for match in all_matches:
        # Skip external URLs
        if match.startswith(('http://', 'https://', '//')):
            continue
            
        # Clean up the path
        asset_path = match.strip()
        
        # Remove any query parameters or fragments
        if '?' in asset_path:
            asset_path = asset_path.split('?')[0]
        if '#' in asset_path:
            asset_path = asset_path.split('#')[0]
        
        # Handle relative paths properly
        if asset_path.startswith('../') or asset_path.startswith('./'):
            # Resolve relative path from the markdown file's directory
            md_dir = os.path.dirname(md_file)
            try:
                resolved_path = os.path.normpath(os.path.join(md_dir, asset_path))
                # Convert to path relative to docs root
                asset_path = os.path.relpath(resolved_path, docs_root)
                # Normalize separators
                asset_path = asset_path.replace('\\', '/')
            except ValueError:
                # Skip malformed paths
                continue
        elif asset_path.startswith('/'):
            # Absolute path from site root - remove leading slash
            asset_path = asset_path.lstrip('/')
        # else: assume it's already relative to docs root
        
        # Only include assets that are in the assets directory
        if asset_path.startswith('assets/') and not asset_path.startswith('assets/<'):
            references.add(asset_path)
    
    return references

def main():
    """Main function to run the unused assets linter."""
    repo_root = os.path.dirname(os.path.dirname(__file__))
    docs_root = os.path.join(repo_root, "docs")
    
    if not os.path.exists(docs_root):
        print(f"Error: docs directory not found at {docs_root}")
        return 1
    
    print("🔍 Scanning for assets and markdown files...")
    
    # Find all assets
    all_assets = find_all_assets(docs_root)
    print(f"Found {len(all_assets)} asset files")
    
    # Find all markdown files
    md_files = find_all_markdown_files(docs_root)
    print(f"Found {len(md_files)} markdown files")
    
    # Extract all asset references from markdown files
    print("📖 Analyzing markdown files for asset references...")
    referenced_assets = set()
    
    for md_file in md_files:
        file_references = extract_asset_references(md_file, docs_root)
        referenced_assets.update(file_references)
    
    print(f"Found {len(referenced_assets)} unique asset references")
    
    # Find unused assets
    unused_assets = all_assets - referenced_assets
    
    # Find missing assets (referenced but don't exist)
    missing_assets = referenced_assets - all_assets
    
    # Convert paths to be relative to repo root for cleaner output
    unused_assets_repo_relative = {f"docs/{asset}" for asset in unused_assets}
    missing_assets_repo_relative = {f"docs/{asset}" for asset in missing_assets}
    
    # Results
    print("\n" + "="*60)
    print("📊 RESULTS")
    print("="*60)
    
    if unused_assets_repo_relative:
        print(f"\n❌ UNUSED ASSETS ({len(unused_assets_repo_relative)}):")
        print("-" * 40)
        for asset in sorted(unused_assets_repo_relative):
            print(f"  {asset}")
    else:
        print("\n✅ No unused assets found!")
    
    if missing_assets_repo_relative:
        print(f"\n⚠️  MISSING ASSETS ({len(missing_assets_repo_relative)}):")
        print("-" * 40)
        for asset in sorted(missing_assets_repo_relative):
            print(f"  {asset}")
    else:
        print("\n✅ No missing asset references found!")
    
    # Summary
    print(f"\n📈 SUMMARY:")
    print(f"  Total assets: {len(all_assets)}")
    print(f"  Referenced assets: {len(referenced_assets & all_assets)}")
    print(f"  Unused assets: {len(unused_assets)}")
    print(f"  Missing assets: {len(missing_assets)}")
    print(f"  Asset usage rate: {((len(all_assets) - len(unused_assets)) / len(all_assets) * 100):.1f}%")
    
    # Return 0 only if no unused assets found (missing assets are warnings, not failures)
    return 1 if unused_assets else 0

if __name__ == "__main__":
    exit(main())
