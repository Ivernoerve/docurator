from docstring_parser import google
from module_traverser import invoke_modules
from docurator import docurator
from doc_containers import ClassDocs, Docs

path = 'docurator'


class DocDisplayFormatter:
    def __init__(self, content: Docs) -> None:
        self.content = content

    
    



invoke_modules(path)
temp_doc = docurator



for name, module in temp_doc.docs.items():
    print(name)
    module_docs = module.contents
    for obj in module_docs:
        print(obj.name)
        if isinstance(obj, ClassDocs):
            for method in obj.contents:
                print('   - ', method.name)


