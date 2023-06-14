"""
This is where we define additional macros for the MkDocs macros plugin.
"""

import os

def define_env(env):
    @env.macro
    def is_self_hosted():
        return env.variables.spacelift_distribution == "SELF_HOSTED"

    @env.macro
    def is_saas():
        return not is_self_hosted()
