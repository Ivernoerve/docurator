# Project Tracker file

The contents of this file keeps track of the idea/ concept , future ideas, and a prioritised task list.



---

## Idea/ concept

The idea of the docurator is to create a simple automatic documentation creator by decorating files with the docurator. 

```
.
├── src
│   └── module
└── docs
    └── documentation_target
```


### Docurator dataclasses hierarchy

* Docs: Contains the base doc attributes and is the base for all others.
* ModuleDocs: Contains Doc for modules and a list of all documented objects within
* ObjectDocs: Contains attributes to document objects
* ClassDocs: Innherits from object docs, but contains a list to store containing methods.

## Dependencies

#### [docstring_parser](https://pypi.org/project/docstring_parser/)
Description:  Parse Python docstrings. Currently support ReST, Google, Numpydoc-style and Epydoc docstrings.

Pros: The library uses only base python modules, and supports python 3.8 -> 4. Allows for parsing many different docstring types without implementing the logic myself.

Cons: Add dependency on small open source library


## To do

### MVP

1. Create decorator to capture docs

    - [x] Two modes
        - document/ doc
        - production (does not collect information)
    - [x] Factory function to return decorator based on mode
    - [x] Capture information about function to be documented, store in various `dataclass` depending on type
        -  name
        -  qualname
        -  docstring
        -  signature
        -  module 
        -  object type (inferred by module)
    - [x] Class for storing all the captured documentation. 
        - how? Partition by module, all in one list




2. Create module traverser

    - [] Object capable of traversing the target module from the given root
    - [] Traverser must invoke code to start the documentation capture/ storing.


3. Store docs
    
    - [] Markdown format.


### Ideas and future development

* Create decorator to capture docs\
    - [] support creating documentation for several users.
        - Some users would like to only read on the relevant methods whereas a potential maintainer would like more in depth knowledge.

* Store docs
    
    - [] Support templating to allow for user documentation in addition to auto doc
        - How to match the templates to the auto-documentation? Module name?

```
.
├── src
│   └── module
└── docs
    ├── documentation_target
    └── templates
```


* Use sphinx with md to compile result. 

Suport hyperlinking related functions, objects modules
