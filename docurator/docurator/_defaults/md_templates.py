"""Contains the default jinja templates for md output."""


_DEFAULT_MODULE_TEMPLATE = """
    MODULE TEMPLATE
    # {{name}}

    > {{module.short_description}}

    {{module.long_description}}
"""


_DEFAULT_FUNCTION_TEMPLATE = """
            FUNCTION TEMPLATE
            # {{name}}
            

            > {{module.short_description}}

            {{module.long_description}}
            """


_DEFAULT_class_TEMPLATE = """
    CLASS TEMPLATE
    # {{name}}

    > {{module.short_description}}

    {{module.long_description}}
"""


_DEFAULT_METHOD_TEMPLATE = """
    METHOD TEMPLATE
    # {{name}}

    > {{module.short_description}}

    {{module.long_description}}
"""


DEFAULT_TEMPLATES = {
    'module': _DEFAULT_MODULE_TEMPLATE,
    'function': _DEFAULT_FUNCTION_TEMPLATE,
    'class': _DEFAULT_class_TEMPLATE,
    'method': _DEFAULT_METHOD_TEMPLATE
}