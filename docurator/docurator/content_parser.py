# ruff: noqa
# This ignores all errors in this file. It is present as this is a work in progress/ test file at the moment.
# Remove when work on this files implementations are performed.
from typing import Any
from inspect import Signature

import docstring_parser.google
from docurator._components.module_traverser import invoke_modules
from docurator.docurator_object import docurator
from docurator._components.doc_containers import ClassDocs, Docs, ModuleDocs
from docurator._components.config_loader import TemplateSetBuilder, ConfigBuilder 

import docstring_parser

from dataclasses import dataclass, make_dataclass, field
import inspect
import jinja2
import re

@dataclass(frozen=True)
class SectionContent:
    name: str
    description: str

@dataclass(frozen=True)
class ArgumentSectionContent(SectionContent):
    kind: str
    annotation: str
    default: Any


@dataclass(frozen=True)
class ReturnsSectionContent(SectionContent):
    annotation: str
    is_generator: bool

# Handle yield and returns.

@dataclass(frozen=True)
class SignatureArg:
    name: str
    kind: str
    annotation: str
    default: Any

@dataclass(frozen=True)
class CombinedContainer:
    name: str

    arguments: list[SignatureArg]
    __signature: Signature

    @property
    def signature(self) -> str:
        return str(self.__signature)

    @property
    def definition(self) -> str:
        return f'{self.name}{self.__signature}'

    @property
    def return_annotation(self) -> str:
        return DocParser.parse_annotation(
            self.__signature.return_annotation
        )


class DocParser:
    def __init__(self, docurator_config: dict) -> None:
        self.config = docurator_config
        self.parser = self.__get_parser_class(
            docurator_config['docstring_format'],
            docurator_config['extra_sections']
        )

    def parse(self, content: Docs) -> dict[str, Any]:
        common_output_dict = {
            'name': content.name
        }
        parsed_docstring = self.parse_docstring(content)

        common_output_dict['full_description'] = parsed_docstring.description
        common_output_dict['short_description'] = parsed_docstring.short_description
        common_output_dict['long_description'] = parsed_docstring.long_description

        if len(self.config['extra_sections']) > 1:
            sections = self.config['extra_sections']
            extra_sections = self.__create_extra_sections_dataclass_instance(sections)
            for section in sections:
                section_list = getattr(extra_sections, section)
                section_list.extend(
                    [SectionContent(m.args[1], m.description) for m in parsed_docstring.meta if m.args[0] == section]
                )

            common_output_dict['extra_sections'] = extra_sections

        if isinstance(content, ModuleDocs):
            return common_output_dict

        signature_args = self.parse_args(content)

        arguments = self.__combine_doc_and_signature_arg_outputs(parsed_docstring.params, signature_args)
        returns = self.__combine_doc_and_signature_return_outputs(
            parsed_docstring.returns,
            content.f_signature
        )
        common_output_dict['arguments'] = arguments
        common_output_dict['returns'] = returns


        common_output_dict['raises'] = [SectionContent(r.args[1], r.description) for r in parsed_docstring.raises]
        common_output_dict['examples'] = [SectionContent(e.args[-1], e.description) for e in parsed_docstring.examples]

        common_output_dict['signature'] = str(content.f_signature)
        common_output_dict['definition'] = f'{content.name}{content.f_signature}'
        @property
        def signature(self) -> str:
            return str(self.__signature)

        @property
        def definition(self) -> str:
            return f'{self.name}{self.__signature}'

        return common_output_dict

    def __combine_doc_and_signature_arg_outputs(self, doc_output: list, signature_output: list) -> list[ArgumentSectionContent]:
        # TODO Have a prioritization parameter in the config referenced here 
        # Will prioritize signature per now.
        consolidated_outputs = []
        for sig in signature_output:
            doc = [d for d in doc_output if d.arg_name == sig.name][0]
            output = ArgumentSectionContent(
                name=sig.name,
                description=doc.description,
                kind=sig.kind,
                annotation=sig.annotation,
                default=sig.default
            )
            consolidated_outputs.append(output)

        return consolidated_outputs

    def __combine_doc_and_signature_return_outputs(self, doc_return, sig_return) -> ReturnsSectionContent:
        output = ReturnsSectionContent(
            name=doc_return.args[0],
            description=doc_return.description,
            annotation=sig_return.return_annotation,
            is_generator=doc_return.is_generator
        )
        return output



    @staticmethod
    def __create_extra_sections_dataclass_instance(extra_sections: list[str]) -> dataclass:
        ExtraSectionsClass = make_dataclass(
            'ExtraSections',
            [(name, list[SectionContent], field(default_factory=list)) for name in extra_sections]
        )
        return ExtraSectionsClass()


    @staticmethod
    def __get_parser_class(docstring_format: str, extra_section: list[str] = None) -> None:
        parser = docstring_parser.google.GoogleParser()
        if extra_section is None:
            return parser

        SectionType = docstring_parser.google.SectionType
        Section = docstring_parser.google.Section
        for section in extra_section:
            cap = section.capitalize()
            lower = section.lower()

            section = Section(
                cap,
                lower,
                SectionType.MULTIPLE
            )
            parser.add_section(section)
        return parser

    def parse_docstring(self, content: Docs):
        docstring = content.docstring
        parsed = self.parser.parse(docstring)

        return parsed

    @classmethod
    def parse_args(cls, content: Docs):
        sig = content.f_signature
        args = sig.parameters
        parsed_args = []
        for arg in args.values():
            if arg.default is inspect.Parameter.empty:
                default = ''
            elif arg.default is None:
                default = 'optional'
            else:
                default = f'optional: default = {arg.default}'

            parsed_args.append(
                SignatureArg(
                    name=arg.name,
                    kind=str(arg.kind).replace('_', ' ').capitalize(),
                    annotation=cls.parse_annotation(arg.annotation),
                    default=default
                )
            )
        return parsed_args

    @staticmethod
    def parse_annotation(annotation: Any) -> str | None:
        if any(annotation is t for t in (inspect.Parameter.empty, None)):
               return None

        if not hasattr(annotation, '__origin__'): 
            return annotation.__name__

        origin = annotation.__origin__
        args = annotation.__args__

        return f'{origin.__name__}[{", ".join([arg.__name__ for arg in args])}]'

path = 'docurator'


if __name__ == '__main__':
    invoke_modules(path)

    templates = TemplateSetBuilder().get()
    config = ConfigBuilder().get()

    module = docurator.docs['test_src.advanced_operations']
    func = list(filter(lambda x: x.name == 'fibonacci_sequence', module.contents))[0]

    par = DocParser.parse_args(func)
    parsed = DocParser(config).parse(func)

    print(parsed)


    template = """
FUNCTION TEMPLATE
# {{name}}
    
```
{{definition}}
```

> {{short_description}}

{{long_description}}

## Arguments
{% for arg in arguments %}
* {{arg.name}}: {{arg.annotation}}, {{arg.default}} {{arg.kind}}
    {{arg.description}}
{% endfor %}
    """



    environment = jinja2.Environment()
    template = environment.from_string(template)
    t = template.render(**parsed)
    print(t)
