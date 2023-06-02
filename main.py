"""
This is where we define additional macros for the MkDocs macros plugin.
"""

import os

def define_env(env):
    @env.macro
    def is_self_hosting():
        return env.page.file.src_uri.startswith('self-hosting-v')

    @env.macro
    def is_saas():
        return not is_self_hosting()

    @env.macro
    def self_hosting_version_links():
        content = ""

        for item in sorted(os.scandir(os.path.join(env.project_dir, "self-hosting")), key=lambda e: e.name):
            if item.is_dir():
                content += f"- [{item.name}](./self-hosting-{item.name.replace('.', '-')})\n"

        return content
