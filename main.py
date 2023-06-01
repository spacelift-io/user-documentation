"""
This is where we define additional macros for the MkDocs macros plugin.
"""

def define_env(env):
    @env.macro
    def is_self_hosting():
        return env.page.file.src_uri.startswith('self-hosting-v')

    @env.macro
    def is_saas():
        return not is_self_hosting()
